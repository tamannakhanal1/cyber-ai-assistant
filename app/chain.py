# chain.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if the key is loaded
print(os.getenv("GOOGLE_API_KEY"))
print("DEBUG: API_KEY =", API_KEY)

def get_coordinates(address: str) -> dict | None:
    """
    Convert an address into latitude and longitude using OpenStreetMap Nominatim API.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
        response = requests.get(url, headers={"User-Agent": "TamannaApp/1.0"}, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
    except requests.RequestException as e:
        return {"error": str(e)}
    return None


def get_response(message: str) -> str:
    """
    Get AI response from Google Gemini AI.
    """
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


# Optional: testing when running chain.py directly
if __name__ == "__main__":
    print("--- Testing Gemini Chain ---")
    test_message = "Explain what a phishing attack is."
    print("User:", test_message)
    print("AI:", get_response(test_message))

    test_address = "New York"
    print("Coordinates for New York:", get_coordinates(test_address))

