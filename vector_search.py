# Responsible for vector analysis using Qdrant + SentenceTransformers (or other technology).

import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_qdrant_client():
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", 6333))
    api_key = os.getenv("QDRANT_API_KEY", None)
    
    # For local Docker you don't need api_key
    client = QdrantClient(host=host, port=port, api_key=api_key)
    return client

# Creates or cleans a collection in Qdrant (e.g. articles_collection).
def init_qdrant_collection(collection_name="articles_collection"):
    client = get_qdrant_client()
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    return client

# Embeds the article in Qdrant by calculating the vector (embedding) using SentenceTransformer.
def insert_article_qdrant(article_text: str, article_id: int, collection_name="articles_collection"):
    client = get_qdrant_client()
    vector = model.encode(article_text).tolist()
    client.upsert(
        collection_name=collection_name,
        points=[{
            "id": article_id,
            "vector": vector,
            "payload": {"text": article_text}
        }]
    )
    print(f"An article {article_id} saved in Qdrant!")

# Searches for articles that are most semantically similar to the query.
def search_similar_articles(query: str, collection_name="articles_collection", limit=3):
    client = get_qdrant_client()
    query_vector = model.encode(query).tolist()
    res = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )
    return res
