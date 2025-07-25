# MCP Server Endpoints Documentation

## 1. /upload_codebase
- **Method:** POST
- **Payload:** multipart/form-data, field name `codebase` (zip/tar/directory)
- **Max file size:** 500MB
- **Response:**
  - Success: `{"status": "uploaded", "id": "<codebase_id>"}`
  - Error codes:
    - 400: Bad request (malformed payload)
    - 413: Payload too large (exceeds 500MB)
    - 500: Server error
- **Example Request:**
  ```bash
  curl -F "codebase=@project.zip" http://localhost:8000/upload_codebase
  ```
- **Example Response:**
  ```json
  {"status": "uploaded", "id": "cb_1"}
  ```

## 2. /trigger_review
- **Method:** POST
- **Payload:** JSON `{ "id": "<codebase_id>" }`
- **Response:**
  - Success: `{"status": "review_started", "id": "<review_id>"}`
  - Error codes:
    - 400: Bad request (malformed payload)
    - 404: Codebase not found
    - 500: Server error
- **Example Request:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"id": "cb_1"}' http://localhost:8000/trigger_review
  ```
- **Example Response:**
  ```json
  {"status": "review_started", "id": "rv_1"}
  ```

## 3. /get_results
- **Method:** GET
- **Query param:** `id=<review_id>`
- **Response:**
  - Success: `{"documentation": {...}, "debt": [...], "improvement": [...], "critical": [...]}`
  - Error codes:
    - 400: Bad request (malformed query)
    - 404: Review not found
    - 500: Server error
- **Example Request:**
  ```bash
  curl "http://localhost:8000/get_results?id=rv_1"
  ```
- **Example Response:**
  ```json
  {
    "documentation": {"README.md": "Sample README content."},
    "debt": [{"type": "debt", "severity": "low", "description": "Sample technical debt issue.", "file": "main.py", "line": 10, "suggestion": "Refactor function.", "reference": "https://example.com/debt"}],
    "improvement": [{"type": "improvement", "severity": "medium", "description": "Sample improvement opportunity.", "file": "utils.py", "line": 5, "suggestion": "Optimize loop.", "reference": "https://example.com/improvement"}],
    "critical": [{"type": "critical", "severity": "high", "description": "Sample critical issue.", "file": "security.py", "line": 42, "remediation": "Fix authentication bug.", "reference": "https://example.com/critical"}]
  }
  ```

## Error Handling
- All error responses are JSON: `{ "error": "<message>" }`
- Error codes and messages are strictly enforced per architecture.md
