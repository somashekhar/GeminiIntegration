"""
Gemini Integration and Intelligent Summarization
-------------------------------------------------
Fetches a live webpage, cleans the HTML, sends the cleaned text to
Gemini 2.5 Flash with a custom prompt, and prints/saves a
Summary + Insight in the required format.

Usage:
    export GEMINI_API_KEY="your-key-here"
    python tripgain_gemini_analysis.py
    python tripgain_gemini_analysis.py --url https://www.bbc.com/news/technology
"""

import argparse
import os
import sys

import requests
from bs4 import BeautifulSoup
from google import genai

ALLOWED_SOURCES = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://www.bbc.com/news/technology",
    "https://edition.cnn.com/business",
]

DEFAULT_URL = ALLOWED_SOURCES[0]
OUTPUT_FILE = "summary_output.txt"
MAX_CHARS = 10000

PROMPT_TEMPLATE = """You are a technology analyst writing for a busy, informed reader.
Read the webpage content below and produce exactly two sections, focusing on
technology, ethical, and business-impact angles. Use a neutral, analytical tone.

1. "Summary": 3 to 5 concise bullet points capturing the key facts.
2. "Insight": exactly one sentence that interprets the broader theme or trend
   implied by the content. This must be an interpretation, not a rephrased bullet.

Respond ONLY in this exact format, with no extra commentary before or after:

Summary:
• <point 1>
• <point 2>
• <point 3>

Insight:
<single-line insight>

Webpage content:
\"\"\"
{content}
\"\"\"
"""


def fetch_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GeminiSummarizer/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    return text[:MAX_CHARS]


def build_prompt(content: str) -> str:
    return PROMPT_TEMPLATE.format(content=content)


def call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    # gemini-2.5-flash is retired for this API key's account tier (Google's API
    # returns a 404 pointing to gemini-3.6-flash as the replacement).
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text.strip()


def main():
    parser = argparse.ArgumentParser(description="Summarize and analyze a live webpage using Gemini 2.5 Flash.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Webpage URL to summarize.")
    args = parser.parse_args()

    print(f"Fetching: {args.url}")
    html = fetch_html(args.url)

    print("Cleaning HTML content...")
    cleaned_text = clean_html(html)

    if not cleaned_text:
        print("Error: no readable text extracted from the page.", file=sys.stderr)
        sys.exit(1)

    print("Sending content to Gemini 2.5 Flash...\n")
    prompt = build_prompt(cleaned_text)
    result = call_gemini(prompt)

    print(result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(result + "\n")

    print(f"\nSaved output to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
