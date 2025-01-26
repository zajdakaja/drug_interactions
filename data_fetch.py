import requests

FDA_ENDPOINT = "https://api.fda.gov/drug/label.json"

"""
example function that connects to the FDA API, 
searches for a drug with the given name (in the brand_name field) and retrieves information such as description, 
warnings, etc..
"""
def fetch_drug_data_fda(drug_name: str) -> dict:
    """
    Retrieves drug data from the FDA public API (simplified example).
    Returns a dict with information about the drug.
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
        print(f"FDA download error: {e}")
        return {}
    

