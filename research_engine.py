from agents.planner_agent import create_plan
from agents.search_agent import search_web
from agents.reader_agent import read_page
from agents.query_agent import generate_queries

from memory_db import search_memory  # 🧠 RAG Memory

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import time


# -----------------------------
# BLOCK LOW-QUALITY SOURCES
# -----------------------------
blocked_domains = [
    "facebook.com", "instagram.com", "twitter.com", "x.com",
    "tiktok.com", "snapchat.com", "pinterest.com",
    "reddit.com", "quora.com",
    "youtube.com", "vimeo.com",
    "fandom.com", "wikihow.com",
    "tumblr.com", "weebly.com", "wixsite.com"
]


def is_valid_source(url):
    domain = urlparse(url).netloc.lower()

    for blocked in blocked_domains:
        if blocked in domain:
            print("Blocked source:", url)
            return False

    return True


# -----------------------------
# PROCESS SINGLE TASK
# -----------------------------
def process_task(task):

    research_data = []

    try:
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
                time.sleep(1)  # avoid rate limit

            except Exception as e:
                print("Search failed:", e)

        # remove duplicates
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

            except Exception:
                print("Failed to read:", url)

        return research_data

    except Exception as e:
        print("Task failed:", e)
        return []


# -----------------------------
# MAIN RESEARCH PIPELINE (RAG ENABLED)
# -----------------------------
def run_research(topic):

    try:
        print("\nStarting research on:", topic)

        # -----------------------------
        # 🧠 RAG MEMORY RETRIEVAL
        # -----------------------------
        memory_context = search_memory(topic)

        if memory_context:
            print("\n🧠 Using relevant memory chunks...\n")

        print("\nCreating research plan...\n")

        # -----------------------------
        # ENHANCED TOPIC WITH MEMORY
        # -----------------------------
        enhanced_topic = f"""
Previous relevant knowledge:
{memory_context}

Current topic:
{topic}
"""

        result = create_plan(enhanced_topic)

        plan = result["text"]
        source = result["source"]

        print("📌 Plan generated using:", source)
        print(plan)

        # ❗ HANDLE FAILURE
        if not plan or "⚠️" in plan:
            return {
                "research": [],
                "memory": memory_context,
                "error": "⚠️ Failed to generate research plan."
            }

        # clean tasks
        tasks = [t.strip() for t in plan.split("\n") if t.strip()]

        if not tasks:
            return {
                "research": [],
                "memory": memory_context,
                "error": "⚠️ No valid research tasks generated."
            }

        all_research = []

        # -----------------------------
        # PARALLEL PROCESSING
        # -----------------------------
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(process_task, tasks))

        for r in results:
            all_research.extend(r)

        # ❗ HANDLE EMPTY OUTPUT
        if not all_research:
            return {
                "research": [],
                "memory": memory_context,
                "error": "⚠️ No useful research data found."
            }

        # -----------------------------
        # FINAL OUTPUT
        # -----------------------------
        return {
            "research": all_research,
            "memory": memory_context,
            "error": None
        }

    except Exception as e:
        print("🔥 Research Engine Error:", e)
        return {
            "research": [],
            "memory": "",
            "error": "⚠️ Research process failed."
        }