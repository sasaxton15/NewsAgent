# NewsAgent - Daily Tech & Finance News Digest

An intelligent news aggregation agent that fetches top tech and finance stories, summarizes them using Claude AI, and delivers a beautifully formatted digest to your Gmail inbox daily.

## Features

- Fetches news from multiple sources:
  - **Tech**: Hacker News, TechCrunch, The Verge
  - **Finance**: Reuters, Bloomberg, WSJ
- Uses Claude AI to:
  - Rank and select the most important stories
  - Generate concise 2-3 sentence summaries
- Sends a clean, formatted HTML email digest
- Runs locally with easy automation options

## Project Structure

```
NewsAgent/
├── main.py              # Main orchestration script
├── config.py            # Configuration management
├── news_fetcher.py      # News fetching from APIs and RSS feeds
├── summarizer.py        # Claude AI summarization
├── email_formatter.py   # HTML email formatting
├── email_sender.py      # Gmail SMTP sender
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Prerequisites

- Python 3.8 or higher
- Gmail account
- Anthropic API key (for Claude)

## Setup Instructions

### 1. Clone or Navigate to Project

```bash
cd /Users/srandlesims/NewsAgent
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your API Keys

#### Anthropic API Key (Claude)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

#### Gmail App Password
1. Enable 2-Factor Authentication on your Gmail account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and your device
4. Click "Generate"
5. Copy the 16-character password (remove spaces)

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```bash
# Anthropic API Key for Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Gmail Configuration
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your16charpassword

# Email Settings
RECIPIENT_EMAIL=your.email@gmail.com

# News Preferences (number of stories in digest)
NUM_STORIES=6
```

## Usage

### Run Manually

To generate and send your news digest right now:

```bash
python3 main.py
```

You should see output like:

```
============================================================
NewsAgent - Daily News Digest Generator
============================================================
Started at: 2024-01-26 09:00:00

✓ Configuration validated

Initializing components...
✓ All components initialized

------------------------------------------------------------
STEP 1: Fetching news from sources...
------------------------------------------------------------
✓ Fetched 30 tech stories
✓ Fetched 30 finance stories

------------------------------------------------------------
STEP 2: Selecting top 6 most important stories...
------------------------------------------------------------
✓ Selected 3 tech stories
✓ Selected 3 finance stories

------------------------------------------------------------
STEP 3: Generating summaries with Claude AI...
------------------------------------------------------------
Summarizing tech stories...
✓ Completed 3 tech summaries

Summarizing finance stories...
✓ Completed 3 finance summaries

------------------------------------------------------------
STEP 4: Formatting email digest...
------------------------------------------------------------
✓ Email formatted

------------------------------------------------------------
STEP 5: Sending email...
------------------------------------------------------------
Connecting to Gmail SMTP server...
Logging in...
Sending email to your.email@gmail.com...
Email sent successfully!

============================================================
SUCCESS! Your news digest has been sent.
Recipient: your.email@gmail.com
Total stories: 6
============================================================
```

### Automate Daily Delivery

#### Option 1: macOS/Linux (cron)

1. Open crontab editor:
```bash
crontab -e
```

2. Add this line to run daily at 8 AM:
```bash
0 8 * * * cd /Users/srandlesims/NewsAgent && /Users/srandlesims/NewsAgent/venv/bin/python3 main.py >> /Users/srandlesims/NewsAgent/newsagent.log 2>&1
```

3. Save and exit (`:wq` in vim)

#### Option 2: macOS (launchd)

Create a file at `~/Library/LaunchAgents/com.newsagent.daily.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.newsagent.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/srandlesims/NewsAgent/venv/bin/python3</string>
        <string>/Users/srandlesims/NewsAgent/main.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/srandlesims/NewsAgent</string>
    <key>StandardOutPath</key>
    <string>/Users/srandlesims/NewsAgent/newsagent.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/srandlesims/NewsAgent/newsagent.log</string>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.newsagent.daily.plist
```

#### Option 3: Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to Daily at your preferred time
4. Action: Start a program
5. Program: `C:\Path\To\NewsAgent\venv\Scripts\python.exe`
6. Arguments: `main.py`
7. Start in: `C:\Path\To\NewsAgent`

## Customization

### Change News Sources

Edit `config.py` and modify the `NEWS_SOURCES` dictionary:

```python
NEWS_SOURCES = {
    'tech': [
        {
            'name': 'Your Source',
            'type': 'rss',
            'url': 'https://example.com/feed.xml'
        }
    ],
    'finance': [
        # Add your sources here
    ]
}
```

### Adjust Number of Stories

Change `NUM_STORIES` in your `.env` file:

```bash
NUM_STORIES=10  # Get 10 stories total (5 tech, 5 finance)
```

### Customize Email Style

Edit `email_formatter.py` to modify the HTML template and styling.

## Troubleshooting

### Gmail Authentication Errors

- Make sure you're using an App Password, not your regular password
- Verify 2FA is enabled on your Google account
- Check that "Less secure app access" is not blocking you

### No Stories Fetched

- Check your internet connection
- Some RSS feeds may be temporarily unavailable
- Try running with fewer sources first

### Claude API Errors

- Verify your API key is correct
- Check you have available credits
- Ensure the key has proper permissions

### Email Not Received

- Check spam/junk folder
- Verify RECIPIENT_EMAIL is correct
- Look for error messages in the console output

## Cost Estimate

- **Anthropic API**: ~$0.10-0.30 per day (based on Claude 3.5 Sonnet pricing)
- **NewsAPI**: Free tier is sufficient (100 requests/day)
- **Gmail**: Free

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use app-specific passwords for Gmail
- The `.gitignore` file protects your credentials

## Future Enhancements

Possible additions:
- More news sources (Reddit, Twitter trends, etc.)
- Category filtering (AI, crypto, healthcare, etc.)
- Sentiment analysis
- Weekly/monthly digest options
- Slack or Discord integration
- Web dashboard for viewing history
- Custom filters based on keywords

## License

MIT License - Feel free to modify and use as you wish!

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review your `.env` configuration
3. Check the console output for error messages
4. Verify all API credentials are valid

---

Built with Claude AI, Python, and lots of coffee! ☕
