from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/mcp")
def process_request(query: str):
    """Handles AI assistant requests via OpenAI API."""
    
    api_url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": query}]
    }

    response = requests.post(api_url, headers=headers, json=data)
    
    try:
        return response.json()
    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
