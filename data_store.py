# Responsible for writing and reading data from databases (relational and non-relational).

import os
import psycopg2
import pymongo
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# loads the connection parameters (host, user, password, dbname).
def get_postgres_config():
    """
 Retrieves the PostgreSQL configuration from the .env file or environment variables.
    """
    required_keys = ["POSTGRES_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise EnvironmentError(f"The following environment variables are missing: {', '.join(missing_keys)}")
    
    return {
        'host': os.getenv("POSTGRES_HOST"),
        'dbname': os.getenv("POSTGRES_DB"),
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD")
    }

def get_mongo_uri():
    """
    Retrieves the MongoDB URI from the .env file or uses the default value.
    """
    return os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Adds a drug entry to the drugs table in the Postgres database.
def save_drug_postgres(drug_name: str, interactions: str):
    """
    Saves the drug information to the ‘drugs’ table in PostgreSQL.
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
                print(f"Saved to PostgreSQL, ID = {new_id}")
    except Exception as e:
        print(f"Error while writing to PostgreSQL: {e}")

# Saves the article text to a collection in MongoDB.
def save_article_mongo(article_text: str):
    """
    Saves the article to the ‘articles’ collection in the ‘drug_mongo’ database.
    """
    try:
        mongo_uri = get_mongo_uri()
        client = pymongo.MongoClient(mongo_uri)
        db = client["drug_mongo"]
        collection = db["articles"]
        doc = {"content": article_text}
        result = collection.insert_one(doc)
        print(f"The article was saved in MongoDB, ID = {result.inserted_id}")
    except Exception as e:
        print(f"Error while writing to MongoDB: {e}")

if __name__ == "__main__":
    # Example of use of the function
    try:
        print("Testing the connection to PostgreSQL.....")
        save_drug_postgres("Aspirin", "Possible interactions with Ibuprofen")
        
        print("Testing the connection to MongoDB...")
        save_article_mongo("Test article on drug interactions.")
    except Exception as error:
        print(f"Error encountered: {error}")
