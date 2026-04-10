# 🧠 Agentic AI Research System (Hybrid AI)

A multi-agent AI research system that automatically generates structured research reports using Tavily (web search), Gemini (cloud AI), and Ollama (local AI fallback).

---

# 🚀 Features

## 🤖 Multi-Agent Architecture

* Planner Agent – breaks topic into research tasks
* Search Agent – retrieves relevant URLs using Tavily
* Reader Agent – extracts content from web pages (web scraping)
* Report Generator – creates structured research reports

---

## 🤖 Tool-Based Agent System (NEW 🔥)

👉 The system now uses **multiple intelligent tools** to gather different types of information instead of relying on a single source.

### Tools Used:

* 📚 **Wikipedia** → Basic understanding
* 📄 **Arxiv** → Research papers & academic insights
* 🌐 **Tavily Web Search** → Latest real-world information

### How it works:

* System automatically gathers:

  * Fundamental concepts from Wikipedia
  * Deep research from Arxiv
  * Current data from web search
* Combines all sources into one structured report

### Example:

```
Query: AI in healthcare

→ Wikipedia: basic explanation  
→ Arxiv: research papers  
→ Tavily: latest industry data  
→ Combined into final report
```

### Key Benefits:

* 📚 Better understanding (basic + advanced)
* 🔬 More accurate research
* 🌍 Real-world + academic coverage
* 🤖 True agent-like behavior

---

## 🔍 Source Transparency System (NEW 🚀)

👉 The system clearly shows **which source is being used**

### Example Output:

```
📚 Using Wikipedia...
📄 Using Arxiv...
🌐 Using Tavily Web Search...
```

### Each result includes:

* Source type (Wiki / Research Paper / Web)
* Source link or origin

💥 Makes system more transparent and professional

---

## 🧠 Persistent Memory System

👉 The system includes a local AI memory layer using ChromaDB

### What it does:

* Stores past queries and generated research reports
* Retrieves relevant past knowledge for new queries
* Improves report quality over time
* Reduces repeated web scraping

---

## 🧠 RAG System (Retrieval-Augmented Generation) (NEW 🚀)

👉 The system now uses chunk-based memory retrieval (RAG) for more accurate and efficient responses.

### What it does:

* Splits reports into small chunks (300–500 words)
* Stores each chunk separately in memory
* Retrieves only the most relevant chunks for new queries
* Provides precise and context-aware responses

### How it works:

* Generated reports are split into smaller chunks
* Each chunk is stored in ChromaDB
* When a new query is received:

  * System searches for relevant chunks
  * Only top relevant chunks are retrieved
* These chunks are used along with new research

### Example:

```
Query 1: AI in healthcare
→ Report split into chunks and stored

Query 2: AI diagnosis tools
→ Only diagnosis-related chunks retrieved
→ More accurate report
```

### Key Benefits:

* 🎯 More accurate responses
* ⚡ Faster processing
* 🧠 Context-aware reasoning
* 🔍 Avoids unnecessary data overload

---

## 🌐 Intelligent Web Research

* Powered by Tavily API
* Filters low-quality websites
* Retrieves relevant and high-quality sources

---

## 🕸️ Web Scraping System

* Uses newspaper3k for structured article extraction
* Uses BeautifulSoup fallback for unsupported websites

---

## ⚡ Parallel Processing

* Uses multithreading to speed up research

---

## 🧠 Hybrid AI System

* Uses Gemini API (cloud) for fast and high-quality responses
* Falls back to Ollama (local AI) if API fails

---

## 🔄 Fail-Safe Mechanism

* Retry logic for API failures
* Automatic fallback ensures output is always generated

---

## 📊 Structured Report Generation

* Executive Summary
* Key Findings
* Detailed Analysis
* Challenges & Risks
* Future Outlook
* Sources with citations

---

# 🏗️ Architecture

```
User Input
   ↓
Flask App
   ↓
🧠 RAG Memory Retrieval
   ↓
📚 Wikipedia Tool
📄 Arxiv Tool
🌐 Tavily Web Search
   ↓
Planner Agent
   ↓
Research Engine
   ↓
Report Generator
   ↓
💾 Store as Chunks (RAG)
   ↓
Final Research Report
```

---

# 🛠️ Tech Stack

### Backend:

* Flask (Python)

### AI Models:

* Google Gemini API
* Ollama (Local LLM – phi / tinyllama)

### Search API:

* Tavily API

### Web Scraping:

* newspaper3k
* BeautifulSoup

### Memory System:

* ChromaDB (Persistent Vector Database)

### RAG System:

* Chunk-based storage & retrieval
* Context-aware memory usage

### Tools System (NEW):

* Wikipedia API
* Arxiv API

### Libraries:

* requests
* concurrent.futures
* python-dotenv

### Other:

* Multithreading
* Git & GitHub

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repository

```bash
git clone https://github.com/harvik07/AGENTIC-AI-RESEARCH-FINAL.git
cd AGENTIC-AI-RESEARCH-FINAL
```

## 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Add API Keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
```

## 4️⃣ Install Ollama

Download: 👉 [https://ollama.com](https://ollama.com)

Run:

```bash
ollama run phi
```

## 5️⃣ Run the application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# 🧪 How It Works

1. User enters a research topic
2. 🧠 System retrieves relevant chunks using RAG
3. 📚 Wikipedia provides base knowledge
4. 📄 Arxiv provides research papers
5. 🌐 Tavily fetches latest web data
6. Planner agent creates research tasks
7. Reader agent extracts content
8. AI generates structured report
9. 💾 Report stored as memory chunks

---

# 🔥 Key Innovation

This project implements a **Hybrid + RAG + Tool-Based Agentic AI System**:

* Cloud AI for speed ⚡
* Local AI for reliability 💻
* Persistent Memory 🧠
* RAG (chunk-based retrieval) 🎯
* Multi-tool intelligence 🤖
* Automatic failover 🔄

👉 Ensures:

* Zero failure during API downtime
* Accurate, context-aware responses
* Multi-source intelligence
* Continuous learning

---

# 📂 Project Structure

```
AGENTIC-AI-RESEARCH/
│
├── agents/
│   ├── planner_agent.py
│   ├── search_agent.py
│   ├── reader_agent.py
│   ├── query_agent.py
│   ├── wiki_tool.py        # NEW
│   ├── arxiv_tool.py       # NEW
│
├── research_engine.py
├── generate_report.py
├── memory_db.py        
├── app.py
│
├── templates/
│   ├── index.html
│   ├── history.html
│
├── reports/
├── memory/             # 🧠 Stores RAG memory chunks
├── .env
├── requirements.txt
```

---

# ⚠️ Notes

* Do not upload `.env` file to GitHub
* Ollama must be installed
* Some websites may block scraping
* Memory is stored locally in `/memory`
* Arxiv may not return results for non-technical topics
* System uses Tavily as fallback

---

# 📌 Future Improvements

* 📄 PDF report download
* 🎨 Improved UI/UX
* 📊 Data visualization dashboard
* 🔍 Better source ranking
* ⚡ Faster local model optimization
* 🧠 Advanced semantic embeddings

---

# 👨‍💻 Author

**Harvik Sanghavi**
BTech Data Science

---

# ⭐ Support

If you like this project, give it a ⭐ on GitHub!

---
