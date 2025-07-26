# Performance Optimization Guide

## Parallel Execution

- The orchestrator runs static analysis plugins in parallel using ThreadPoolExecutor.
- Each tool processes files independently, minimizing total scan time.

## Batching for LLM

- LLM plugin supports batching findings to reduce API calls and latency.
- Batch size is configurable in the LLM plugin interface.

## Caching

- Results for unchanged files are cached using file hashes (see [`cache_utils.py`](src/multiagent_mcp_server/cache_utils.py:1)).
- Only changed files are rescanned, reducing redundant computation.

## Scan Modes

- "Quick" mode runs only the fastest tools (Ruff, Bandit).
- "Deep" mode runs all tools and LLM, which is slower but more thorough.

## Asynchronous Execution

- Tools can be configured to run synchronously or asynchronously.
- LLM analysis can be deferred or run in the background for CI/CD use cases.

## Recommendations

- Use "quick" mode for pre-commit or local development.
- Use "deep" mode for CI, PRs, or nightly scans.
- Tune batch size and tool selection in config for your workflow.
