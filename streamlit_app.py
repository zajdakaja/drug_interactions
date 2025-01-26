import streamlit as st
import requests

#####################
# KONFIGURACJA
#####################
# Zakładamy, że API FastAPI działa lokalnie na porcie 8000
API_URL = "http://127.0.0.1:8000"

def main():
    # Ustawiamy tytuł aplikacji
    st.title("Analiza Interakcji Leków – Prototyp")

    # Tworzymy boczne menu (sidebar) z wyborem sekcji
    menu = [
        "Sprawdź interakcje leków",
        "Dodaj artykuł do MongoDB",
        "Wyszukiwanie wektorowe (Qdrant)",
        "Wyświetl historię leków (Postgres)"
    ]
    choice = st.sidebar.selectbox("Wybierz funkcjonalność", menu)

    ######################################################
    # SEKCJA 1: Sprawdź interakcje leków
    ######################################################
    if choice == "Sprawdź interakcje leków":
        st.subheader("Sekcja: Sprawdź interakcje leków")

        # Pole tekstowe do wprowadzenia listy leków
        drugs_input = st.text_input("Podaj nazwy leków, oddzielone przecinkami", value="Ibuprofen, Aspirin")

        if st.button("Sprawdź"):
            # Przykład: konwersja na listę
            drug_list = [d.strip() for d in drugs_input.split(",") if d.strip()]

            # Wywołanie endpointu FastAPI (POST /check_interactions)
            payload = {"drug_list": drug_list}
            try:
                response = requests.post(f"{API_URL}/check_interactions", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    # Wyświetlamy wynik
                    st.write("**Lek (pierwszy z listy)**:", data.get("drug"))
                    st.write("**Opis (z FDA lub innego źródła)**:", data.get("description", "Brak opisu"))
                    st.write("**Rekomendacje AI**:", data.get("recommendations", "Brak rekomendacji"))
                else:
                    st.error(f"Błąd {response.status_code} – nie udało się sprawdzić interakcji.")
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")

    ######################################################
    # SEKCJA 2: Dodaj artykuł do MongoDB
    ######################################################
    elif choice == "Dodaj artykuł do MongoDB":
        st.subheader("Sekcja: Dodaj artykuł do MongoDB")

        # Pole tekstowe do wprowadzenia treści artykułu
        article_text = st.text_area("Wklej treść artykułu (dowolny tekst)")

        if st.button("Zapisz w MongoDB"):
            # Tu możemy wywołać endpoint FastAPI, np. POST /save_article
            # lub bezpośrednio użyć funkcji z data_store.py (jeśli mamy import).
            # Przykład wywołania endpointu (zakładamy, że istnieje /save_article):
            payload = {"article_text": article_text}
            try:
                response = requests.post(f"{API_URL}/save_article", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Zapisano artykuł w MongoDB, ID = {data.get('inserted_id')}")
                else:
                    st.error(f"Błąd {response.status_code} – nie udało się zapisać artykułu.")
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")

    ######################################################
    # SEKCJA 3: Wyszukiwanie wektorowe (Qdrant)
    ######################################################
    elif choice == "Wyszukiwanie wektorowe (Qdrant)":
        st.subheader("Sekcja: Wyszukiwanie wektorowe")

        # Pole na zapytanie semantyczne
        query_text = st.text_input("Czego szukasz w artykułach?", value="Interakcje ibuprofenu z innymi lekami")

        if st.button("Szukaj"):
            # Tu możesz wywołać endpoint FastAPI typu POST /search_articles
            # lub bezpośrednio importować funkcję search_similar_articles(...)
            payload = {"query": query_text, "limit": 3}
            try:
                response = requests.post(f"{API_URL}/search_articles", json=payload)
                if response.status_code == 200:
                    results = response.json()
                    st.write("**Najbardziej podobne artykuły:**")
                    for r in results:
                        # np. r = {"score":..., "text":...}
                        st.write(f"- **Score**: {r.get('score')}")
                        st.write(f"  Treść artykułu: {r.get('text')[:300]}...")
                else:
                    st.error(f"Błąd {response.status_code} – nie udało się wyszukać artykułów.")
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")

    ######################################################
    # SEKCJA 4: Wyświetl historię leków (Postgres)
    ######################################################
    else:  # "Wyświetl historię leków (Postgres)"
        st.subheader("Sekcja: Wyświetl historię leków")

        # Przycisk do wywołania SELECT * FROM drugs
        if st.button("Pokaż wszystkie leki"):
            # Można to zrobić przez endpoint np. /list_drugs
            # lub bezpośrednio z data_store (jeśli mamy import i dostęp do read_all_drugs())
            try:
                response = requests.get(f"{API_URL}/list_drugs")
                if response.status_code == 200:
                    drugs_data = response.json()  # zakładamy, że to jest lista obiektów
                    st.write("**Lista leków w bazie:**")
                    for item in drugs_data:
                        st.write(f"- ID: {item.get('id')} | Nazwa: {item.get('drug_name')} | Opis: {item.get('interactions')}")
                else:
                    st.error(f"Błąd {response.status_code} – nie udało się pobrać historii leków.")
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
