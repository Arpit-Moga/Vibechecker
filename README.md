# Multi-Agent MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A production-ready, modular multi-agent server for automated codebase review, documentation, and improvement. Built with the Model Context Protocol (MCP) for seamless integration with AI development workflows.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for documentation, technical debt, improvements, and critical issue detection
- **MCP Integration**: Full Model Context Protocol support for AI tool integration
- **Workflow Orchestration**: Advanced DSPy and LangChain workflow integration
- **Strict Validation**: Comprehensive output validation with Pydantic schemas
- **RESTful API**: Clean HTTP endpoints for codebase upload, review triggering, and result retrieval
- **Production Ready**: Docker support, comprehensive testing, and professional packaging

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Python Package (Recommended)

```bash
# Using uv (recommended)
uv add multiagent-mcp-server

# Using pip
pip install multiagent-mcp-server
```

### From Source

```bash
# Clone the repository
git clone https://github.com/your-org/multi-agent-mcp-server.git
cd multi-agent-mcp-server

# Install with uv
uv sync

# Or with pip
pip install -e .
```

### Docker

```bash
# Build the image
docker build -t multiagent-mcp-server .

# Run the container
docker run -p 8080:8080 multiagent-mcp-server
```

## 🚦 Quick Start

### Start the Server

```bash
# Using the installed package
multiagent-mcp-server

# Or using Python module
python -m multiagent_mcp_server.server
```

### Basic Usage

```python
import httpx

# Upload a codebase
files = {"codebase": open("your_project.zip", "rb")}
response = httpx.post("http://localhost:8080/upload_codebase", files=files)
codebase_id = response.json()["id"]

# Trigger review
review_response = httpx.post(
    "http://localhost:8080/trigger_review", 
    json={"id": codebase_id}
)
review_id = review_response.json()["review_id"]

# Get results
results = httpx.get(f"http://localhost:8080/get_results?id={review_id}")
print(results.json())
```

## 📚 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload_codebase` | Upload a codebase for analysis |
| `POST` | `/trigger_review` | Start multi-agent review process |
| `GET` | `/get_results` | Retrieve analysis results |
| `GET` | `/health` | Health check endpoint |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_MAX_FILE_SIZE` | `524288000` | Maximum file size for uploads (bytes) |
| `MCP_PORT` | `8080` | Server port |
| `MCP_HOST` | `0.0.0.0` | Server host |

## 📖 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[Getting Started Guide](docs/guides/getting_started.md)** - Quick start tutorial
- **[API Documentation](docs/api/)** - Detailed API reference
- **[Architecture Guide](docs/development/architecture.md)** - System architecture overview
- **[Development Guide](docs/development/)** - Development setup and guidelines
- **[Agent Documentation](docs/phases/)** - Agent-specific documentation

## 🔧 Development

### Prerequisites

- Python 3.10 or higher
- uv or pip for package management

### Setup

```bash
# Clone and setup
git clone https://github.com/your-org/multi-agent-mcp-server.git
cd multi-agent-mcp-server
uv sync

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=src/multiagent_mcp_server
```

### Project Structure

```
multi-agent-mcp-server/
├── src/multiagent_mcp_server/    # Main package
├── docs/                         # Documentation
├── examples/                     # Usage examples
├── tests/                        # Test suite
├── data/                         # Sample data and outputs
└── scripts/                      # Utility scripts
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [DSPy](https://github.com/stanfordnlp/dspy) and [LangChain](https://github.com/langchain-ai/langchain)
- Validation with [Pydantic](https://pydantic.dev/)

---

**[📚 Documentation](docs/)** • **[🐛 Issues](https://github.com/your-org/multi-agent-mcp-server/issues)** • **[💬 Discussions](https://github.com/your-org/multi-agent-mcp-server/discussions)**

## License
MIT
