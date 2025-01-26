# Odpowiada za zapisywanie i odczytywanie danych z baz (relacyjnych oraz nierelacyjnych).

import os
import psycopg2
import pymongo
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

# wczytuje parametry połączenia (host, user, password, dbname).
def get_postgres_config():
    """
    Pobiera konfigurację PostgreSQL z pliku .env lub zmiennych środowiskowych.
    """
    required_keys = ["POSTGRES_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise EnvironmentError(f"Brakuje następujących zmiennych środowiskowych: {', '.join(missing_keys)}")
    
    return {
        'host': os.getenv("POSTGRES_HOST"),
        'dbname': os.getenv("POSTGRES_DB"),
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD")
    }

def get_mongo_uri():
    """
    Pobiera URI MongoDB z pliku .env lub używa wartości domyślnej.
    """
    return os.getenv("MONGO_URI", "mongodb://localhost:27017")

#  Dodaje wpis o leku do tabeli drugs w bazie Postgres.
def save_drug_postgres(drug_name: str, interactions: str):
    """
    Zapisuje informację o leku do tabeli 'drugs' w PostgreSQL.
    """
    try:
        db_config = get_postgres_config()
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO drugs (drug_name, interactions)
                VALUES (%s, %s)
                RETURNING id
                """
                cursor.execute(insert_query, (drug_name, interactions))
                new_id = cursor.fetchone()[0]
                print(f"Zapisano do PostgreSQL, ID = {new_id}")
    except Exception as e:
        print(f"Błąd podczas zapisu do PostgreSQL: {e}")

#  Zapisuje tekst artykułu do kolekcji w MongoDB.
def save_article_mongo(article_text: str):
    """
    Zapisuje artykuł do kolekcji 'articles' w bazie 'drug_mongo'.
    """
    try:
        mongo_uri = get_mongo_uri()
        client = pymongo.MongoClient(mongo_uri)
        db = client["drug_mongo"]
        collection = db["articles"]
        doc = {"content": article_text}
        result = collection.insert_one(doc)
        print(f"Zapisano artykuł w MongoDB, ID = {result.inserted_id}")
    except Exception as e:
        print(f"Błąd podczas zapisu do MongoDB: {e}")

if __name__ == "__main__":
    # Przykład użycia funkcji
    try:
        print("Testowanie połączenia z PostgreSQL...")
        save_drug_postgres("Aspiryna", "Możliwe interakcje z Ibuprofenem")
        
        print("Testowanie połączenia z MongoDB...")
        save_article_mongo("Artykuł testowy dotyczący interakcji leków.")
    except Exception as error:
        print(f"Napotkano błąd: {error}")
