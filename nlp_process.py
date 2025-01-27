# Includes functions for text processing (NLP), e.g. using SpaCy, Regex, BeautifulSoup.

import spacy
from bs4 import BeautifulSoup
import re

# Load the language model. If you want for eg. Polish, change to ‘pl_core_news_lg’
nlp = spacy.load("en_core_web_sm")

# A simple example of how to extract drug names from text (using SpaCy models, rules, etc.).
def extract_drug_names(text: str):
    """
    A very simple function for extracting potential drug names from text.
    """
    doc = nlp(text)
    drugs_found = []
    for token in doc:
        # Simplification: if token has entity type ‘ORG’ or looks like a proper name
        if token.ent_type_ == "ORG" or (token.text[0].isupper() and len(token.text) > 3):
            drugs_found.append(token.text)
    return list(set(drugs_found))

# Convert HTML to plain text, remove tags.
def parse_html_content(html: str):
    """
    An example of using BeautifulSoup to extract text from HTML and clean up whitespace.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text
