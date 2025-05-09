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
            return {"error": "API key not found in environment variables."}

        # Make the request to Gemini API
        response = requests.post(
            "https://api.gemini.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
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
        print("API Response:", response.json())

        # Return the JSON response directly for inspection
        return response.json()

    except requests.RequestException as e:
        return {"error": f"Request error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
