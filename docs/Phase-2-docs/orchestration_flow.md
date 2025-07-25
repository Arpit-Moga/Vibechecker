# Orchestration Logic: Multi-Agent MCP Server

This document specifies the orchestration logic for the master agent, including agent sequencing, message formats, error codes, fallback strategies, and logging requirements. All details strictly follow architecture.md.

---

## Agent Trigger Sequence
1. **Master Agent** receives a review request (`/trigger_review` endpoint).
2. **Documentation Agent** is triggered first; output is validated and stored.
3. **Debt Agent** is triggered next; output is validated and stored.
4. **Improvement Agent** is triggered next; output is validated and stored.
5. **Critical Issue Agent** is triggered last; output is validated and stored.
6. **Master Agent** aggregates all outputs, validates against pydantic schemas, and serializes for `/get_results`.

## Message Formats
- All inter-agent communication uses JSON objects validated by pydantic schemas.
- Example message to agent:
  ```json
  {
    "codebase": { "files": [...], "metadata": {...} },
    "checklist": [...]
  }
  ```
- Example agent output:
  ```json
  [
    {
      "type": "debt",
      "severity": "high",
      "description": "...",
      "file": "...",
      "line": 42,
      "suggestion": "...",
      "reference": "..."
    }
  ]
  ```

## Error Codes & Fallback Strategies
- All endpoints and agent invocations must handle and propagate error codes:
  - 400: Bad request (invalid input)
  - 404: Not found (codebase/review missing)
  - 413: Payload too large
  - 500: Internal server error
- On agent failure:
  - Retry up to 2-3 times (see agent_interfaces.md for specifics) with exponential backoff.
  - If persistent failure, log error and return partial results with error details.
  - All errors must be logged with timestamp, agent name, error code, and message.

## Logging Requirements
- Every agent invocation, output, error, and retry must be logged.
- Logs must include:
  - Timestamp
  - Agent name
  - Input parameters
  - Output summary
  - Error codes/messages (if any)
  - Retry count
- Logs must be accessible for audit and debugging.

## Sequence Diagrams & Flowcharts
- See `/docs/architecture/` for visual diagrams of orchestration flow (to be created in Step 5).

---

All orchestration logic must be explicit, standards-compliant, and unambiguous. See architecture.md for all shared definitions.