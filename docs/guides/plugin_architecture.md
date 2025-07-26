# Plugin Architecture Guide

## Overview

This project uses a modular, plugin-based architecture for static and LLM-powered code analysis. Each tool (Ruff, Bandit, mypy, Semgrep, LLM) is a plugin with a common interface, enabling easy extensibility and parallel orchestration.

---

## Static Analysis Plugin Interface

See [`plugin_interface.py`](src/multiagent_mcp_server/plugin_interface.py:1).

- All static analysis tools must implement `StaticAnalysisPlugin`.
- Required methods: `name()`, `supported_languages()`, `run(files, config)`.

---

## LLM Plugin Interface

See [`llm_plugin.py`](src/multiagent_mcp_server/llm_plugin.py:1).

- All LLM integrations must implement `LLMPlugin`.
- Required methods: `name()`, `explain_findings(findings, code, batch_size)`, `propose_fixes(findings, code, batch_size)`.

---

## Orchestrator

See [`orchestrator.py`](src/multiagent_mcp_server/orchestrator.py:1).

- Registers and runs plugins in parallel.
- Aggregates and deduplicates results.
- Supports config for scan mode, tool selection, and execution type.

---

## Scan Configuration

See [`scan_config.py`](src/multiagent_mcp_server/scan_config.py:1).

- Defines "quick" and "deep" scan modes.
- Allows user overrides for tool selection and execution style.

---

## Result Caching

See [`cache_utils.py`](src/multiagent_mcp_server/cache_utils.py:1).

- Caches results for unchanged files using file hashes.

---

## Adding a New Tool or Language

1. Implement the plugin interface for your tool.
2. Register the plugin with the orchestrator.
3. Update scan config if needed.

---

## Example Workflow

1. User triggers scan.
2. Orchestrator loads plugins based on config.
3. Plugins run in parallel; results are normalized and cached.
4. LLM plugin (if enabled) explains or triages findings.
5. Results are merged and presented.

---

## Mermaid Diagram

```mermaid
flowchart TD
    A[Codebase] -->|Parallel| B(Ruff Plugin)
    A -->|Parallel| C(Bandit Plugin)
    A -->|Parallel| D(mypy Plugin)
    A -->|Parallel| E(Semgrep Plugin)
    B & C & D & E --> F[Results Aggregator]
    F -->|Batch| G[LLM Plugin]
    G --> H[Final Report]