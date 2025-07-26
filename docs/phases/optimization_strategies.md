# Prompt Optimization Strategies

This document details explicit strategies for prompt engineering and optimization for all agents, strictly following architecture.md and best practices.

---

## Versioning & Reproducibility
- All prompt templates are versioned (see prompt_templates.md).
- Changes to prompts are tracked and documented for reproducibility.
- Use template variables for codebase metadata, file structure, and checklists.

## Feedback Loops
- Incorporate agent output feedback to refine prompts (e.g., if output is incomplete or invalid, adjust prompt and retry).
- Use LangChain memory to store previous outputs and context for iterative improvement.
- Log prompt changes and outcomes for auditability.

## Chain-of-Thought Reasoning
- For complex tasks (e.g., technical debt detection, critical issue identification), use chain-of-thought prompts:
  - Ask LLM to reason step-by-step before producing final output.
  - Example: "List all possible issues, then select the most critical and explain your reasoning."

## Error Handling & Fallbacks
- On LLM failure or invalid output, retry with simplified or more explicit prompt.
- Use prompt variants for edge cases (e.g., large codebases, ambiguous files).
- Document all fallback strategies and their triggers.

## Output Validation
- Always validate LLM output against pydantic schemas.
- If output fails validation, log error and retry with adjusted prompt.

## Best Practices
- Prompts must be explicit, unambiguous, and match output schemas.
- Use examples in prompts to guide LLM output format.
- Limit prompt length to avoid context window overflow; summarize codebase if needed.
- Reference open-source and enterprise documentation standards for prompt structure.

---

See prompt_templates.md for template details and agent_workflows.md for workflow integration.