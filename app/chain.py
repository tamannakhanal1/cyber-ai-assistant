import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("AIzaSyCDx6vuO0_yzXI3trvw3h-kwHLvZcyt73E")

def get_response(message: str) -> str:
    """
    Send user message to OpenAI (v1.x API) and return the AI's reply.
    Handles configuration and specific API errors.
    """
    if not API_KEY:
        return "Configuration Error: OPENAI_API_KEY is not set. Please check your .env file."

    try:
        # Initialize the OpenAI client with the API key
        client = openai.OpenAI(api_key=API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=150
        )
        return response.choices[0].message.content
    
    except openai.AuthenticationError:
        # Catches issues like an invalid key
        return "Authentication Error: The provided API key is invalid or lacks necessary permissions."
    except openai.APIError as e:
        # Catches other API-specific errors (rate limits, context window, etc.)
        return f"API Error: An OpenAI API error occurred: {e}"
    except Exception as e:
        # Catches other unexpected errors (network, file system, etc.)
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    print("--- Testing OpenAI Chain ---")
    test_message = "Explain what a large language model is in one short paragraph."
    print(f"User Message: {test_message}")

    if API_KEY:
        print("API Key status: Loaded.")
    else:
        print("API Key status: Missing. Expecting a Configuration Error.")

    ai_response = get_response(test_message)
    print("\nAI Response:")
    print(ai_response)
    print("----------------------------")