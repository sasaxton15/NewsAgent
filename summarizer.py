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
                    model="claude-haiku-4-5-20251001",
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

    def rank_and_select_stories(self, all_stories: Dict[str, List[Dict]], num_per_category: int) -> Dict[str, List[Dict]]:
        """Use Claude to rank stories by importance and select top N from each category."""
        category_priorities = {
            'ai': 'Model releases, agent frameworks, AI product launches, developer tools, AI policy shifts',
            'finance': 'Market-moving events, earnings surprises, interest rate changes, macro trends, personal finance insights',
            'industry': 'Major business strategy shifts, executive moves, M&A, industry disruption, regulatory changes',
            'marketing': 'Brand campaigns, platform algorithm changes, consumer behavior shifts, ad industry news, martech launches',
        }

        sections = []
        response_format_lines = []
        for category, stories in all_stories.items():
            if not stories:
                continue
            titles = "\n".join([
                f"{i+1}. {s['title']} (from {s['source']})"
                for i, s in enumerate(stories[:20])
            ])
            sections.append(f"{category.upper()} STORIES:\n{titles}")
            response_format_lines.append(f"{category.upper()}: 1,2,3")

        priority_lines = "\n".join([
            f"- {cat.upper()}: {desc}"
            for cat, desc in category_priorities.items()
            if cat in all_stories
        ])

        prompt = f"""You are a news curator for a professional daily digest covering AI, finance, business, and marketing.

{chr(10).join(sections)}

Select the {num_per_category} most important stories from each category.

Prioritize by category:
{priority_lines}

Respond in this exact format (comma-separated story numbers only):
{chr(10).join(response_format_lines)}"""

        try:
            result_text = self._create_message_with_retry(prompt, max_tokens=300)
            selected = {cat: [] for cat in all_stories}

            for line in result_text.strip().split('\n'):
                for cat in all_stories:
                    if line.upper().startswith(f"{cat.upper()}:"):
                        nums = [int(n) - 1 for n in re.findall(r"\d+", line)]
                        selected[cat] = [all_stories[cat][i] for i in nums if i < len(all_stories[cat])]
                        break

            # Fallback for any category Claude missed
            for cat in all_stories:
                if not selected[cat]:
                    selected[cat] = all_stories[cat][:num_per_category]

            return selected

        except Exception as e:
            print(f"Error ranking stories: {e}")
            return {cat: stories[:num_per_category] for cat, stories in all_stories.items()}

    def generate_subject_line(self, summarized: Dict[str, List[Dict]]) -> str:
        """Generate a punchy subject line from the two most important story titles."""
        top_titles = []
        for cat in ['ai', 'finance', 'industry', 'marketing']:
            if cat in summarized and summarized[cat]:
                top_titles.append(summarized[cat][0]['title'])
            if len(top_titles) == 2:
                break

        if not top_titles:
            return ""

        titles_text = "\n".join(top_titles)
        prompt = f"""Create a punchy email subject line for a daily news digest. Compress the 2 headlines below into ~5 words each, joined with " + ". No date. No quotes.

Headlines:
{titles_text}

Write only the subject line. Example: "OpenAI releases agents SDK + Fed holds rates steady" """

        try:
            return self._create_message_with_retry(prompt, max_tokens=60).strip().strip('"')
        except Exception as e:
            print(f"Error generating subject line: {e}")
            return ""

    def generate_daily_brief(self, summarized: Dict[str, List[Dict]]) -> str:
        """Generate a 2-sentence overview of the day's most important themes."""
        all_titles = []
        for cat, stories in summarized.items():
            for s in stories:
                all_titles.append(f"[{cat.upper()}] {s['title']}")

        titles_text = "\n".join(all_titles)

        prompt = f"""Based on these headlines from today's news digest, write exactly 2 sentences summarizing the most important themes and what they signal for the day ahead. Be specific and direct — name the actual topics, companies, or trends.

Headlines:
{titles_text}

Write only the 2-sentence brief, nothing else."""

        try:
            return self._create_message_with_retry(prompt, max_tokens=150).strip()
        except Exception as e:
            print(f"Error generating daily brief: {e}")
            return ""

    def summarize_article(self, title: str, content: str, url: str) -> str:
        """Summarize a single article in 2 sentences + a 'Why it matters' line."""
        prompt = f"""Summarize this news article in exactly 2 clear sentences covering the key facts. Then add one sentence starting with exactly "Why it matters:" explaining the real-world significance.

Title: {title}

Content: {content}

Provide only the 3-sentence summary, no additional commentary."""

        try:
            return self._create_message_with_retry(prompt, max_tokens=200).strip()
        except Exception as e:
            print(f"Error summarizing article '{title}': {e}")
            return "Unable to generate summary for this article."

    def summarize_stories(self, stories: List[Dict], fetcher) -> List[Dict]:
        """Summarize a list of stories."""
        summarized_stories = []

        for story in stories:
            print(f"Summarizing: {story['title']}")

            content = fetcher.extract_article_content(story['url'])

            if not content:
                content = story.get('summary', story.get('text', ''))
            if not content:
                content = "No additional content available."

            summary = self.summarize_article(story['title'], content, story['url'])

            summarized_stories.append({
                'title': story['title'],
                'url': story['url'],
                'source': story['source'],
                'summary': summary,
            })

        return summarized_stories
