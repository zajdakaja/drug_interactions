import streamlit as st
import requests

#####################
# CONFIGURATION
#####################
# We assume that the FastAPI API is running locally on port 8000
API_URL = "http://127.0.0.1:8000"

def main():
    # Set the title of the application
    st.title("Drug Interaction Analysis - Prototype")

    # We create a sidebar menu with a selection of sections
    menu = [
        ‘Check drug interactions’,
        ‘Add article to MongoDB’,
        ‘Vector search (Qdrant)’,
        ‘View drug history (Postgres)’.
    ]
    choice = st.sidebar.selectbox("Select functionality", menu)

    ######################################################
    # SECTION 1: Check drug interactions
    ######################################################
    if choice == "Check drug interactions:":
        st.subheader("Section: Check drug interactions")

        # Text field for entering a list of medicines
        drugs_input = st.text_input("Give the names of the drugs, separated by commas.", value="Ibuprofen, Aspirin")

        if st.button("Check"):
            # Example: conversion to a list
            drug_list = [d.strip() for d in drugs_input.split(",") if d.strip()]

            # FastAPI endpoint call (POST /check_interactions)
            payload = {"drug_list": drug_list}
            try:
                response = requests.post(f"{API_URL}/check_interactions", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    # Display the result
                    st.write("**Drug (first on the list)**:", data.get("drug"))
                    st.write("**Description (from FDA or other source)**:", data.get("description", "No description"))
                    st.write("**AI recommendations**:", data.get("recommendations", "No recommendations"))
                else:
                    st.error(f"Error {response.status_code} – interaction could not be tested.")
            except Exception as e:
                st.error(f"Error occurred: {e}")

    ######################################################
    # SECTION 2: Add the article to MongoDB
    ######################################################
    elif choice == "Add the article to MongoDB":
        st.subheader("Section: Add the article to MongoDB")

        # Text field for entering article content
        article_text = st.text_area("Paste article content (any text)")

        if st.button("Save in MongoDB"):
            # Here we can call a FastAPI endpoint, e.g. POST /save_article
            # or directly use the function from data_store.py (if we have an import).
            # Example of an endpoint call (we assume /save_article exists):
            payload = {"article_text": article_text}
            try:
                response = requests.post(f"{API_URL}/save_article", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"An article has been saved in MongoDB, ID = {data.get('inserted_id')}")
                else:
                    st.error(f"Error {response.status_code} – failed to save the article.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    ######################################################
    # SECTION 3: Vector search (Qdrant)
    ######################################################
    elif choice == "Vector Search (Qdrant)":
        st.subheader("Section: Vector Search")

        # Field for semantic query
        query_text = st.text_input("What do you look for in articles?", value="Interactions of ibuprofen with other drugs")

        if st.button("Search"):
            # Here you can call the FastAPI endpoint POST type /search_articles
            # or directly import the search_similar_articles(...) function
            payload = {"query": query_text, "limit": 3}
            try:
                response = requests.post(f"{API_URL}/search_articles", json=payload)
                if response.status_code == 200:
                    results = response.json()
                    st.write("**Most related articles:**")
                    for r in results:
                        # np. r = {"score":..., "text":...}
                        st.write(f"- **Score**: {r.get('score')}")
                        st.write(f"  Article content: {r.get('text')[:300]}...")
                else:
                    st.error(f"Błąd {response.status_code} – failed to search for articles.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    ######################################################
    # SECTION 4: View medication history (Postgres)
    ######################################################
    else:  # "Display drug history (Postgres)"
        st.subheader("Section: Display drug history (Postgres)")
        
        # Button to call SELECT * FROM drugs
        if st.button("Show all drugs"):
            # This can be done via endpoint e.g. /list_drugs
            # or directly from the data_store (if we have import and access to read_all_drugs())
            try:
                response = requests.get(f"{API_URL}/list_drugs")
                if response.status_code == 200:
                    drugs_data = response.json()  # we assume that this is a list of objects
                    st.write("**List of drugs in the database:**")
                    for item in drugs_data:
                        st.write(f"- ID: {item.get('id')} | Name: {item.get('drug_name')} | Description: {item.get('interactions')}")
                else:
                    st.error(f"Error {response.status_code} – failed to retrieve drug history.")
            except Exception as e:
                st.error(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
