# Agent Input/Output Interfaces

This document specifies the input and output formats, error handling, and retry logic for all agents in the Multi-Agent Code Review MCP Server, strictly following architecture.md.

---

## Master Agent
- **Input:**
  - JSON object containing codebase ID and review parameters.
  - Example: `{ "id": "<codebase_id>", "params": { ... } }`
- **Output:**
  - Aggregated JSON object containing outputs from all agents.
  - Example: `{ "documentation": {...}, "debt": [...], "improvement": [...], "critical": [...] }`
- **Error Handling:**
  - Returns error codes and messages as per MCP server endpoints (400, 404, 413, 500).
  - Retries failed agent invocations up to 3 times with exponential backoff.

## Documentation Agent
- **Input:**
  - JSON object with codebase metadata and file structure.
  - Example: `{ "codebase": { "files": [...], "metadata": {...} } }`
- **Output:**
  - Markdown files for documentation (README.md, CONTRIBUTING.md, etc.), OpenAPI YAML, SVG/PNG diagrams.
  - Example: `{ "README.md": "...", "swagger.yaml": "...", "diagram.svg": "..." }`
- **Error Handling:**
  - Returns error message in markdown if documentation cannot be generated.
  - Retries once with simplified prompt if LLM fails.

## Debt Agent
- **Input:**
  - JSON object with codebase files and explicit debt checklist.
  - Example: `{ "files": [...], "checklist": [...] }`
- **Output:**
  - JSON array of debt issues, validated by pydantic.
  - Example: `[ { "type": "debt", "severity": "high", "description": "...", "file": "...", "line": 42, "suggestion": "...", "reference": "..." }, ... ]`
- **Error Handling:**
  - Returns error code 400 for invalid input, 500 for internal errors.
  - Retries up to 2 times for transient failures.

## Improvement Agent
- **Input:**
  - JSON object with codebase files and improvement checklist.
  - Example: `{ "files": [...], "checklist": [...] }`
- **Output:**
  - JSON array of improvement suggestions, validated by pydantic.
  - Example: `[ { "type": "improvement", "severity": "medium", "description": "...", "file": "...", "line": 88, "suggestion": "...", "reference": "..." }, ... ]`
- **Error Handling:**
  - Returns error code 400 for invalid input, 500 for internal errors.
  - Retries up to 2 times for transient failures.

## Critical Issue Agent
- **Input:**
  - JSON object with codebase files and critical issue checklist.
  - Example: `{ "files": [...], "checklist": [...] }`
- **Output:**
  - JSON array of critical issues, validated by pydantic.
  - Example: `[ { "type": "critical", "severity": "high", "description": "...", "file": "...", "line": 12, "remediation": "...", "reference": "..." }, ... ]`
- **Error Handling:**
  - Returns error code 400 for invalid input, 500 for internal errors.
  - Retries up to 2 times for transient failures.

---

All input/output formats must be strictly validated against pydantic schemas. All error codes and retry logic must be logged and documented.