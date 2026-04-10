from google import genai
from dotenv import load_dotenv
import os
import time
import requests
from memory_db import store_memory

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
# MAIN REPORT FUNCTION (UPDATED)
# ==============================
def generate_report(topic, research_data, memory_context):

    try:
        # -----------------------------
        # LIMIT DATA (avoid overload)
        # -----------------------------
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

        # -----------------------------
        # PROMPT (RAG ENABLED)
        # -----------------------------
        prompt = f"""
You are a professional research analyst.

Use BOTH:
1. Relevant previous knowledge (memory)
2. New research data

Important Rules:
- Do NOT invent information.
- Prefer NEW research data.
- Use memory only when relevant.
- Cite sources using numbers like [1], [2], [3].
- Every important claim must include a citation.

Topic:
{topic}

Relevant Previous Knowledge:
{memory_context}

New Research Data:
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

        # -----------------------------
        # GENERATE REPORT
        # -----------------------------
        final_report = generate_with_retry(prompt)

        # -----------------------------
        # STORE IN MEMORY (RAG)
        # -----------------------------
        store_memory(topic, final_report)

        return final_report

    except Exception as e:
        print("🔥 Report Error:", e)
        return "⚠️ Report generation failed."