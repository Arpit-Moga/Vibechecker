import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Minimal MCP Server")

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# In-memory storage for codebases and reviews (no persistence)
codebases = {}
reviews = {}

class CodeFile(BaseModel):
    path: str
    content: str

class Codebase(BaseModel):
    repo_url: Optional[str]
    files: List[CodeFile]

class ReviewRequest(BaseModel):
    id: str

@app.post("/upload_codebase")
async def upload_codebase(request: Request, codebase: UploadFile = File(...)):
    # Enforce file size limit
    contents = await codebase.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Payload too large. Max 500MB allowed.")
    # Simulate storing codebase
    codebase_id = f"cb_{len(codebases)+1}"
    codebases[codebase_id] = contents  # Placeholder: store raw bytes
    return JSONResponse({"status": "uploaded", "id": codebase_id})

@app.post("/trigger_review")
async def trigger_review(req: ReviewRequest):
    codebase_id = req.id
    if codebase_id not in codebases:
        raise HTTPException(status_code=404, detail="Codebase not found.")
    # Simulate review process
    review_id = f"rv_{len(reviews)+1}"
    # Placeholder agent outputs
    reviews[review_id] = {
        "documentation": {"README.md": "Sample README content."},
        "debt": [
            {
                "type": "debt",
                "severity": "low",
                "description": "Sample technical debt issue.",
                "file": "main.py",
                "line": 10,
                "suggestion": "Refactor function.",
                "reference": "https://example.com/debt"
            }
        ],
        "improvement": [
            {
                "type": "improvement",
                "severity": "medium",
                "description": "Sample improvement opportunity.",
                "file": "utils.py",
                "line": 5,
                "suggestion": "Optimize loop.",
                "reference": "https://example.com/improvement"
            }
        ],
        "critical": [
            {
                "type": "critical",
                "severity": "high",
                "description": "Sample critical issue.",
                "file": "security.py",
                "line": 42,
                "remediation": "Fix authentication bug.",
                "reference": "https://example.com/critical"
            }
        ]
    }
    return JSONResponse({"status": "review_started", "id": review_id})

@app.get("/get_results")
async def get_results(id: str):
    if id not in reviews:
        raise HTTPException(status_code=404, detail="Review not found.")
    return JSONResponse(reviews[id])

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
