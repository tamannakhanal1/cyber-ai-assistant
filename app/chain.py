# chain.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_response(message: str) -> str:
    if not API_KEY:
        return "Error: Missing GOOGLE_API_KEY in .env file."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    payload = {"contents": [{"parts": [{"text": message}]}]}

    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get("candidates")
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
        return "AI did not return any content."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with AI: {e}"



if __name__ == "__main__":
    print("--- Testing Gemini Chain ---")
    msg = "Explain what a phishing attack is."
    print("User:", msg)
    print("AI:", get_response(msg))
