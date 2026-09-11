# Step-by-Step Instructions: Gemini Integration Exercise

These steps walk through building and running `tripgain_gemini_analysis.py`, which
fetches a live webpage, cleans it, sends it to Gemini 2.5 Flash with a custom prompt,
and prints/saves a summary + insight in the required format.

> `tripgain_gemini_analysis.py` already exists in this project and implements steps 4–9
> below (fetch, clean, prompt, call Gemini, format, save). Steps 1–2 and 10 are the
> manual actions you still need to run yourself.

## 1. Get a Gemini API key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and sign in.
2. Click **Create API key** and copy it.
3. Store it as an environment variable instead of hardcoding it:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```
   (Add this line to your `~/.zshrc` if you want it to persist across terminal sessions.)

## 2. Set up the project environment

1. Create and activate a virtual environment:
   ```bash
   cd /Users/somashekhar/Desktop/soma/projects/GeminiIntegration
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the required packages:
   ```bash
   pip install google-genai requests beautifulsoup4
   ```

## 3. Pick a source URL

Choose one of the three allowed sources:
- `https://en.wikipedia.org/wiki/Artificial_intelligence` (default in the script)
- `https://www.bbc.com/news/technology`
- `https://edition.cnn.com/business`

Wikipedia is the most reliable to scrape (stable HTML structure, no heavy JS/paywall),
so it's the script's default. To target a different source, pass `--url`:
```bash
python tripgain_gemini_analysis.py --url https://www.bbc.com/news/technology
```
BBC's response is gzip-compressed; if you ever fetch it manually with `curl` instead of
the script, remember to add `--compressed -L` or you'll get an empty/garbled file.

## 4. Fetch the webpage automatically

Implemented in `tripgain_gemini_analysis.py` as `fetch_html(url)`:
- Uses `requests.get(url, headers={"User-Agent": "..."})` to download the raw HTML.
- Sets a 15s timeout and calls `response.raise_for_status()` to fail loudly on errors.
- Runs automatically each time the script is executed — no manual copy-paste involved.

## 5. Clean the HTML

Implemented as `clean_html(html)` using `BeautifulSoup`:
1. Parses the HTML with `BeautifulSoup(html, "html.parser")`.
2. Removes irrelevant tags before extracting text: `script`, `style`, `nav`, `header`,
   `footer`, `aside`, `form`, `noscript`.
3. Extracts visible text with `soup.get_text(separator=" ", strip=True)`.
4. Collapses extra whitespace with `" ".join(text.split())`.
5. Truncates to the first `MAX_CHARS` (10,000) characters to stay within prompt size
   limits and keep the request fast.

## 6. The custom prompt

Implemented as `PROMPT_TEMPLATE` / `build_prompt(content)` in the script. It:
- Sets the tone: neutral, analytical, written for "a busy, informed reader".
- Sets the focus: technology, ethical, and business-impact angles.
- Explicitly asks for 3–5 bullet points under a `Summary:` heading.
- Explicitly asks for exactly one interpretive sentence under an `Insight:` heading
  (not a rephrased bullet).
- Locks down the exact output structure so the response is predictable and needs no
  extra parsing.

## 7. Calling the Gemini 2.5 Flash API

Implemented as `call_gemini(prompt)` using the `google-genai` SDK:
```python
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)
result_text = response.text
```
The script reads `GEMINI_API_KEY` from the environment and exits with an error message
if it isn't set — the key is never hardcoded.

## 8. Output format

Because the prompt locks the structure, the script prints `response.text` directly.
Console output looks like:
```
Summary:
• <point 1>
• <point 2>
• <point 3>

Insight:
<single-line insight>
```
(The model may return 3–5 bullets depending on content length; the prompt allows either.)

## 9. Saving the output to a file

The script writes the same text Gemini returned to `summary_output.txt` in the project
directory (`main()` opens the file in write mode and appends a trailing newline).

## 10. Run and test the script end to end

1. Make sure your API key is exported and dependencies are installed (steps 1–2).
2. Run it:
   ```bash
   python tripgain_gemini_analysis.py
   ```
   or against a different source:
   ```bash
   python tripgain_gemini_analysis.py --url https://www.bbc.com/news/technology
   ```
3. Verify:
   - The script fetches the page live (no cached/pasted content) — you'll see
     `Fetching: <url>` printed first.
   - Console output matches the required format exactly.
   - `summary_output.txt` is created in the project directory with the same content.
   - The insight is a genuine interpretation, not a rephrased bullet point.

## 11. Final deliverables checklist

- [ ] `tripgain_gemini_analysis.py` — implements steps 4–9 above.
- [ ] `summary_output.txt` — generated by running the script.
- [ ] Console output matches the exact required format.
- [ ] `GEMINI_API_KEY` is read from an environment variable, never hardcoded in the script.
