# C – Gemini Integration (Applied Intelligence Task)

**Total Marks: 30**

## Q1. Gemini Integration and Intelligent Summarization

Use Google Gemini 2.5 Flash API in Python to analyze and summarize information from a live webpage.

Perform the following steps:
- Connect to Gemini 2.5 Flash using the official SDK or REST API.
- Automatically fetch webpage data (no manual copy-paste) from one of the following sources:
  - https://en.wikipedia.org/wiki/Artificial_intelligence
  - https://www.bbc.com/news/technology
  - https://edition.cnn.com/business
- Clean the HTML — remove scripts, navigation, and irrelevant text.
- Send the cleaned text to Gemini using a custom prompt that you create.
- The prompt must instruct Gemini to summarize and provide a short analytical insight (not just paraphrase).
- Print the result in the required console format.

## Q2. What Your Script Must Do

Your script must:
- Fetch and clean webpage content automatically.
- Pass the cleaned content to Gemini 2.5 Flash with your custom prompt.
- Ask Gemini to:
  - Summarize the content in 3–5 bullet points.
  - Add one short insight that interprets the overall theme or trend.
- Display output exactly in the following structure:

  ```
  Summary:
  • <point 1>
  • <point 2>
  • <point 3>
  • <point 4>
  • <point 5>

  Insight:
  <single-line insight>
  ```

- Save both parts (summary + insight) into a file named `summary_output.txt`.

## Q3. Prompt Design and Reasoning Quality

- Write a creative, clear, and well-structured prompt that tells Gemini exactly what to produce.
- The prompt should specify the tone, structure, and focus area (e.g., technology, ethics, or business impact).
- Avoid generic instructions like "Summarize this text."
- Include an explicit request for an insight line after the summary.

Example concept (do not copy):

> "Analyze the following webpage content and summarize it into 4 concise bullet points focusing on emerging AI trends, followed by one line that explains what these trends suggest about the future of technology."

## Response Format (Example Output for Reference)

```
Summary:
• AI is increasingly used across healthcare, finance, and education.
• Ethical and policy concerns around AI governance are growing.
• Major tech companies are investing in responsible AI development.
• Transparency and public trust remain critical focus areas.

Insight:
The article indicates that AI is shifting from rapid innovation to responsible regulation and long-term governance.
```

## Deliverables

- `tripgain_gemini_analysis.py` → Python script implementing Gemini integration
- `summary_output.txt` → Saved summary and insight output
- Console output must match the exact response format shown above
