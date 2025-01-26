# Drug Interaction Analysis Application

## 1. Application Overview and Features

### 1.1 General Description

This application is designed to analyze drug interactions using various technologies:

- **Data Retrieval:** Fetching data from external sources (e.g., FDA API).
- **Data Storage:** Processing and saving data into databases (PostgreSQL, MongoDB).
- **Recommendation Generation:** Utilizing GPT models (e.g., GPT-4) to provide recommendations.
- **Vector Search:** Implementing vector-based search (Qdrant).
- **Interactive Interface:** Streamlit-based user interface and FastAPI-powered REST API.

### 1.2 Main Files (Modules)

- `data_fetch.py`: Fetches drug data from external APIs (e.g., FDA).
- `data_store.py`: Handles data storage/retrieval in PostgreSQL and MongoDB.
- `llm_integration.py`: Integrates GPT (OpenAI) for generating recommendations.
- `main.py`: Main FastAPI file defining endpoints.
- `nlp_process.py`: Text processing using tools like SpaCy, Regex, and BeautifulSoup.
- `vector_search.py`: Vector search with Qdrant and SentenceTransformers.
- `streamlit_app.py`: Interactive Streamlit application demonstrating all features.

---

## 2. Step-by-Step: Running the Application

### 2.1 Environment Setup

1. Clone or download the project folder (`drug_interactions_prototype`).
2. Navigate to the project folder in the terminal (Git Bash, PowerShell, etc.).
3. Create a virtual environment (Python 3.9+):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```

5. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

6. (Optional) Install the SpaCy model (e.g., English):

   ```bash
   python -m spacy download en_core_web_sm
   ```

### 2.2 Database Configuration and Files

#### PostgreSQL
- Start the PostgreSQL service.
- Create a database `drugdb` and a table `drugs` with the structure:
  ```sql
  CREATE TABLE drugs (
      id SERIAL PRIMARY KEY,
      drug_name VARCHAR,
      interactions TEXT
  );
  ```
- Ensure you have a user (e.g., `drug_user`) with a password (e.g., `secret`).

#### MongoDB
- Start the MongoDB service (e.g., Community Edition).
- The database `drug_mongo` and collection `articles` are created automatically upon the first insert.

#### Qdrant
- To enable vector search, run Qdrant in Docker:

  ```bash
  docker run -p 6333:6333 qdrant/qdrant
  ```

#### `.env` File (Environment Variables)

Create a `.env` file to store database connection details and API keys:

```env
POSTGRES_HOST=localhost
POSTGRES_DB=drugdb
POSTGRES_USER=drug_user
POSTGRES_PASSWORD=secret
MONGO_URI=mongodb://localhost:27017
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

### 2.3 Starting the FastAPI Server

Run the following command in the terminal (with the virtual environment active):

```bash
uvicorn app.main:app --reload
```

If successful, you will see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

#### Test Endpoints
Visit `http://127.0.0.1:8000/docs` to access Swagger UI. Key endpoints include:

- **POST /check_interactions:** Analyze drug interactions.
- **POST /save_article:** Save an article to MongoDB.
- **POST /search_articles:** Perform vector search for articles.
- **GET /list_drugs:** Retrieve the list of drugs from PostgreSQL.

### 2.4 Running the Streamlit Front-End

In a new terminal window (keeping the FastAPI server running):

```bash
streamlit run streamlit_app.py
```

Access the interface at `http://localhost:8501`. Features include:

- **Drug Interaction Analysis:** Enter drug names and view interaction details.
- **Add Articles:** Save articles to MongoDB.
- **Vector Search:** Query articles using vector-based search.
- **Drug List:** View saved drugs from PostgreSQL.

---

## 3. Summary of Features

### Data Retrieval (FDA)
- `fetch_drug_data_fda` in `data_fetch.py` retrieves initial drug descriptions.
- Triggered in the `check_interactions` endpoint for the first drug.

### PostgreSQL Data Storage
- `save_drug_postgres` in `data_store.py` saves drug interaction records.
- Enables query history and descriptions.

### MongoDB Article Storage
- `save_article_mongo` stores documents (e.g., notes or articles).
- Invoked by the `save_article` endpoint.

### Vector Search (Qdrant)
- `search_similar_articles` in `vector_search.py` computes embeddings and queries Qdrant.
- Accessible via the `search_articles` endpoint.

### Recommendation Generation (GPT)
- `get_drug_recommendations` in `llm_integration.py` generates GPT-4 recommendations.
- Results appear in the `recommendations` field of the `check_interactions` response.

### Streamlit Interface
- Offers a user-friendly way to test all functionalities.
- Uses FastAPI endpoints for backend operations.

---

## 4. FAQ and Troubleshooting

### 4.1 Common Issues

#### Error 500 (Internal Server Error) on `/check_interactions`
- Check terminal logs for details.
- Ensure PostgreSQL is running and GPT API key is valid.

#### Empty Drug Description
- Some drugs may lack data in FDA sources. Try common drugs like Aspirin or Warfarin.

#### MongoDB Article Save Error
- Verify MongoDB is running and `MONGO_URI` is correctly configured.

#### GPT Key or Limit Issues
- If recommendations fail, check your OpenAI plan and API key validity.

#### Qdrant Issues
- If Qdrant is not running, the `search_articles` endpoint will fail. Disable the vector search section in Streamlit to avoid errors.

---

## 5. Final Output

By completing all steps:

- FastAPI server runs on port 8000, handling API requests.
- Streamlit interface on port 8501 displays:
  - **Drug Interaction Check:** GPT analysis and PostgreSQL storage.
  - **Article Management:** MongoDB integration.
  - **Vector Search:** Qdrant-powered search.
  - **Drug List History:** PostgreSQL queries.

Demonstrate the complete workflow from inputting drug names to generating AI-based recommendations, saving data, and conducting searches.

