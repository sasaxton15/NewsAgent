# NewsAgent — AI-Powered Daily News Digest

A personal AI agent that reads dozens of sources every morning and delivers a curated digest to your inbox. Built with Python and Claude AI.

> I built this because I was spending too much time tab-hopping between news sites. Now I get one clean email with the stories that actually matter, summarized and ranked by Claude.

---

## What it does

Every day, NewsAgent:

1. **Fetches** stories from 13+ sources across 4 categories — AI, Finance, Industry, and Marketing
2. **Ranks** them using Claude AI, prioritizing the most signal-rich stories
3. **Summarizes** each one in 2 sentences + a "Why it matters" line
4. **Delivers** a clean, TLDR-style HTML digest to your inbox

<!-- Add a screenshot of your email digest here -->
<!-- ![NewsAgent Digest](screenshot.png) -->

---

## Categories & Sources

| Category | Sources |
|---|---|
| 🤖 AI & Technology | Hacker News, The Rundown AI, Hugging Face Blog, VentureBeat, MIT Technology Review, The New Stack |
| 💰 Finance & Markets | Reuters, Yahoo Finance, CNBC, Bloomberg Markets |
| 🏢 Industry & Business | Harvard Business Review, Fortune, Fast Company |
| 📣 Marketing | Digiday, Adweek, Marketing Week |

---

## Setup

### Prerequisites
- Python 3.8+
- [Anthropic API key](https://console.anthropic.com/) (Claude)
- Gmail account

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/NewsAgent.git
cd NewsAgent
```

### 2. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure your environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...        # From console.anthropic.com
GMAIL_USER=you@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx  # See below
RECIPIENT_EMAIL=you@gmail.com
NUM_STORIES=8                       # Total stories across all categories
```

**Getting a Gmail App Password:**
1. Enable 2-Factor Authentication on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate a password for "Mail" — copy the 16 characters

### 4. Run it

```bash
python3 main.py
```

---

## Automate it

### GitHub Actions (recommended — free, no server needed)

The repo includes a workflow that runs daily at 7 AM UTC. Just add your credentials as repository secrets:

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GMAIL_USER` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Your Gmail app password |
| `RECIPIENT_EMAIL` | Where to send the digest |

The workflow at `.github/workflows/daily-news.yml` handles the rest.

### macOS / Linux (cron)

```bash
crontab -e
# Add this line to run at 8 AM daily:
0 8 * * * cd /path/to/NewsAgent && venv/bin/python3 main.py >> newsagent.log 2>&1
```

---

## Customization

### Add your own sources

Open `config.py` and add any RSS feed to the relevant category:

```python
NEWS_SOURCES = {
    'ai': [
        {
            'name': 'Your Source',
            'type': 'rss',
            'url': 'https://example.com/feed.xml'
        },
        # ...existing sources
    ],
}
```

### Add a new category

Add an entry to both `NEWS_SOURCES` and `CATEGORY_CONFIG` in `config.py`:

```python
CATEGORY_CONFIG = {
    'crypto': {
        'label': 'Crypto & Web3',
        'emoji': '🪙',
        'color': '#f39c12',
    },
}
```

### Change story count

```bash
NUM_STORIES=12  # 3 per category if you have 4 categories
```

---

## How the AI works

NewsAgent makes three types of Claude API calls per run:

1. **Ranking** — Given all fetched headlines, Claude selects the most important stories per category based on signal value (e.g. for AI: model releases, agent frameworks, policy shifts)
2. **Summarizing** — Each article is fetched and summarized in 2 facts + a "Why it matters" line
3. **Daily brief** — A 2-sentence overview of the day's key themes, used as the email intro

---

## Cost

Running this daily costs roughly **$0.05–$0.15/day** depending on story count, using Claude Haiku.

---

## Troubleshooting

**No email received** — Check spam, verify `RECIPIENT_EMAIL`, and confirm Gmail App Password is correct (no spaces).

**Claude API error** — Verify your `ANTHROPIC_API_KEY` and that your account has credits.

**RSS feed errors** — Some feeds go down occasionally. The agent continues with available sources and logs warnings.

---

## Built with

- [Claude AI](https://anthropic.com) — story ranking, summarization, daily brief
- [feedparser](https://pythonhosted.org/feedparser/) — RSS parsing
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — article content extraction
- [GitHub Actions](https://github.com/features/actions) — daily scheduling

---

MIT License
