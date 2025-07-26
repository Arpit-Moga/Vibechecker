# Contributing to Multi-Agent MCP Server

Thank you for your interest in contributing to the Multi-Agent MCP Server! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Agent Development](#agent-development)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/multi-agent-mcp-server.git`
3. Create a new branch for your feature: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites
- Python 3.10 or higher
- uv (recommended) or pip for package management

### Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
pip install -e .
```

### Environment Variables

Create a `.env` file in the project root:

```bash
MCP_MAX_FILE_SIZE=524288000
# Add other configuration as needed
```

## Project Structure

```
multi-agent-mcp-server/
├── src/multiagent_mcp_server/    # Main package
│   ├── agents/                   # Agent implementations
│   ├── workflows/                # DSPy and LangChain workflows
│   ├── validation/               # Output validation
│   └── server.py                 # MCP server implementation
├── docs/                         # Documentation
│   ├── guides/                   # User guides
│   ├── development/              # Development docs
│   ├── api/                      # API documentation
│   └── phases/                   # Project phases
├── examples/                     # Usage examples
├── tests/                        # Test suite
├── data/                         # Data files and samples
└── scripts/                      # Utility scripts
```

## Code Style

- Follow PEP 8 for Python code style
- Use type hints for all function parameters and return values
- Use docstrings for all public functions and classes
- Maximum line length: 88 characters (Black formatter)

### Formatting

We use the following tools for code formatting and linting:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/multiagent_mcp_server

# Run specific test file
pytest tests/test_agents.py
```

### Writing Tests

- Write unit tests for all new functionality
- Use descriptive test names that explain what is being tested
- Mock external dependencies
- Test both success and failure scenarios

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Add or update tests for your changes
3. Update documentation if needed
4. Ensure all tests pass
5. Create a pull request with a clear title and description
6. Link any related issues

### Pull Request Template

Please include:

- **What**: Brief description of changes
- **Why**: Reason for the changes
- **How**: Technical approach used
- **Testing**: How the changes were tested
- **Documentation**: Any documentation updates

## Agent Development

### Creating a New Agent

1. Create a new file in `src/multiagent_mcp_server/agents/`
2. Inherit from the base `Agent` class
3. Implement required methods:
   - `analyze()` - Main analysis logic
   - `validate_output()` - Output validation
4. Add corresponding tests
5. Update documentation

### Agent Guidelines

- Each agent should have a single, well-defined responsibility
- Use consistent output formats across agents
- Implement proper error handling
- Add comprehensive logging
- Follow the established patterns in existing agents

### Example Agent Structure

```python
from typing import Dict, Any
from .base import Agent

class YourAgent(Agent):
    \"\"\"Agent for [specific purpose].\"\"\"
    
    def analyze(self, codebase: str) -> Dict[str, Any]:
        \"\"\"Analyze codebase and return findings.\"\"\"
        # Implementation here
        pass
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        \"\"\"Validate agent output format.\"\"\"
        # Validation logic here
        pass
```

## Documentation

- Update relevant documentation for any user-facing changes
- Use clear, concise language
- Include code examples where appropriate
- Update the changelog for notable changes

## Questions?

If you have questions or need help:

1. Check existing documentation
2. Search through existing issues
3. Create a new issue with the `question` label
4. Join our community discussions

Thank you for contributing!
