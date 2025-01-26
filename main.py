import sys
print("Python executable:", sys.executable)
print("Sys.path:", sys.path)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import os

# Import funkcji z plików pomocniczych
from app.data_fetch import fetch_drug_data_fda  # przykładowa funkcja
from app.data_store import save_drug_postgres, save_article_mongo
from app.llm_integration import get_drug_recommendations
from app.vector_search import search_similar_articles  # jeśli chcesz Qdrant
# Ewentualnie: from app.data_store import get_all_drugs (jeśli taką funkcję masz)

app = FastAPI()

#############################
# MODELE DANYCH (Pydantic)
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
    Endpoint analizujący interakcje między lekami w 'drug_list'.
    1) Pobiera dane z FDA dla pierwszego leku (przykładowo).
    2) Zapisuje opis do Postgres.
    3) Wywołuje GPT po rekomendacje.
    4) Zwraca JSON z opisem i rekomendacjami.
    """
    if not request.drug_list:
        return {"drug": None, "description": "", "recommendations": "Brak leków w zapytaniu"}

    drug_name = request.drug_list[0]

    # 1) Pobieramy dane z FDA
    raw_data = fetch_drug_data_fda(drug_name)  # może zwrócić dict lub pusty {}
    # Uproszczenie: wyciągamy opis
    try:
        description = raw_data["results"][0].get("description", [""])[0]
    except (IndexError, KeyError):
        description = ""

    # 2) Zapis do Postgres (nazwę leku + opis)
    save_drug_postgres(drug_name, description)

    # 3) GPT-4: generowanie rekomendacji
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
    Endpoint do zapisu artykułu w MongoDB (kolekcja 'articles').
    Zwraca ID zapisanego dokumentu.
    """
    article_text = req.article_text.strip()
    if not article_text:
        return {"inserted_id": None, "error": "Pusty tekst artykułu"}

    try:
        # wywołanie funkcji z data_store.py
        save_article_mongo(article_text)
        # Niestety, save_article_mongo nie zwraca inserted_id (chyba że ją zmodyfikujesz)
        # By to zwrócić, można zwrócić wartość z insert_one().inserted_id
        return {"inserted_id": "DummyID"}  # dopasuj do własnej implementacji
    except Exception as e:
        return {"inserted_id": None, "error": str(e)}

#############################
# ENDPOINT 3: /search_articles
#############################
@app.post("/search_articles")
def search_articles(req: SearchRequest):
    """
    Endpoint do wyszukiwania wektorowego (np. w Qdrant).
    Zwraca listę artykułów (np. tytuł, fragment) w kolejności podobieństwa.
    """
    try:
        results = search_similar_articles(req.query, limit=req.limit)  # tu wchodzi Qdrant
        # Przykładowa struktura:
        # results może być listą obiektów: [{"score":..., "text":...}, ...]
        return results
    except Exception as e:
        return {"error": str(e)}

#############################
# ENDPOINT 4: /list_drugs
#############################
@app.get("/list_drugs")
def list_drugs():
    """
    Endpoint do pobrania wszystkich leków z tabeli 'drugs' w Postgres.
    Zwraca listę obiektów JSON.
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
        # rows będzie listą słowników [{'id':..., 'drug_name':..., 'interactions':...}, ...]
        return rows
    except Exception as e:
        return {"error": str(e)}
