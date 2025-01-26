#Zajmuje się pobieraniem (fetchowaniem) danych z zewnętrznych źródeł, np. z publicznego API FDA lub z innego miejsca w internecie.

import requests

FDA_ENDPOINT = "https://api.fda.gov/drug/label.json"

"""
przykładowa funkcja, która łączy się z API FDA, 
wyszukuje lek o podanej nazwie (w polu brand_name) i pobiera informacje takie jak opis, 
ostrzeżenia itp.
"""
def fetch_drug_data_fda(drug_name: str) -> dict:
    """
    Pobiera dane o leku z publicznego API FDA (uproszczony przykład).
    Zwraca dict z informacjami o leku.
    """
    try:
        params = {
            "search": f"openfda.brand_name:{drug_name}",
            "limit": 1
        }
        response = requests.get(FDA_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Błąd pobierania danych z FDA: {e}")
        return {}
    

