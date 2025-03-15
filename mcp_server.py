from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

# Load API keys from .env
load_dotenv()
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

app = FastAPI()

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "MCP server is running"}

# ✅ Helper function for API requests
def fetch_github_data(endpoint, params={}):
    """Fetch data from GitHub API."""
    if not GITHUB_API_KEY:
        raise HTTPException(status_code=500, detail="GitHub API key not found. Set GITHUB_API_KEY in .env")

    api_url = f"https://api.github.com/{endpoint}"
    headers = {
        "Authorization": f"token {GITHUB_API_KEY}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Fetch GitHub user details
@app.get("/github-user")
def get_github_user(username: str):
    """Fetch GitHub user details."""
    data = fetch_github_data(f"users/{username}")
    return {
        "input": {"action": "fetch_github_user", "username": username},
        "output": data
    }

# ✅ Fetch GitHub repositories
@app.get("/github-repos")
def get_github_repos(username: str):
    """Fetch repositories of a GitHub user."""
    data = fetch_github_data(f"users/{username}/repos")
    return {
        "input": {"action": "fetch_github_repos", "username": username},
        "output": data
    }

# ✅ Fetch issues of a repository
@app.get("/github-issues")
def get_github_issues(owner: str, repo: str):
    """Fetch issues from a GitHub repository."""
    data = fetch_github_data(f"repos/{owner}/{repo}/issues")
    return {
        "input": {"action": "fetch_github_issues", "owner": owner, "repo": repo},
        "output": data
    }

# ✅ Create an issue in a GitHub repository
@app.post("/create-issue")
def create_issue(owner: str, repo: str, title: str, body: str = ""):
    """Create an issue in a GitHub repository."""
    if not GITHUB_API_KEY:
        return JSONResponse(status_code=500, content={"error": "GitHub API key not found"})

    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {GITHUB_API_KEY}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"title": title, "body": body}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return {
            "input": {"action": "create_issue", "owner": owner, "repo": repo, "title": title, "body": body},
            "output": response.json()
        }
    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=400, content={"error": "GitHub API request failed", "details": str(e)})

# ✅ Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
