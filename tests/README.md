# Tests

This directory contains the test suite for the Multi-Agent MCP Server.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for workflows and APIs
- `fixtures/` - Test fixtures and sample data
- `conftest.py` - Pytest configuration and shared fixtures

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/multiagent_mcp_server

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Run with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_agent"
```

## Test Guidelines

- Write descriptive test names that explain what is being tested
- Use fixtures for common test data and setup
- Mock external dependencies
- Test both success and failure scenarios
- Maintain high test coverage (aim for >90%)

## Test Categories

### Unit Tests
- Individual agent functionality
- Validation logic
- Utility functions
- Schema validation

### Integration Tests
- API endpoint functionality
- End-to-end workflows
- Agent orchestration
- File processing pipelines
