from agents.planner_agent import create_plan
from agents.search_agent import search_web
from agents.reader_agent import read_page
from agents.query_agent import generate_queries

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import time


# Block low-quality sites
blocked_domains = [
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "tiktok.com",
    "snapchat.com",
    "pinterest.com",

    "reddit.com",
    "quora.com",

    "youtube.com",
    "vimeo.com",

    "fandom.com",
    "wikihow.com",

    "tumblr.com",
    "weebly.com",
    "wixsite.com"
]


def is_valid_source(url):

    domain = urlparse(url).netloc.lower()

    for blocked in blocked_domains:
        if blocked in domain:
            print("Blocked source:", url)
            return False

    return True


def process_task(task):

    research_data = []

    if not task.strip():
        return []

    print("\nProcessing task:", task)

    queries = generate_queries(task)

    urls = []

    for q in queries:

        print("Searching for:", q)

        try:

            results = search_web(q)

            urls.extend(results)

            # small delay to avoid Tavily rate limit
            time.sleep(1)

        except Exception as e:

            print("Search failed:", e)

    # remove duplicate URLs
    urls = list(set(urls))

    # filter bad domains
    urls = [u for u in urls if is_valid_source(u)]

    for url in urls:

        print("Reading:", url)

        try:

            text = read_page(url)

            if text and len(text) > 200:

                research_data.append({
                    "source": url,
                    "content": text[:4000]
                })

                print("Collected text length:", len(text))

        except Exception as e:

            print("Failed to read:", url)

    return research_data


def run_research(topic):

    print("\nStarting research on:", topic)

    print("\nCreating research plan...\n")

    plan = create_plan(topic)

    print(plan)

    # clean tasks (remove empty lines)
    tasks = [t.strip() for t in plan.split("\n") if t.strip()]

    all_research = []

    with ThreadPoolExecutor(max_workers=3) as executor:

        results = executor.map(process_task, tasks)

    for r in results:

        all_research.extend(r)

    return all_research