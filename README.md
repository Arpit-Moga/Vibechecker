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

### Python (Recommended for MCP Server)
```bash
# Clone repo
# Install dependencies
pip install -r requirements.txt
```

### Docker
```bash
# Build Docker image
docker build -t mcp-server .
# Run container
# (Expose port 80, override env vars as needed)
docker run -p 80:80 mcp-server
```

## Usage

### API Endpoints
- POST `/upload_codebase` (multipart/form-data, field: codebase)
- POST `/trigger_review` (json: {"id": "<codebase_id>"})
- GET `/get_results?id=<review_id>`

### Environment Variables
- `MCP_MAX_FILE_SIZE` (default: 524288000)

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
