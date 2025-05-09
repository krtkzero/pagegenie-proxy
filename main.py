import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Fetch the API key securely from environment variables
API_KEY = os.getenv("API_KEY")

@app.get("/")
async def root():
    return {"message": "PageGenie Proxy Server is running!"}

@app.post("/api/gemini")
async def gemini_proxy(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")

        # Check if the API key is available
        if not API_KEY:
            print("API key not found!")  # Debug log
            return {"error": "API key not found in environment variables."}

        # Make the request to Gemini API
        response = requests.post(
            "https://api.gemini.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",  # Use the environment variable
                "Content-Type": "application/json"
            },
            json={
                "model": "gemini-1",  # Replace with actual Gemini model name if different
                "messages": [{"role": "user", "content": f"Write JavaScript to: {prompt}. Only return the JS code."}],
                "temperature": 0.5
            }
        )

        # Check if the request was successful
        response.raise_for_status()

        # Log the full response for debugging
        response_data = response.json()
        print("Full API Response:", response_data)

        # Return the JSON response directly for inspection
        return response_data

    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
        return {"error": f"Request error: {str(e)}"}

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}
