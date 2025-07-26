"""Pytest configuration and shared fixtures."""

import pytest
from typing import Dict, Any
import tempfile
import os


@pytest.fixture
def sample_codebase():
    """Sample codebase for testing."""
    return {
        "main.py": """
def hello(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    hello("World")
""",
        "utils.py": """
def add(a, b):
    return a + b

def divide(a, b):
    return a / b  # Potential division by zero
""",
        "README.md": "# Sample Project\n\nThis is a sample project for testing."
    }


@pytest.fixture
def temp_codebase_dir(sample_codebase):
    """Create a temporary directory with sample codebase."""
    with tempfile.TemporaryDirectory() as tmpdir:
        for filename, content in sample_codebase.items():
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        yield tmpdir


@pytest.fixture
def mock_agent_output():
    """Mock agent output for testing."""
    return {
        "agent_type": "test_agent",
        "findings": [
            {
                "type": "issue",
                "severity": "medium",
                "description": "Test issue",
                "file": "test.py",
                "line": 1
            }
        ],
        "summary": "Test analysis complete",
        "metadata": {
            "analysis_time": 1.23,
            "files_analyzed": 2
        }
    }


@pytest.fixture
def api_client():
    """Test client for API testing."""
    from fastapi.testclient import TestClient
    from multiagent_mcp_server.server import app
    return TestClient(app)
