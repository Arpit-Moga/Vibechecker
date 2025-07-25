from fastmcp import FastMCP
from pydantic import BaseModel, ValidationError
from typing import List, Optional

mcp = FastMCP(name="MinimalMCPServer", instructions="Upload a codebase, trigger review, and get results.")

# --- Pydantic Schemas ---
class CodeFile(BaseModel):
    path: str
    content: str

class CodebaseUpload(BaseModel):
    files: List[CodeFile]
    repo_url: Optional[str] = None

class ReviewTrigger(BaseModel):
    id: str

class ReviewResults(BaseModel):
    documentation: dict
    debt: list
    improvement: list
    critical: list

# --- In-memory storage for prototype ---
codebases = {}
reviews = {}

# --- Endpoint: /upload_codebase ---
@mcp.tool
def upload_codebase(codebase: CodebaseUpload) -> dict:
    """
    Accepts a codebase upload (simulated as a list of files). Enforces 500MB limit. Returns codebase ID.
    """
    # Simulate file size check (assume each file is 1MB for prototype)
    if len(codebase.files) > 500:
        return {"error": "Payload too large. Max 500MB allowed."}
    codebase_id = f"cb_{len(codebases)+1}"
    codebases[codebase_id] = codebase
    return {"status": "uploaded", "id": codebase_id}

# --- Endpoint: /trigger_review ---
@mcp.tool
def trigger_review(payload: ReviewTrigger) -> dict:
    """
    Triggers review for a given codebase ID. Returns review ID.
    """
    if payload.id not in codebases:
        return {"error": "Codebase not found.", "code": 404}
    review_id = f"rv_{len(reviews)+1}"
    # Placeholder agent outputs
    reviews[review_id] = {
        "documentation": {"README.md": "Sample README"},
        "debt": [{"type": "debt", "severity": "low", "description": "Sample debt", "file": "main.py", "line": 1, "suggestion": "Refactor"}],
        "improvement": [{"type": "improvement", "severity": "medium", "description": "Sample improvement", "file": "main.py", "line": 2, "suggestion": "Optimize"}],
        "critical": [{"type": "critical", "severity": "high", "description": "Sample critical issue", "file": "main.py", "line": 3, "remediation": "Fix immediately"}]
    }
    return {"status": "review_started", "id": review_id}

# --- Endpoint: /get_results ---
@mcp.tool
def get_results(id: str) -> dict:
    """
    Returns review results for a given review ID.
    """
    if id not in reviews:
        return {"error": "Review not found.", "code": 404}
    return reviews[id]

if __name__ == "__main__":
    mcp.run()
