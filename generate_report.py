from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_report(topic, research_data):

    # limit chunks to avoid context overload
    research_data = research_data[:12]

    combined_text = ""
    sources = {}
    source_list = []

    for item in research_data:

        source = item["source"]
        content = item["content"]

        if source not in sources:
            sources[source] = len(sources) + 1
            source_list.append(source)

        source_id = sources[source]

        combined_text += f"\n[Source {source_id}: {source}]\n{content}\n"

    prompt = f"""
You are a professional research analyst.

Write a detailed research report using ONLY the research data provided.

Rules:
- Do NOT invent information.
- If the research data is insufficient, state that clearly.
- Cite sources using numbers like [1], [2], [3].
- Every major claim must reference a source.

Topic:
{topic}

Research Data:
{combined_text}

Structure the report with these sections:

1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Challenges & Risks
5. Future Outlook
6. Sources

In the Sources section list all sources with their numbers.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.3}
    )

    return response.text