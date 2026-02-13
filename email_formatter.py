"""Format news digest as HTML email."""
from datetime import datetime
from typing import List, Dict


class EmailFormatter:
    """Formats news stories into a clean HTML email."""

    @staticmethod
    def format_digest(tech_stories: List[Dict], finance_stories: List[Dict]) -> str:
        """
        Create a beautifully formatted HTML email digest.
        """
        today = datetime.now().strftime("%B %d, %Y")

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #2c3e50;
            margin: 0 0 5px 0;
            font-size: 28px;
        }}
        .date {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-title {{
            color: #2c3e50;
            font-size: 22px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }}
        .story {{
            margin-bottom: 25px;
            padding-bottom: 25px;
            border-bottom: 1px solid #ecf0f1;
        }}
        .story:last-child {{
            border-bottom: none;
        }}
        .story-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .story-title a {{
            color: #2c3e50;
            text-decoration: none;
        }}
        .story-title a:hover {{
            color: #3498db;
        }}
        .source {{
            color: #7f8c8d;
            font-size: 13px;
            margin-bottom: 10px;
        }}
        .summary {{
            color: #555;
            font-size: 15px;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #95a5a6;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 Daily News Digest</h1>
            <div class="date">{today}</div>
        </div>
"""

        # Tech section
        if tech_stories:
            html += """
        <div class="section">
            <h2 class="section-title">💻 Technology</h2>
"""
            for story in tech_stories:
                html += f"""
            <div class="story">
                <div class="story-title">
                    <a href="{story['url']}" target="_blank">{story['title']}</a>
                </div>
                <div class="source">Source: {story['source']}</div>
                <div class="summary">{story['summary']}</div>
            </div>
"""
            html += """
        </div>
"""

        # Finance section
        if finance_stories:
            html += """
        <div class="section">
            <h2 class="section-title">💰 Finance & Business</h2>
"""
            for story in finance_stories:
                html += f"""
            <div class="story">
                <div class="story-title">
                    <a href="{story['url']}" target="_blank">{story['title']}</a>
                </div>
                <div class="source">Source: {story['source']}</div>
                <div class="summary">{story['summary']}</div>
            </div>
"""
            html += """
        </div>
"""

        html += """
        <div class="footer">
            Powered by NewsAgent | Daily automated digest
        </div>
    </div>
</body>
</html>
"""
        return html

    @staticmethod
    def format_plain_text(tech_stories: List[Dict], finance_stories: List[Dict]) -> str:
        """
        Create a plain text version of the digest as fallback.
        """
        today = datetime.now().strftime("%B %d, %Y")

        text = f"DAILY NEWS DIGEST - {today}\n"
        text += "=" * 60 + "\n\n"

        if tech_stories:
            text += "TECHNOLOGY\n"
            text += "-" * 60 + "\n\n"
            for i, story in enumerate(tech_stories, 1):
                text += f"{i}. {story['title']}\n"
                text += f"   Source: {story['source']}\n"
                text += f"   {story['summary']}\n"
                text += f"   Read more: {story['url']}\n\n"

        if finance_stories:
            text += "\nFINANCE & BUSINESS\n"
            text += "-" * 60 + "\n\n"
            for i, story in enumerate(finance_stories, 1):
                text += f"{i}. {story['title']}\n"
                text += f"   Source: {story['source']}\n"
                text += f"   {story['summary']}\n"
                text += f"   Read more: {story['url']}\n\n"

        text += "\n" + "=" * 60 + "\n"
        text += "Powered by NewsAgent | Daily automated digest\n"

        return text
