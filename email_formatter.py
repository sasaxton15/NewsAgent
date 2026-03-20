"""Format news digest as HTML email."""
import re
from datetime import datetime
from typing import Dict, List


class EmailFormatter:
    """Formats news stories into a clean newsletter-style HTML email."""

    @staticmethod
    def _format_summary_html(summary: str) -> str:
        """Style the 'Why it matters:' portion of a summary differently."""
        parts = re.split(r'(Why it matters:)', summary, flags=re.IGNORECASE, maxsplit=1)
        if len(parts) == 3:
            return (
                f'<span style="color: #2d3436;">{parts[0]}</span>'
                f'<span style="color: #636e72; font-style: italic;">'
                f'<strong style="font-style: normal;">{parts[1]}</strong>{parts[2]}</span>'
            )
        return summary

    @staticmethod
    def format_digest(
        summarized: Dict[str, List[Dict]],
        daily_brief: str,
        category_config: dict,
    ) -> str:
        today = datetime.now().strftime("%B %d, %Y")

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #2d3436;
            max-width: 620px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f2f5;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}
        .header {{
            border-bottom: 3px solid #2d3436;
            padding-bottom: 20px;
            margin-bottom: 28px;
        }}
        .newsletter-name {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #b2bec3;
            margin-bottom: 8px;
        }}
        h1 {{
            color: #2d3436;
            margin: 0 0 4px 0;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        .date {{
            color: #b2bec3;
            font-size: 13px;
            font-weight: 500;
        }}
        .brief-box {{
            background-color: #f8f9fa;
            border-left: 4px solid #2d3436;
            padding: 18px 22px;
            margin-bottom: 36px;
            border-radius: 0 6px 6px 0;
        }}
        .brief-label {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #b2bec3;
            margin-bottom: 10px;
        }}
        .brief-text {{
            font-size: 15px;
            color: #2d3436;
            line-height: 1.7;
            margin: 0;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-header {{
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 17px;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0.3px;
            color: #2d3436;
        }}
        .story {{
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid #f0f2f5;
        }}
        .story:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .source-tag {{
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #b2bec3;
            margin-bottom: 6px;
        }}
        .story-title {{
            font-size: 16px;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 8px;
        }}
        .story-title a {{
            color: #2d3436;
            text-decoration: none;
        }}
        .story-title a:hover {{
            text-decoration: underline;
        }}
        .summary {{
            font-size: 14px;
            line-height: 1.75;
            color: #636e72;
            margin: 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #f0f2f5;
            text-align: center;
            color: #b2bec3;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="newsletter-name">The Brief</div>
            <h1>Your Daily Digest</h1>
            <div class="date">{today}</div>
        </div>
"""

        if daily_brief:
            html += f"""
        <div class="brief-box">
            <div class="brief-label">Today at a Glance</div>
            <p class="brief-text">{daily_brief}</p>
        </div>
"""

        for cat, stories in summarized.items():
            if not stories:
                continue
            cfg = category_config.get(cat, {'label': cat.title(), 'emoji': '', 'color': '#2d3436'})
            color = cfg['color']

            html += f"""
        <div class="section">
            <div class="section-header" style="border-bottom: 3px solid {color};">
                <h2 class="section-title">{cfg['emoji']} {cfg['label']}</h2>
            </div>
"""
            for story in stories:
                formatted_summary = EmailFormatter._format_summary_html(story['summary'])
                html += f"""
            <div class="story">
                <div class="source-tag">{story['source']}</div>
                <div class="story-title">
                    <a href="{story['url']}" target="_blank">{story['title']}</a>
                </div>
                <p class="summary">{formatted_summary}</p>
            </div>"""

            html += "\n        </div>\n"

        html += """
        <div class="footer">
            The Brief &mdash; Powered by NewsAgent &amp; Claude AI
        </div>
    </div>
</body>
</html>"""

        return html

    @staticmethod
    def format_plain_text(summarized: Dict[str, List[Dict]], category_config: dict) -> str:
        today = datetime.now().strftime("%B %d, %Y")
        text = f"THE BRIEF -- YOUR DAILY DIGEST\n{today}\n"
        text += "=" * 60 + "\n\n"

        for cat, stories in summarized.items():
            if not stories:
                continue
            cfg = category_config.get(cat, {'label': cat.title(), 'emoji': ''})
            text += f"{cfg['emoji']} {cfg['label'].upper()}\n"
            text += "-" * 60 + "\n\n"
            for i, story in enumerate(stories, 1):
                text += f"{i}. {story['title']}\n"
                text += f"   Source: {story['source']}\n"
                text += f"   {story['summary']}\n"
                text += f"   Read more: {story['url']}\n\n"
            text += "\n"

        text += "=" * 60 + "\n"
        text += "The Brief -- Powered by NewsAgent & Claude AI\n"
        return text
