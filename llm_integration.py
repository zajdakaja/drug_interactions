# Includes code for integration into a large language model (e.g. GPT-4 via the OpenAI API).

import os
import json
import openai

def load_api_key():
    # Get path to parent directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "env", "api_key.json")
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data["api_key"]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except KeyError:
        print("Key ‘api_key’ not found in JSON file.")
        raise

api_key = load_api_key()
openai.api_key = api_key

# The main function that builds the prompt (text command) and sends the query to the GPT.
def get_drug_recommendations(drug_list, interactions):
    prompt = f"""
    You are a medical assistant. You analyse drug interactions: {drug_list}.
    Description of interactions:
    {interactions}
    What are the potential risks and what would you recommend to the patient?
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT-4 callout error: {e}")
        return "Recommendation generation error."
