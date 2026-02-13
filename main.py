#!/usr/bin/env python3
"""
NewsAgent - Daily Tech & Finance News Digest
Fetches, summarizes, and emails top news stories.
"""
import json
import os
import sys
from datetime import datetime

import config
from news_fetcher import NewsFetcher
from summarizer import ArticleSummarizer
from email_formatter import EmailFormatter
from email_sender import EmailSender

SEEN_ARTICLES_FILE = "seen_articles.json"
SEEN_ARTICLES_RETENTION_DAYS = 7


def load_seen_articles(path: str) -> dict:
    """Load URL -> last_seen_timestamp mapping from disk."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_seen_articles(path: str, seen_articles: dict) -> None:
    """Persist URL -> last_seen_timestamp mapping to disk."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(seen_articles, f, indent=2)


def prune_seen_articles(seen_articles: dict, now_ts: int) -> dict:
    """Keep only recently seen URLs."""
    cutoff = now_ts - (SEEN_ARTICLES_RETENTION_DAYS * 86400)
    pruned = {}
    for url, seen_ts in seen_articles.items():
        try:
            ts = int(seen_ts)
        except (TypeError, ValueError):
            continue
        if ts >= cutoff:
            pruned[url] = ts
    return pruned


def filter_new_stories(stories: list, seen_articles: dict) -> list:
    """Remove stories that were sent recently."""
    return [story for story in stories if story.get("url") not in seen_articles]


def main():
    """Main execution function."""
    print("=" * 60)
    print("NewsAgent - Daily News Digest Generator")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    sender = None
    try:
        # Validate configuration
        try:
            config.validate_config()
            print("✓ Configuration validated")
        except ValueError as e:
            print(f"✗ Configuration error: {e}")
            print("\nPlease create a .env file based on .env.example and fill in your credentials.")
            return 1

        # Initialize components
        print("\nInitializing components...")
        fetcher = NewsFetcher()
        summarizer = ArticleSummarizer(config.ANTHROPIC_API_KEY)
        formatter = EmailFormatter()
        sender = EmailSender(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
        print("✓ All components initialized")

        # Fetch news
        print("\n" + "-" * 60)
        print("STEP 1: Fetching news from sources...")
        print("-" * 60)
        all_news = fetcher.fetch_all_news(config.NEWS_SOURCES, num_per_source=10)
        all_news["tech"] = fetcher.deduplicate_stories(all_news["tech"])
        all_news["finance"] = fetcher.deduplicate_stories(all_news["finance"])
        fetched_news = {
            "tech": list(all_news["tech"]),
            "finance": list(all_news["finance"]),
        }

        seen_articles = prune_seen_articles(
            load_seen_articles(SEEN_ARTICLES_FILE),
            int(datetime.now().timestamp()),
        )
        all_news["tech"] = filter_new_stories(all_news["tech"], seen_articles)
        all_news["finance"] = filter_new_stories(all_news["finance"], seen_articles)

        tech_count = len(all_news['tech'])
        finance_count = len(all_news['finance'])
        print(f"✓ Fetched {tech_count} new tech stories")
        print(f"✓ Fetched {finance_count} new finance stories")

        if tech_count == 0 and finance_count == 0:
            print("\nNo unseen stories found. Falling back to best available current stories.")
            all_news = fetched_news

        # Rank and select top stories
        print("\n" + "-" * 60)
        print(f"STEP 2: Selecting top {config.NUM_STORIES} most important stories...")
        print("-" * 60)
        selected_stories = summarizer.rank_and_select_stories(
            all_news['tech'],
            all_news['finance'],
            config.NUM_STORIES
        )

        tech_selected = len(selected_stories['tech'])
        finance_selected = len(selected_stories['finance'])
        print(f"✓ Selected {tech_selected} tech stories")
        print(f"✓ Selected {finance_selected} finance stories")

        # Summarize stories
        print("\n" + "-" * 60)
        print("STEP 3: Generating summaries with Claude AI...")
        print("-" * 60)

        print("\nSummarizing tech stories...")
        tech_summarized = summarizer.summarize_stories(selected_stories['tech'], fetcher)
        print(f"✓ Completed {len(tech_summarized)} tech summaries")

        print("\nSummarizing finance stories...")
        finance_summarized = summarizer.summarize_stories(selected_stories['finance'], fetcher)
        print(f"✓ Completed {len(finance_summarized)} finance summaries")

        # Format email
        print("\n" + "-" * 60)
        print("STEP 4: Formatting email digest...")
        print("-" * 60)
        html_content = formatter.format_digest(tech_summarized, finance_summarized)
        plain_text = formatter.format_plain_text(tech_summarized, finance_summarized)
        print("✓ Email formatted")

        # Send email
        print("\n" + "-" * 60)
        print("STEP 5: Sending email...")
        print("-" * 60)
        success = sender.send_digest(
            config.RECIPIENT_EMAIL,
            html_content,
            plain_text
        )

        # Summary
        print("\n" + "=" * 60)
        if success:
            now_ts = int(datetime.now().timestamp())
            for story in tech_summarized + finance_summarized:
                url = story.get("url")
                if url:
                    seen_articles[url] = now_ts
            save_seen_articles(SEEN_ARTICLES_FILE, seen_articles)

            print("SUCCESS! Your news digest has been sent.")
            print(f"Recipient: {config.RECIPIENT_EMAIL}")
            print(f"Total stories: {len(tech_summarized) + len(finance_summarized)}")
        else:
            print("FAILED to send email. Please check the error messages above.")
            sender.send_failure_alert(config.RECIPIENT_EMAIL, "Digest email send step failed.")
            return 1

        print("=" * 60)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        return 0
    except Exception as e:
        error_message = str(e)
        print(f"Unhandled error: {error_message}")
        if sender and config.RECIPIENT_EMAIL:
            sender.send_failure_alert(config.RECIPIENT_EMAIL, error_message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
