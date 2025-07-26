# Agent Workflow Diagrams

This file contains workflow diagrams for each agent’s DSPy/LangChain chain, strictly following architecture.md and best practices.

---

## Master Agent Workflow (Markdown/ASCII)
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

## Documentation Agent Workflow
```
Input Parsing
  |
Prompt Construction
  |
LLM Invocation (DSPy/LangChain)
  |
Output Validation (pydantic)
  |
Error Handling & Retry
  |
Output (Markdown, YAML, Diagrams)
```

## Debt/Improvement/Critical Agent Workflow
```
Input Parsing
  |
Prompt Construction
  |
LLM Invocation (DSPy/LangChain)
  |
Output Validation (pydantic)
  |
Error Handling & Retry
  |
Output (JSON array of issues)
```

---

## Diagram Notes
- For SVG/PNG rendering, use UML activity diagram conventions.
- Each workflow step is a node; arrows indicate flow.
- Error/retry branches are shown as decision diamonds.

---

See agent_workflows.md for written workflow specs.