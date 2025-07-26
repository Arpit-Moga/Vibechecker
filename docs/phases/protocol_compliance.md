# Protocol Compliance: Minimal MCP Server

This document details protocol compliance for all endpoints, including required headers, payload schemas, authentication, error codes, sample requests/responses, and a compliance checklist.

---

## 1. /upload_codebase
- **Method:** POST
- **Headers:**
  - `Content-Type: multipart/form-data`
- **Payload Schema:**
  - Field: `codebase` (zip/tar/directory)
  - Max file size: 500MB
- **Authentication:** None (prototype)
- **Error Codes:**
  - `400 Bad Request`: Malformed request
  - `413 Payload Too Large`: File exceeds 500MB
  - `500 Internal Server Error`: Unexpected failure
- **Sample Request:**
  ```bash
  curl -F "codebase=@project.zip" http://localhost:8000/upload_codebase
  ```
- **Sample Response:**
  ```json
  {"status": "uploaded", "id": "cb_1"}
  ```

---

## 2. /trigger_review
- **Method:** POST
- **Headers:**
  - `Content-Type: application/json`
- **Payload Schema:**
  ```json
  {"id": "cb_1"}
  ```
- **Authentication:** None (prototype)
- **Error Codes:**
  - `400 Bad Request`: Malformed request
  - `404 Not Found`: Codebase not found
  - `500 Internal Server Error`: Unexpected failure
- **Sample Request:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"id": "cb_1"}' http://localhost:8000/trigger_review
  ```
- **Sample Response:**
  ```json
  {"status": "review_started", "id": "rv_1"}
  ```

---

## 3. /get_results
- **Method:** GET
- **Headers:**
  - None required
- **Query Param:** `id=<review_id>`
- **Payload Schema:** None (GET request)
- **Authentication:** None (prototype)
- **Error Codes:**
  - `400 Bad Request`: Malformed request
  - `404 Not Found`: Review not found
  - `500 Internal Server Error`: Unexpected failure
- **Sample Request:**
  ```bash
  curl "http://localhost:8000/get_results?id=rv_1"
  ```
- **Sample Response:**
  ```json
  {
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
  ```

---

## Compliance Checklist
| Endpoint           | Payload Validation | File Size Limit | Error Codes | Output Schema | Auth | Notes |
|--------------------|-------------------|-----------------|-------------|--------------|------|-------|
| /upload_codebase   | Yes (multipart)   | Yes (500MB)     | Yes         | Yes          | No   | Strictly enforced |
| /trigger_review    | Yes (JSON)        | N/A             | Yes         | Yes          | No   | Strictly enforced |
| /get_results       | N/A (GET)         | N/A             | Yes         | Yes          | No   | Strictly enforced |

- All endpoints match MCP protocol standards as defined in Docs/architecture.md.
- All payloads and outputs validated using Pydantic models.
- All error codes and messages documented and tested.
- No ambiguity or deferred decisions permitted.
