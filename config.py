"""Configuration management for NewsAgent."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Gmail Configuration
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# News Settings — total stories across all categories (2 per category default)
NUM_STORIES = int(os.getenv('NUM_STORIES', 8))

# Category display configuration
CATEGORY_CONFIG = {
    'ai': {
        'label': 'AI & Technology',
        'emoji': '\U0001f916',
        'color': '#6c5ce7',
    },
    'finance': {
        'label': 'Finance & Markets',
        'emoji': '\U0001f4b0',
        'color': '#00b894',
    },
    'industry': {
        'label': 'Industry & Business',
        'emoji': '\U0001f3e2',
        'color': '#0984e3',
    },
    'marketing': {
        'label': 'Marketing',
        'emoji': '\U0001f4e3',
        'color': '#e17055',
    },
}

# News Sources Configuration
NEWS_SOURCES = {
    'ai': [
        {
            'name': 'Hacker News',
            'type': 'api',
            'url': 'https://hacker-news.firebaseio.com/v0/topstories.json',
        },
        {
            'name': 'The Rundown AI',
            'type': 'rss',
            'url': 'https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml',
        },
        {
            'name': 'Hugging Face Blog',
            'type': 'rss',
            'url': 'https://huggingface.co/blog/feed.xml',
        },
        {
            'name': 'VentureBeat',
            'type': 'rss',
            'url': 'https://venturebeat.com/feed',
        },
        {
            'name': 'MIT Technology Review',
            'type': 'rss',
            'url': 'https://www.technologyreview.com/feed/',
        },
        {
            'name': 'The New Stack',
            'type': 'rss',
            'url': 'https://thenewstack.io/feed/',
        },
    ],
    'finance': [
        {
            'name': 'Reuters Business',
            'type': 'rss',
            'url': 'https://feeds.reuters.com/reuters/businessNews',
        },
        {
            'name': 'Yahoo Finance',
            'type': 'rss',
            'url': 'https://finance.yahoo.com/news/rssindex',
        },
        {
            'name': 'CNBC',
            'type': 'rss',
            'url': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        },
        {
            'name': 'Bloomberg Markets',
            'type': 'rss',
            'url': 'https://feeds.bloomberg.com/markets/news.rss',
        },
    ],
    'industry': [
        {
            'name': 'Harvard Business Review',
            'type': 'rss',
            'url': 'https://feeds.hbr.org/harvardbusiness',
        },
        {
            'name': 'Fortune',
            'type': 'rss',
            'url': 'https://fortune.com/feed/',
        },
        {
            'name': 'Fast Company',
            'type': 'rss',
            'url': 'https://www.fastcompany.com/latest/rss',
        },
    ],
    'marketing': [
        {
            'name': 'Digiday',
            'type': 'rss',
            'url': 'https://digiday.com/feed/',
        },
        {
            'name': 'Adweek',
            'type': 'rss',
            'url': 'https://www.adweek.com/feed/',
        },
        {
            'name': 'Marketing Week',
            'type': 'rss',
            'url': 'https://www.marketingweek.com/feed/',
        },
    ],
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
