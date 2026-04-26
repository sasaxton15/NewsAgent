"""Format news digest as HTML email."""
import re
from datetime import datetime
from typing import Dict, List


class EmailFormatter:
    """Formats news stories into a TLDR-inspired newsletter email."""

    @staticmethod
    def _split_summary(summary: str):
        """Split summary into facts and 'Why it matters' parts."""
        parts = re.split(r'(Why it matters:)', summary, flags=re.IGNORECASE, maxsplit=1)
        if len(parts) == 3:
            return parts[0].strip(), parts[2].strip()
        return summary.strip(), None

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
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f0f2f5;
            color: #1a1a1a;
            padding: 24px 16px;
        }}
        .container {{
            background: #ffffff;
            border-radius: 12px;
            max-width: 600px;
            margin: 0 auto;
            overflow: hidden;
            box-shadow: 0 1px 8px rgba(0,0,0,0.07);
        }}
        .header {{
            padding: 32px 36px 24px;
            border-bottom: 1px solid #ebebeb;
        }}
        .masthead {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #aaa;
            margin-bottom: 10px;
        }}
        .headline {{
            font-size: 26px;
            font-weight: 800;
            color: #1a1a1a;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }}
        .dateline {{
            font-size: 13px;
            color: #aaa;
        }}
        .brief-box {{
            margin: 24px 36px;
            padding: 16px 20px;
            background: #f7f7f7;
            border-left: 3px solid #1a1a1a;
            border-radius: 0 6px 6px 0;
        }}
        .brief-label {{
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: #aaa;
            margin-bottom: 8px;
        }}
        .brief-text {{
            font-size: 14px;
            line-height: 1.65;
            color: #333;
        }}
        .section {{
            padding: 0 36px;
            margin-bottom: 8px;
        }}
        .section-label {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 16px 0 12px;
            border-bottom: 2px solid #ebebeb;
            margin-bottom: 4px;
        }}
        .section-label-bar {{
            display: inline-block;
            width: 3px;
            height: 16px;
            border-radius: 2px;
        }}
        .section-label-text {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #555;
        }}
        .story {{
            padding: 18px 0;
            border-bottom: 1px solid #f2f2f2;
        }}
        .story:last-child {{
            border-bottom: none;
        }}
        .story-source {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #bbb;
            margin-bottom: 5px;
        }}
        .story-title {{
            font-size: 15px;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 8px;
        }}
        .story-title a {{
            color: #1a1a1a;
            text-decoration: none;
        }}
        .story-title a:hover {{
            text-decoration: underline;
        }}
        .story-summary {{
            font-size: 13px;
            line-height: 1.7;
            color: #555;
            margin-bottom: 10px;
        }}
        .why-it-matters {{
            font-size: 13px;
            line-height: 1.65;
            color: #555;
            border-left: 2px solid #ddd;
            padding: 6px 12px;
            margin-bottom: 10px;
            font-style: italic;
        }}
        .why-label {{
            font-style: normal;
            font-weight: 700;
            color: #888;
        }}
        .read-more {{
            display: inline-block;
            font-size: 12px;
            font-weight: 600;
            color: #888;
            text-decoration: none;
        }}
        .read-more:hover {{
            color: #333;
        }}
        .jump-links {{
            padding: 12px 36px;
            border-bottom: 1px solid #ebebeb;
            font-size: 11px;
            color: #aaa;
            text-align: center;
        }}
        .jump-links a {{
            color: #888;
            text-decoration: none;
            font-weight: 600;
            margin: 0 6px;
        }}
        .jump-links a:hover {{
            color: #333;
        }}
        .footer {{
            padding: 24px 36px;
            border-top: 1px solid #ebebeb;
            text-align: center;
            font-size: 11px;
            color: #bbb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="masthead">The Brief</div>
            <div class="headline">Your Daily Digest</div>
            <div class="dateline">{today}</div>
        </div>
"""

        if daily_brief:
            html += f"""
        <div class="brief-box">
            <div class="brief-label">Today at a Glance</div>
            <div class="brief-text">{daily_brief}</div>
        </div>
"""

        active_cats = [cat for cat, stories in summarized.items() if stories]
        if len(active_cats) > 1:
            links = " &middot; ".join(
                f'<a href="#{cat}">{category_config.get(cat, {}).get("label", cat.title())}</a>'
                for cat in active_cats
            )
            html += f'\n        <div class="jump-links">Jump to: {links}</div>\n'

        for cat, stories in summarized.items():
            if not stories:
                continue
            cfg = category_config.get(cat, {'label': cat.title(), 'emoji': '', 'color': '#888'})
            color = cfg['color']

            html += f"""
        <div class="section" id="{cat}">
            <div class="section-label">
                <span class="section-label-bar" style="background:{color};"></span>
                <span class="section-label-text">{cfg['emoji']} {cfg['label']}</span>
            </div>
"""
            for story in stories:
                facts, why = EmailFormatter._split_summary(story['summary'])

                why_block = ""
                if why:
                    why_block = f"""
                <div class="why-it-matters">
                    <span class="why-label">Why it matters:</span> {why}
                </div>"""

                html += f"""
            <div class="story">
                <div class="story-source">{story['source']}</div>
                <div class="story-title">
                    <a href="{story['url']}" target="_blank">{story['title']}</a>
                </div>
                <div class="story-summary">{facts}</div>{why_block}
                <a class="read-more" href="{story['url']}" target="_blank">Read more &rarr;</a>
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
