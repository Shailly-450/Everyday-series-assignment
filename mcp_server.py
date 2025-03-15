from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

app = FastAPI()

# ✅ Add this route to verify the server is running
@app.get("/")
def root():
    return {"message": "MCP server is running"}

@app.get("/github-user")
def get_github_user(username: str):
    """Fetch GitHub user details using GitHub API."""
    
    if not GITHUB_API_KEY:
        return {"error": "GitHub API key not found. Set GITHUB_API_KEY in .env"}

    api_url = f"https://api.github.com/users/{username}"
    
    headers = {
        "Authorization": f"token {GITHUB_API_KEY}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raises error for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "GitHub API request failed", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
