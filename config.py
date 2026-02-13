"""Configuration management for NewsAgent."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Gmail Configuration
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# News Settings
NUM_STORIES = int(os.getenv('NUM_STORIES', 6))

# News Sources Configuration
NEWS_SOURCES = {
    'tech': [
        {
            'name': 'Hacker News',
            'type': 'api',
            'url': 'https://hacker-news.firebaseio.com/v0/topstories.json'
        },
        {
            'name': 'TechCrunch',
            'type': 'rss',
            'url': 'https://techcrunch.com/feed/'
        },
        {
            'name': 'The Verge',
            'type': 'rss',
            'url': 'https://www.theverge.com/rss/index.xml'
        },
        {
            'name': 'Wired',
            'type': 'rss',
            'url': 'https://www.wired.com/feed/rss'
        },
        {
            'name': 'Ars Technica',
            'type': 'rss',
            'url': 'https://feeds.arstechnica.com/arstechnica/index'
        }
    ],
    'finance': [
        {
            'name': 'Reuters Business',
            'type': 'rss',
            'url': 'https://feeds.reuters.com/reuters/businessNews'
        },
        {
            'name': 'Financial Times',
            'type': 'rss',
            'url': 'https://www.ft.com/?format=rss'
        },
        {
            'name': 'Yahoo Finance',
            'type': 'rss',
            'url': 'https://finance.yahoo.com/news/rssindex'
        },
        {
            'name': 'CNBC',
            'type': 'rss',
            'url': 'https://www.cnbc.com/id/100003114/device/rss/rss.html'
        },
        {
            'name': 'Bloomberg Markets',
            'type': 'rss',
            'url': 'https://feeds.bloomberg.com/markets/news.rss'
        }
    ]
}

def validate_config():
    """Validate that all required configuration is present."""
    missing = []

    if not ANTHROPIC_API_KEY:
        missing.append('ANTHROPIC_API_KEY')
    if not GMAIL_USER:
        missing.append('GMAIL_USER')
    if not GMAIL_APP_PASSWORD:
        missing.append('GMAIL_APP_PASSWORD')
    if not RECIPIENT_EMAIL:
        missing.append('RECIPIENT_EMAIL')

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return True
