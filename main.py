import sys
print("Python executable:", sys.executable)
print("Sys.path:", sys.path)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import os

# Importing functions from support files
from app.data_fetch import fetch_drug_data_fda  # sample function
from app.data_store import save_drug_postgres, save_article_mongo
from app.llm_integration import get_drug_recommendations
from app.vector_search import search_similar_articles  # if you want Qdrant
# alternatively: from app.data_store import get_all_drugs (if you have such a function)

app = FastAPI()

#############################
# DATA MODELS (Pydantic)
#############################

class DrugListRequest(BaseModel):
    drug_list: List[str]

class ArticleRequest(BaseModel):
    article_text: str

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 3

#############################
# ENDPOINT 1: /check_interactions
#############################
@app.post("/check_interactions")
def check_interactions(request: DrugListRequest):
    """
    Endpoint analysing drug interactions in ‘drug_list’.
    1) Retrieves data from the FDA for the first drug (example).
    2) Saves the description to Postgres.
    3) Calls GPT for recommendations.
    4) Returns JSON with description and recommendations.
    """
    if not request.drug_list:
        return {"drug": None, "description": "", "recommendations": "Brak leków w zapytaniu"}

    drug_name = request.drug_list[0]

    # 1) Downloading data from the FDA
    raw_data = fetch_drug_data_fda(drug_name)  # may return a dict or an empty {}
    # Simplification: we extract the description
    try:
        description = raw_data["results"][0].get("description", [""])[0]
    except (IndexError, KeyError):
        description = ""

    # 2) Entry into Postgres (drug name + description)
    save_drug_postgres(drug_name, description)

    # 3) GPT-4: generation of recommendations
    recommendations = get_drug_recommendations(request.drug_list, description)

    return {
        "drug": drug_name,
        "description": description,
        "recommendations": recommendations
    }

#############################
# ENDPOINT 2: /save_article
#############################
@app.post("/save_article")
def save_article(req: ArticleRequest):
    """
    Endpoint to save an article in MongoDB (collection ‘articles’).
    Returns the ID of the saved document.
    """
    article_text = req.article_text.strip()
    if not article_text:
        return {"inserted_id": None, "error": "Blank article text"}

    try:
       # call function from data_store.py
        save_article_mongo(article_text)
        # Unfortunately, save_article_mongo does not return an inserted_id (unless you modify it)
        # To return this, you can return the value from insert_one().inserted_id
        return {"inserted_id": "DummyID"}  # match your own implementation
    except Exception as e:
        return {"inserted_id": None, "error": str(e)}

#############################
# ENDPOINT 3: /search_articles
#############################
@app.post("/search_articles")
def search_articles(req: SearchRequest):
    """
    Endpoint for vector search (e.g. in Qdrant).
    Returns a list of articles (e.g. title, excerpt) in order of similarity.
    """
    try:
        results = search_similar_articles(req.query, limit=req.limit)  # here comes Qdrant
        # exemplary structure:
        # results can be a list of objects: [{"score":..., "text":...}, ...]
        return results
    except Exception as e:
        return {"error": str(e)}

#############################
# ENDPOINT 4: /list_drugs
#############################
@app.get("/list_drugs")
def list_drugs():
    """
    Endpoint to retrieve all drugs from the ‘drugs’ table in Postgres.
    Returns a list of JSON objects.
    """
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from app.data_store import get_postgres_config

    config = get_postgres_config()
    rows = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, drug_name, interactions FROM drugs ORDER BY id DESC")
                rows = cur.fetchall()
        # rows will be a list of dictionaries [{'id':..., 'drug_name':..., 'interactions':...}, ...]
        return rows
    except Exception as e:
        return {"error": str(e)}
