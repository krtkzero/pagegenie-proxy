from fastapi import FastAPI, Request
import requests

app = FastAPI()

API_KEY = "AIzaSyBOKRHS50LsMznOySAS6_yURH7Pav_DoXc"  # Replace with your actual key

@app.post("/api/gemini")
async def gemini_proxy(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    response = requests.post(
        "https://api.gemini.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AIzaSyBOKRHS50LsMznOySAS6_yURH7Pav_DoXc}",
            "Content-Type": "application/json"
        },
        json={
        "model": "gemini-1",  # Replace with the actual Gemini model name
        "messages": [{"role": "user", "content": f"Write JavaScript to: {prompt}. Only return the JS code."}],
        "temperature": 0.5
        }
    )
    return response.json()
