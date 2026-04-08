
from google import genai
from google.genai.errors import ServerError
from dotenv import load_dotenv
import os
import time
import requests

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)


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
        return "⚠️ Ollama failed."


# ==============================
# RETRY + FALLBACK FUNCTION
# ==============================
def generate_with_retry(prompt, retries=3):

    # 🔹 Try Gemini first
    for attempt in range(retries):
        try:
            print("🟢 Using Gemini API")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return {
                "text": response.text,
                "source": "Gemini"
            }

        except ServerError:
            print(f"Retry {attempt+1}... Gemini busy")
            time.sleep(2)

        except Exception as e:
            print("Unexpected error:", e)
            break

    # 🔥 FINAL FALLBACK → OLLAMA
    print("🔵 Switching to Ollama (Local AI)...")

    return {
        "text": run_ollama(prompt),
        "source": "Ollama"
    }


# ==============================
# MAIN FUNCTION
# ==============================
def create_plan(topic):

    if not topic or topic.strip() == "":
        return {
            "text": "⚠️ Please enter a valid research topic.",
            "source": "None"
        }

    prompt = f"""
    Break the following research topic into 5 clear and logical research tasks.

    Topic: {topic}

    Instructions:
    - Return exactly 5 tasks
    - Use numbered format (1 to 5)
    - Keep tasks clear and specific
    """

    return generate_with_retry(prompt)

