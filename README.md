# Multi-Agent MCP Server

## Overview
A modular, multi-agent server for automated codebase review, documentation, and improvement. Integrates specialized agents, strict output validation, and NPX packaging for easy CLI use.

## Features
- Upload codebase, trigger review, and get results via endpoints
- Specialized agents for documentation, debt, improvement, and critical issues
- DSPy and LangChain workflow integration
- Strict output validation with pydantic
- NPX/CLI packaging for easy distribution

## Installation
```bash
npm install -g multi-agent-mcp-server
```

## Usage
### CLI
```bash
npx mcp-server --upload path/to/codebase
npx mcp-server --trigger-review
npx mcp-server --get-results
```

### Python
```python
from mcp_server.validation import OutputValidator
# See validation_docs.md for details
```

## Development
- Run tests: `npm test` or `pytest mcp_server/`
- Entry point: `mcp_server/main.py`
- See [docs/Overview/Phase/Phase-3.md](docs/Overview/Phase/Phase-3.md) for full spec

## License
MIT
