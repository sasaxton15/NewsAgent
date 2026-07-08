"""Fetch news from various sources including Hacker News API and RSS feeds."""
import calendar
import time
from typing import Dict, List, Optional, Set
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TRACKING_PARAMS = {'fbclid', 'gclid', 'mc_cid', 'mc_eid', 'cmpid', 'partner', 'ref', 'src'}


class NewsFetcher:
    """Fetches news from multiple sources."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        retry_strategy = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    @staticmethod
    def normalize_url(url: str) -> str:
        """Canonicalize a URL so the same story matches across feeds and runs."""
        url = (url or "").strip()
        if not url:
            return ""
        try:
            scheme, netloc, path, query, _ = urlsplit(url)
            params = [
                (k, v) for k, v in parse_qsl(query, keep_blank_values=True)
                if k.lower() not in TRACKING_PARAMS and not k.lower().startswith('utm_')
            ]
            return urlunsplit((
                scheme.lower(),
                netloc.lower(),
                path.rstrip('/'),
                urlencode(params),
                '',
            ))
        except ValueError:
            return url

    @staticmethod
    def _age_hours(epoch: Optional[float]) -> Optional[float]:
        """Hours elapsed since a unix timestamp, or None if unknown."""
        if not epoch:
            return None
        return max(0.0, (time.time() - epoch) / 3600)

    def fetch_hacker_news(self, num_stories: int = 10) -> List[Dict]:
        """Fetch top stories from Hacker News API."""
        try:
            response = self.session.get(
                'https://hacker-news.firebaseio.com/v0/topstories.json',
                timeout=10
            )
            response.raise_for_status()
            story_ids = response.json()[:num_stories]

            stories = []
            for story_id in story_ids:
                try:
                    story_response = self.session.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=10
                    )
                    story_response.raise_for_status()
                    story_data = story_response.json()

                    if story_data and story_data.get('url'):
                        stories.append({
                            'title': story_data.get('title', ''),
                            'url': story_data.get('url', ''),
                            'source': 'Hacker News',
                            'score': story_data.get('score', 0),
                            'text': story_data.get('text', ''),
                            'time': story_data.get('time', 0),
                            'age_hours': self._age_hours(story_data.get('time')),
                        })
                except Exception as e:
                    print(f"Error fetching HN story {story_id}: {e}")
                    continue

            return stories
        except Exception as e:
            print(f"Error fetching Hacker News: {e}")
            return []

    def fetch_rss_feed(self, feed_url: str, source_name: str, num_stories: int = 10) -> List[Dict]:
        """Fetch stories from an RSS feed."""
        try:
            response = self.session.get(feed_url, timeout=15)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            if getattr(feed, "bozo", 0):
                print(f"Warning: RSS feed parse issue for {source_name}: {feed.bozo_exception}")

            stories = []
            for entry in feed.entries[:num_stories]:
                published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                epoch = calendar.timegm(published_parsed) if published_parsed else None
                stories.append({
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'source': source_name,
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'time': published_parsed,
                    'age_hours': self._age_hours(epoch),
                })

            return stories
        except Exception as e:
            print(f"Error fetching RSS feed from {source_name}: {e}")
            return []

    def fetch_all_news(self, sources: Dict, num_per_source: int = 10) -> Dict[str, List[Dict]]:
        """Fetch news from all configured sources."""
        all_news = {category: [] for category in sources}

        for category, source_list in sources.items():
            for source in source_list:
                if source['type'] == 'api' and source['name'] == 'Hacker News':
                    stories = self.fetch_hacker_news(num_per_source)
                    all_news[category].extend(stories)
                elif source['type'] == 'rss':
                    stories = self.fetch_rss_feed(
                        source['url'],
                        source['name'],
                        num_per_source
                    )
                    all_news[category].extend(stories)

        return all_news

    def deduplicate_stories(self, stories: List[Dict], seen_urls: Optional[Set[str]] = None) -> List[Dict]:
        """Remove duplicate stories by normalized URL.

        Pass a shared `seen_urls` set to also dedupe across categories.
        """
        deduped = []
        if seen_urls is None:
            seen_urls = set()
        for story in stories:
            url = self.normalize_url(story.get("url", ""))
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            deduped.append(story)
        return deduped

    def filter_recent(self, stories: List[Dict], max_age_hours: float) -> List[Dict]:
        """Drop stories older than max_age_hours; keep stories with no publish date."""
        return [
            s for s in stories
            if s.get('age_hours') is None or s['age_hours'] <= max_age_hours
        ]

    def extract_article_content(self, url: str) -> str:
        """
        Attempt to extract article content from URL.
        Returns a snippet for summarization.
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'lxml')

            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            main_content = soup.find('article') or soup.find('main') or soup.find('body')

            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                return text[:6000]

            return ""
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
