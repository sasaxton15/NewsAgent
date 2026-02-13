"""Summarize news articles using Claude AI."""
import re
import time
from typing import Dict, List

from anthropic import Anthropic
from anthropic import APIError, APITimeoutError, RateLimitError


class ArticleSummarizer:
    """Uses Claude to summarize news articles."""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.max_retries = 3

    def _create_message_with_retry(self, prompt: str, max_tokens: int) -> str:
        """Call Claude with retries for transient API failures."""
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text
            except (RateLimitError, APITimeoutError, APIError) as e:
                if attempt == self.max_retries:
                    raise
                wait_seconds = 2 ** attempt
                print(f"Claude API transient error (attempt {attempt}/{self.max_retries}): {e}. Retrying in {wait_seconds}s...")
                time.sleep(wait_seconds)

    def rank_and_select_stories(self, tech_stories: List[Dict], finance_stories: List[Dict], num_stories: int) -> Dict[str, List[Dict]]:
        """
        Use Claude to rank stories by importance and select top N from each category.
        """
        tech_titles = "\n".join([f"{i+1}. {s['title']} (from {s['source']})"
                                  for i, s in enumerate(tech_stories[:20])])
        finance_titles = "\n".join([f"{i+1}. {s['title']} (from {s['source']})"
                                     for i, s in enumerate(finance_stories[:20])])

        prompt = f"""You are a news curator. Review these tech and finance news stories and select the {num_stories//2} most important stories from each category.

TECH STORIES:
{tech_titles}

FINANCE STORIES:
{finance_titles}

Please respond with just the story numbers (comma-separated) for each category in this exact format:
TECH: 1,3,5
FINANCE: 2,4,7

Select stories based on:
- Significance and impact
- Novelty and relevance
- Broad interest
- Major company/market news"""

        try:
            result_text = self._create_message_with_retry(prompt, max_tokens=200)

            # Parse the response
            selected = {'tech': [], 'finance': []}
            for line in result_text.strip().split('\n'):
                if line.startswith('TECH:'):
                    tech_nums = [int(n) - 1 for n in re.findall(r"\d+", line)]
                    selected['tech'] = [tech_stories[i] for i in tech_nums if i < len(tech_stories)]
                elif line.startswith('FINANCE:'):
                    finance_nums = [int(n) - 1 for n in re.findall(r"\d+", line)]
                    selected['finance'] = [finance_stories[i] for i in finance_nums if i < len(finance_stories)]

            if not selected["tech"]:
                selected["tech"] = tech_stories[:num_stories // 2]
            if not selected["finance"]:
                selected["finance"] = finance_stories[:num_stories // 2]
            return selected
        except Exception as e:
            print(f"Error ranking stories: {e}")
            # Fallback: just take the first N stories
            return {
                'tech': tech_stories[:num_stories//2],
                'finance': finance_stories[:num_stories//2]
            }

    def summarize_article(self, title: str, content: str, url: str) -> str:
        """
        Summarize a single article to 2-3 sentences using Claude.
        """
        prompt = f"""Summarize this news article in exactly 2-3 clear, informative sentences. Focus on the key facts and implications.

Title: {title}

Content: {content}

Provide only the summary, no additional commentary."""

        try:
            summary = self._create_message_with_retry(prompt, max_tokens=150).strip()
            return summary
        except Exception as e:
            print(f"Error summarizing article '{title}': {e}")
            return "Unable to generate summary for this article."

    def summarize_stories(self, stories: List[Dict], fetcher) -> List[Dict]:
        """
        Summarize a list of stories.
        """
        summarized_stories = []

        for story in stories:
            print(f"Summarizing: {story['title']}")

            # Try to extract content for better summarization
            content = fetcher.extract_article_content(story['url'])

            # Fallback to existing summary/text if content extraction fails
            if not content:
                content = story.get('summary', story.get('text', ''))

            # If still no content, use just the title
            if not content:
                content = "No additional content available."

            summary = self.summarize_article(story['title'], content, story['url'])

            summarized_stories.append({
                'title': story['title'],
                'url': story['url'],
                'source': story['source'],
                'summary': summary
            })

        return summarized_stories
