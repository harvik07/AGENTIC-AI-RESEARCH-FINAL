from google import genai
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

# read API key
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def create_plan(topic):

    prompt = f"""
    Break the following research topic into 5 research tasks.

    Topic: {topic}

    Return the tasks as a numbered list.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text