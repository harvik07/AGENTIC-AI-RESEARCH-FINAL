import chromadb

# -----------------------------
# PERSISTENT DATABASE
# -----------------------------
client = chromadb.PersistentClient(path="./memory")

# -----------------------------
# COLLECTION
# -----------------------------
collection = client.get_or_create_collection(
    name="research_memory"
)


# -----------------------------
# STORE MEMORY (RAG CHUNKING)
# -----------------------------
def store_memory(query, content):
    try:
        if not content or not query:
            return

        print(f"\n💾 Storing chunks for: {query}")

        # -----------------------------
        # SPLIT INTO CHUNKS
        # -----------------------------
        chunk_size = 400  # words per chunk
        words = content.split()

        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        # -----------------------------
        # STORE EACH CHUNK
        # -----------------------------
        for idx, chunk in enumerate(chunks):

            # safety check
            if len(chunk.strip()) < 50:
                continue

            unique_id = f"{query}_{idx}_{hash(chunk)}"

            collection.add(
                documents=[chunk],
                metadatas=[{"query": query}],
                ids=[unique_id]
            )

    except Exception as e:
        print("❌ Store error:", e)


# -----------------------------
# SEARCH MEMORY (RETRIEVE BEST CHUNKS)
# -----------------------------
def search_memory(query):
    try:
        print(f"\n🔍 Searching memory for: {query}")

        results = collection.query(
            query_texts=[query],
            n_results=5   # top 5 relevant chunks
        )

        docs = results.get("documents", [])

        if docs and docs[0]:
            print("🧠 Relevant chunks found!")

            # Combine chunks into one context
            combined = "\n".join(docs[0])

            return combined

        else:
            print("⚠️ No memory found.")
            return ""

    except Exception as e:
        print("❌ Search error:", e)
        return ""


# -----------------------------
# DEBUG: VIEW ALL MEMORY
# -----------------------------
def view_all_memory():
    try:
        data = collection.get()

        print("\n📂 ALL STORED CHUNKS:")

        for i, doc in enumerate(data.get("documents", [])):
            print(f"\n--- Chunk {i+1} ---")
            print(doc[:200])

    except Exception as e:
        print("❌ Error viewing memory:", e)