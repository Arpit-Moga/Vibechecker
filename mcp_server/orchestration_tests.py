import pytest
from mcp_server.orchestration import orchestrate_review

def test_orchestrate_review_success():
    dummy_codebase = b"print('hello world')"
    results = orchestrate_review(dummy_codebase)
    assert "documentation" in results
    assert "debt" in results
    assert "improvement" in results
    assert "critical" in results
    assert isinstance(results["documentation"], dict)
    assert isinstance(results["debt"], list)
    assert isinstance(results["improvement"], list)
    assert isinstance(results["critical"], list)

def test_orchestrate_review_agent_error(monkeypatch):
    def fail_agent(_):
        raise Exception("Agent failed!")
    dummy_codebase = b"print('hello world')"
    # Patch documentation_agent to fail
    from mcp_server import orchestration
    monkeypatch.setattr(orchestration, "documentation_agent", fail_agent)
    results = orchestration.orchestrate_review(dummy_codebase)
    assert "error" in results["documentation"]
    # Other agents should still succeed
    assert isinstance(results["debt"], list)
    assert isinstance(results["improvement"], list)
    assert isinstance(results["critical"], list)
