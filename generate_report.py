
from google import genai
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

# ==============================
# GEMINI CLIENT
# ==============================
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ==============================
# OLLAMA FUNCTION (LOCAL AI)
# ==============================
def run_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    except Exception as e:
        print("Ollama error:", e)
        return "⚠️ Report generation failed (Ollama error)."


# ==============================
# RETRY + FALLBACK FUNCTION
# ==============================
def generate_with_retry(prompt, retries=3):

    # 🔹 Try Gemini first
    for attempt in range(retries):
        try:
            print("🟢 Using Gemini for report")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"temperature": 0.3}
            )
            return response.text

        except Exception:
            print(f"Retry {attempt+1}... Gemini busy")
            time.sleep(2)

    # 🔥 FALLBACK → OLLAMA
    print("🔵 Switching to Ollama for report")

    return run_ollama(prompt)


# ==============================
# MAIN REPORT FUNCTION
# ==============================
def generate_report(topic, research_data):

    try:
        # Limit data (avoid overload)
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

Write a detailed, well-structured research report using ONLY the research data provided.

Important Rules:
- Do NOT invent information.
- Use only the provided research data.
- If the research data is insufficient, clearly state that.
- Cite sources using numbers like [1], [2], [3].
- Every important statistic or claim must include a citation.
- If multiple sources provide different statistics, explain the difference instead of choosing only one.

Topic:
{topic}

Research Data:
{combined_text}

Write the report with the following structure:

1. Executive Summary  
2. Key Findings  
3. Detailed Analysis  
4. Challenges & Risks  
5. Future Outlook  
6. Sources

In the Sources section list all sources with their citation numbers.
"""

        return generate_with_retry(prompt)

    except Exception as e:
        print("🔥 Report Error:", e)
        return "⚠️ Report generation failed."

