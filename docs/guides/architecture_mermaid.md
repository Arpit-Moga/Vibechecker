# Modular Static+LLM Code Analysis Architecture

```mermaid
flowchart TD
    A[Codebase] -->|Parallel| B(Ruff Plugin)
    A -->|Parallel| C(Bandit Plugin)
    A -->|Parallel| D(mypy Plugin)
    A -->|Parallel| E(Semgrep Plugin)
    B & C & D & E --> F[Results Aggregator]
    F -->|Batch| G[LLM Plugin]
    G --> H[Final Report]
```

- Plugins are modular and language-agnostic.
- Orchestrator manages plugin execution, aggregation, and config.
- LLM plugin can explain, triage, or propose fixes for findings.
- Caching and batching optimize performance.