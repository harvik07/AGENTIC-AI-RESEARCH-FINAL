from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query, max_results=3):

    print("Searching for:", query)

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )

    urls = []

    for r in response["results"]:
        urls.append(r["url"])

    return urls