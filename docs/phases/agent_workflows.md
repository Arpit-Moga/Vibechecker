# DSPy & LangChain Agent Workflows

This document specifies the workflow for each agent as a DSPy/LangChain chain, strictly following architecture.md and best practices.

---

## Master Agent Workflow
1. **Input Parsing:** Receives review request, parses codebase ID and parameters.
2. **Agent Invocation:** Triggers Documentation, Debt, Improvement, and Critical Issue agents in sequence.
3. **Aggregation:** Collects outputs, validates against pydantic schemas.
4. **Error Handling:** Retries failed agent invocations up to 3 times; logs errors and returns partial results if persistent failure.
5. **Output:** Returns aggregated results in JSON format.

## Documentation Agent Workflow
1. **Input Parsing:** Parses codebase metadata and file structure.
2. **Prompt Construction:** Builds explicit prompt for documentation generation (see prompt_templates.md).
3. **LLM Invocation:** Calls LLM via DSPy/LangChain with constructed prompt.
4. **Output Validation:** Validates generated documentation against pydantic schema.
5. **Error Handling:** On failure, retries once with simplified prompt; logs errors.
6. **Output:** Returns markdown files, OpenAPI YAML, SVG/PNG diagrams.

## Debt Agent Workflow
1. **Input Parsing:** Parses codebase files and debt checklist.
2. **Prompt Construction:** Builds prompt for technical debt detection.
3. **LLM Invocation:** Calls LLM via DSPy/LangChain.
4. **Output Validation:** Validates output against DebtIssue schema.
5. **Error Handling:** Retries up to 2 times for transient failures; logs errors.
6. **Output:** Returns JSON array of debt issues.

## Improvement Agent Workflow
1. **Input Parsing:** Parses codebase files and improvement checklist.
2. **Prompt Construction:** Builds prompt for improvement suggestions.
3. **LLM Invocation:** Calls LLM via DSPy/LangChain.
4. **Output Validation:** Validates output against ImprovementIssue schema.
5. **Error Handling:** Retries up to 2 times for transient failures; logs errors.
6. **Output:** Returns JSON array of improvement suggestions.

## Critical Issue Agent Workflow
1. **Input Parsing:** Parses codebase files and critical issue checklist.
2. **Prompt Construction:** Builds prompt for critical issue detection.
3. **LLM Invocation:** Calls LLM via DSPy/LangChain.
4. **Output Validation:** Validates output against CriticalIssue schema.
5. **Error Handling:** Retries up to 2 times for transient failures; logs errors.
6. **Output:** Returns JSON array of critical issues.

---

## Workflow Details
- **Prompt Templates:** See prompt_templates.md for explicit templates.
- **Memory Usage:** LangChain memory used for context across steps (e.g., codebase summary, previous outputs).
- **Output Formats:** Strictly match pydantic schemas.
- **Testing:** All chains must be unit/integration tested.

---

See workflow diagrams in /docs/architecture/ for visual representation.