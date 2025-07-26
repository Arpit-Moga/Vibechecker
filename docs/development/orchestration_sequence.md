# Orchestration Sequence Diagram

This diagram illustrates the agent orchestration flow in the MCP server, strictly following architecture.md and best practices.

---

## Sequence Diagram (Markdown/ASCII)

```
User
  |
  | POST /trigger_review
  v
Master Agent
  |
  |---> Documentation Agent
  |         |
  |         |---> Output (validated)
  |
  |---> Debt Agent
  |         |
  |         |---> Output (validated)
  |
  |---> Improvement Agent
  |         |
  |         |---> Output (validated)
  |
  |---> Critical Issue Agent
  |         |
  |         |---> Output (validated)
  |
  |<--- Aggregates all outputs
  |
  |---> Validates, serializes, logs
  |
  |---> Returns results via /get_results
```

## Error Handling & Retry Logic
- On agent failure, master agent retries up to 2-3 times (exponential backoff).
- If persistent failure, logs error and returns partial results with error details.
- All errors are logged with timestamp, agent name, error code, and message.

## Diagram Notes
- For SVG/PNG rendering, use UML sequence diagram conventions.
- Each agent invocation is a distinct message arrow.
- Error/retry branches are shown as decision diamonds.

---

See orchestration_flow.md for full logic and standards.