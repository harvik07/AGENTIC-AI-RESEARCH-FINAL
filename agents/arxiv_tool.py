import requests
import xml.etree.ElementTree as ET

def search_arxiv(query):
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=2"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)

        results = []

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title")
            summary = entry.find("{http://www.w3.org/2005/Atom}summary")

            if title is not None and summary is not None:
                text = f"{title.text}\n{summary.text}"
                results.append(text)

        return results

    except Exception as e:
        print("Arxiv error:", e)
        return []