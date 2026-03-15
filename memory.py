import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="research_memory"
)

def store_research(text, source):

    collection.add(
        documents=[text],
        metadatas=[{"source": source}],
        ids=[source]
    )


def search_memory(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    return results["documents"] 