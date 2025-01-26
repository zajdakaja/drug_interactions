# Zawiera kod do integracji z dużym modelem językowym (np. GPT-4 przez API OpenAI).

import os
import json
import openai

def load_api_key():
    # Pobierz ścieżkę do katalogu nadrzędnego
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "env", "api_key.json")
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data["api_key"]
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {file_path}")
        raise
    except KeyError:
        print("Klucz 'api_key' nie został znaleziony w pliku JSON.")
        raise

api_key = load_api_key()
openai.api_key = api_key

# Główna funkcja, która buduje prompt (tekstowe polecenie) i wysyła zapytanie do GPT.
def get_drug_recommendations(drug_list, interactions):
    prompt = f"""
    Jesteś asystentem medycznym. Analizujesz interakcje leków: {drug_list}.
    Opis interakcji:
    {interactions}
    Jakie są potencjalne zagrożenia i co byś zalecił pacjentowi?
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Błąd wywołania GPT-4: {e}")
        return "Błąd generowania rekomendacji."
