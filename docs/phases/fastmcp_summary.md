# FastMCP Architecture & Best Practices

This summary provides a comprehensive guide to building, configuring, and securing a Model Context Protocol (MCP) server using the FastMCP framework, strictly following project standards.

---

## 1. Initializing a FastMCP Server

### Required Imports and Instantiation

```python
from fastmcp import FastMCP

mcp = FastMCP(name="CodeReviewServer")

if __name__ == "__main__":
    mcp.run()
```

### Key Configuration Options
- `name`: Human-readable server name
- `instructions`: Description for clients
- `on_duplicate_tools`: Behavior for duplicate tool names ('error', 'warn', 'replace', 'ignore')
- `mask_error_details`: Hide detailed exception messages for security

Example:
```python
mcp = FastMCP(
    name="SecureCodeReviewServer",
    instructions="This server provides tools to analyze and review codebases.",
    on_duplicate_tools="error",
    mask_error_details=True
)
```

---

## 2. Defining Endpoints

Endpoints are implemented as tools and resources in FastMCP. For REST-like behavior, use:

### `/upload_codebase` (POST)
- Accepts multipart/form-data, field: `codebase` (zip/tar/directory)
- Max file size: 500MB
- Success: `{ "status": "uploaded", "id": "<codebase_id>" }`
- Errors: 400, 413, 500

### `/trigger_review` (POST)
- Accepts JSON `{ "id": "<codebase_id>" }`
- Triggers all agents (Documentation, Debt, Improvement, Critical Issue)
- Success: `{ "status": "review_started", "id": "<review_id>" }`
- Errors: 400, 404, 500

### `/get_results` (GET)
- Query param: `id=<review_id>`
- Returns all agent outputs in JSON, validated by pydantic schemas
- Success: `{ "documentation": {...}, "debt": [...], "improvement": [...], "critical": [...] }`
- Errors: 400, 404, 500

---

## 3. Agent Orchestration & Error Handling
- Master agent orchestrates workflow, delegates to specialized agents, aggregates outputs, handles errors/retries, logs actions.
- Use placeholder agent logic for prototype (static sample outputs matching pydantic schemas).

---

## 4. Security Features
- Enforce file size limits (500MB)
- Input validation using pydantic models
- Mask error details in responses if configured
- Return documented error codes/messages for all failure cases

---

## 5. Best Practices
- Use pydantic for payload validation and output serialization
- Document all endpoints, payloads, error codes, and sample requests/responses
- Follow standards in architecture.md for schemas and agent outputs
- Reference top open-source project documentation for clarity and completeness

---

## 6. Example Code Snippet: Tool Definition

```python
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List

mcp = FastMCP(name="CodeReviewServer")

class CodeFile(BaseModel):
    path: str
    content: str

class Codebase(BaseModel):
    repo_url: str
    files: List[CodeFile]

@mcp.tool
def analyze_codebase(codebase: Codebase) -> dict:
    """
    Analyzes a given codebase for quality and returns a summary.
    """
    num_files = len(codebase.files)
    return {"num_files": num_files, "summary": "Static output for prototype."}
```

---

## References
- See architecture.md for endpoint specs and schemas
- See endpoint_spec.md and protocol_compliance.md for detailed endpoint documentation
- See reference_index.md for professional documentation standards

---

*Strictly follow all standards and specifications. No ambiguity or deferred decisions permitted.*
