# 🧠 Agentic AI Research System (Hybrid AI)

A multi-agent AI research system that automatically generates structured research reports using **Tavily (web search)**, **Gemini (cloud AI)**, and **Ollama (local AI fallback)**.

---

## 🚀 Features

* 🤖 **Multi-Agent Architecture**

  * Planner Agent – breaks topic into research tasks
  * Search Agent – retrieves relevant URLs using Tavily
  * Reader Agent – extracts content from web pages (web scraping)
  * Report Generator – creates structured research reports

* 🌐 **Intelligent Web Research**

  * Powered by **Tavily API**
  * Filters low-quality websites
  * Retrieves relevant and high-quality sources

* 🕸️ **Web Scraping System**

  * Uses **newspaper3k** for structured article extraction
  * Uses **BeautifulSoup fallback** for unsupported websites

* ⚡ **Parallel Processing**

  * Uses multithreading to speed up research

* 🧠 **Hybrid AI System**

  * Uses **Gemini API (cloud)** for fast and high-quality responses
  * Falls back to **Ollama (local AI)** if API fails

* 🔄 **Fail-Safe Mechanism**

  * Retry logic for API failures
  * Automatic fallback ensures output is always generated

* 📊 **Structured Report Generation**

  * Executive Summary
  * Key Findings
  * Detailed Analysis
  * Challenges & Risks
  * Future Outlook
  * Sources with citations

---

## 🏗️ Architecture

```text
User Input
   ↓
Flask App
   ↓
Planner Agent (Gemini → Ollama fallback)
   ↓
Research Engine
   ├── Query Generation
   ├── Tavily Web Search
   ├── Reader Agent (Web Scraping)
   ↓
Report Generator (Gemini → Ollama fallback)
   ↓
Final Research Report
```

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)

* **AI Models:**

  * Google Gemini API
  * Ollama (Local LLM – phi / tinyllama)

* **Search API:**

  * Tavily API

* **Web Scraping:**

  * newspaper3k
  * BeautifulSoup

* **Libraries:**

  * requests
  * concurrent.futures
  * python-dotenv

* **Other:**

  * Multithreading
  * Git & GitHub

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/harvik07/AGENTIC-AI-RESEARCH-FINAL.git
cd AGENTIC-AI-RESEARCH-FINAL
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add API Keys

Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
```

---

### 4️⃣ Install Ollama (Local AI fallback)

Download:
👉 https://ollama.com

Run model:

```bash
ollama run phi
```

---

### 5️⃣ Run the application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🧪 How It Works

1. User enters a research topic
2. Planner agent breaks it into tasks
3. Tavily searches for relevant sources
4. Reader agent scrapes and extracts content
5. AI generates a structured report
6. If API fails → system switches to Ollama

---

## 🔍 Web Search & Scraping

* **Tavily API** → retrieves relevant URLs
* **newspaper3k** → extracts clean article content
* **BeautifulSoup** → fallback scraping for unsupported sites

---

## 🔥 Key Innovation

This project implements a **Hybrid AI Architecture**:

* Cloud AI for speed ⚡
* Local AI for reliability 💻
* Automatic failover system 🔄

👉 Ensures **zero failure even during API downtime**

---

## 📂 Project Structure

```text
AGENTIC-AI-RESEARCH/
│
├── agents/
│   ├── planner_agent.py
│   ├── search_agent.py
│   ├── reader_agent.py
│   ├── query_agent.py
│
├── research_engine.py
├── generate_report.py
├── app.py
│
├── templates/
│   ├── index.html
│   ├── history.html
│
├── reports/
├── .env
├── requirements.txt
```

---

## ⚠️ Notes

* Do not upload `.env` file to GitHub
* Ollama must be installed for offline fallback
* Some websites may block scraping
* Local models may be slower than cloud APIs

---

## 📌 Future Improvements

* 📄 PDF report download
* 🎨 Improved UI/UX
* 📊 Data visualization dashboard
* 🔍 Better source ranking
* ⚡ Faster local model optimization

---

## 👨‍💻 Author

**Harvik Sanghavi**
BTech Data Science

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
