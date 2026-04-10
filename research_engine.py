from agents.planner_agent import create_plan
from agents.search_agent import search_web
from agents.reader_agent import read_page
from agents.query_agent import generate_queries

from memory_db import search_memory

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import time

from agents.wiki_tool import search_wikipedia
from agents.arxiv_tool import search_arxiv


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
            print("🚫 Blocked source:", url)
            return False

    return True


# -----------------------------
# PROCESS SINGLE TASK (TAVILY)
# -----------------------------
def process_task(task):

    research_data = []

    try:
        if not task.strip():
            return []

        print("\n🌐 Using Tavily Web Search...")
        print("Processing task:", task)

        queries = generate_queries(task)
        urls = []

        for q in queries:
            print("🔎 Searching for:", q)

            try:
                results = search_web(q)
                urls.extend(results)
                time.sleep(1)

            except Exception as e:
                print("Search failed:", e)

        urls = list(set(urls))
        urls = [u for u in urls if is_valid_source(u)]

        for url in urls:
            print("📖 Reading:", url)

            try:
                text = read_page(url)

                if text and len(text) > 200:
                    research_data.append({
                        "source": url,
                        "type": "Web",
                        "content": text[:4000]
                    })

            except Exception:
                print("Failed to read:", url)

        return research_data

    except Exception as e:
        print("Task failed:", e)
        return []


# -----------------------------
# MAIN RESEARCH PIPELINE
# -----------------------------
def run_research(topic):

    try:
        print("\n🚀 Starting research on:", topic)

        # -----------------------------
        # 🧠 MEMORY
        # -----------------------------
        memory_context = search_memory(topic)

        if isinstance(memory_context, list) and memory_context:
            memory_context = "\n".join(memory_context[0])
            print("\n🧠 Using previous memory...\n")
        else:
            memory_context = ""

        # -----------------------------
        # 📚 WIKIPEDIA TOOL
        # -----------------------------
        print("\n📚 Using Wikipedia...")
        wiki_data = search_wikipedia(topic)

        wiki_result = []
        if wiki_data:
            print("✅ Wikipedia data added")
            wiki_result.append({
                "source": "Wikipedia",
                "type": "Wiki",
                "content": wiki_data[:2000]
            })
        else:
            print("⚠️ Wikipedia not found")

        # -----------------------------
        # 📄 ARXIV TOOL
        # -----------------------------
        print("\n📄 Using Arxiv...")
        arxiv_data = search_arxiv(topic)

        arxiv_result = []
        if arxiv_data:
            print("✅ Arxiv data added")
            for paper in arxiv_data:
                arxiv_result.append({
                    "source": "Arxiv",
                    "type": "Research Paper",
                    "content": paper[:2000]
                })
        else:
            print("⚠️ No Arxiv papers found")

        # -----------------------------
        # CREATE PLAN
        # -----------------------------
        print("\n🧠 Creating research plan...\n")

        enhanced_topic = f"""
Previous knowledge:
{memory_context}

Current topic:
{topic}
"""

        result = create_plan(enhanced_topic)

        plan = result["text"]
        source = result["source"]

        print("📌 Plan generated using:", source)
        print(plan)

        if not plan or "⚠️" in plan:
            return {
                "research": [],
                "memory": memory_context,
                "error": "⚠️ Failed to generate research plan."
            }

        tasks = [t.strip() for t in plan.split("\n") if t.strip()]

        if not tasks:
            return {
                "research": [],
                "memory": memory_context,
                "error": "⚠️ No valid research tasks generated."
            }

        # -----------------------------
        # COMBINE ALL DATA
        # -----------------------------
        all_research = []

        # Add tools first
        all_research.extend(wiki_result)
        all_research.extend(arxiv_result)

        # -----------------------------
        # PARALLEL WEB SEARCH
        # -----------------------------
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(process_task, tasks))

        for r in results:
            all_research.extend(r)

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