import requests

def search_wikipedia(query):
    try:
        query = query.replace(" ", "_")

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return ""

        data = response.json()

        return data.get("extract", "")

    except Exception as e:
        print("Wiki error:", e)
        return ""