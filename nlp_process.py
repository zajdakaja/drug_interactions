# Zawiera funkcje do przetwarzania tekstu (NLP), np. z użyciem SpaCy, Regex, BeautifulSoup.

import spacy
from bs4 import BeautifulSoup
import re

# Załaduj model językowy. Jeśli chcesz polski, zmień na "pl_core_news_lg"
nlp = spacy.load("en_core_web_sm")

# Prosty przykład, jak wyłuskać nazwy leków z tekstu (wykorzystując modele SpaCy, reguły itp.).
def extract_drug_names(text: str):
    """
    Bardzo prosta funkcja do wyłuskania potencjalnych nazw leków z tekstu.
    """
    doc = nlp(text)
    drugs_found = []
    for token in doc:
        # Uproszczenie: jeśli token ma typ encji 'ORG' lub wygląda na nazwę własną
        if token.ent_type_ == "ORG" or (token.text[0].isupper() and len(token.text) > 3):
            drugs_found.append(token.text)
    return list(set(drugs_found))

# Konwersja HTML do czystego tekstu, usuwanie znaczników.
def parse_html_content(html: str):
    """
    Przykład użycia BeautifulSoup do wyciągnięcia tekstu z HTML i wyczyszczenia białych znaków.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text
