"""
Unit tests for validation.py
Covers all models, edge cases, and error reporting
"""
import pytest
from mcp_server.models import DocumentationOutput, IssueOutput, AgentReport, AllAgentOutputs
from mcp_server.validation import OutputValidator

# --- DocumentationOutput tests ---
def test_documentation_output_valid():
    data = {
        "files": {f: "content" for f in [
            'README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
            'swagger.yaml', 'schema.graphql', 'architecture.svg',
            'ONBOARDING.md', 'RUNBOOK.md', 'SECURITY.md',
            'CHANGELOG.md', 'TESTING.md', 'DEPENDENCY.md', 'LICENSE'
        ]}
    }
    model = OutputValidator.validate_output(data, DocumentationOutput)
    assert isinstance(model, DocumentationOutput)

def test_documentation_output_missing_file():
    data = {"files": {"README.md": "content"}}
def test_documentation_output_missing_file():
    data = {"files": {"README.md": "content"}}
    with pytest.raises(RuntimeError) as e:
        OutputValidator.validate_output(data, DocumentationOutput)
    assert "Missing required documentation files" in str(e.value)
# --- IssueOutput tests ---
def test_issue_output_debt_valid():
    data = {
        "type": "debt",
        "severity": "low",
        "description": "Refactor needed",
        "file": "main.py",
        "line": 10,
        "suggestion": "Use function",
    }
    model = OutputValidator.validate_output(data, IssueOutput)
    assert model.type == "debt"

def test_issue_output_critical_missing_remediation():
    data = {
        "type": "critical",
        "severity": "high",
        "description": "Security flaw",
        "file": "server.py",
        "line": 42,
    }
def test_issue_output_critical_missing_remediation():
    data = {
        "type": "critical",
        "severity": "high",
        "description": "Security flaw",
        "file": "server.py",
        "line": 42,
    }
    with pytest.raises(RuntimeError) as e:
        OutputValidator.validate_output(data, IssueOutput)
    assert "remediation is required for critical issues" in str(e.value)

def test_issue_output_critical_severity():
    data = {
        "type": "critical",
        "severity": "low",
        "description": "Security flaw",
        "file": "server.py",
        "line": 42,
        "remediation": "Patch immediately"
    }
def test_issue_output_critical_severity():
    data = {
        "type": "critical",
        "severity": "low",
        "description": "Security flaw",
        "file": "server.py",
        "line": 42,
        "remediation": "Patch immediately"
    }
    with pytest.raises(RuntimeError) as e:
        OutputValidator.validate_output(data, IssueOutput)
    assert "Critical issues must have severity \"high\"" in str(e.value)
# --- AgentReport and AllAgentOutputs tests ---
def test_agent_report_valid():
    issue = {
        "type": "improvement",
        "severity": "medium",
        "description": "Optimize loop",
        "file": "utils.py",
        "line": 5,
        "suggestion": "Use list comprehension"
    }
    data = {"issues": [issue]}
    model = OutputValidator.validate_output(data, AgentReport)
    assert isinstance(model, AgentReport)
    assert model.issues[0].type == "improvement"

def test_all_agent_outputs_valid():
    doc_data = {
        "files": {f: "content" for f in [
            'README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
            'swagger.yaml', 'schema.graphql', 'architecture.svg',
            'ONBOARDING.md', 'RUNBOOK.md', 'SECURITY.md',
            'CHANGELOG.md', 'TESTING.md', 'DEPENDENCY.md', 'LICENSE'
        ]}
    }
    issue = {
        "type": "debt",
        "severity": "low",
        "description": "Refactor needed",
        "file": "main.py",
        "line": 10,
        "suggestion": "Use function"
    }
    agent_report = {"issues": [issue]}
    data = {
        "documentation": doc_data,
        "debt": agent_report,
        "improvement": agent_report,
        "critical": {"issues": []}
    }
    model = OutputValidator.validate_all_agents_output(data)
    assert isinstance(model, AllAgentOutputs)

def test_all_agent_outputs_invalid():
    data = {"documentation": {"files": {}}, "debt": {"issues": []}, "improvement": {"issues": []}, "critical": {"issues": []}}
def test_all_agent_outputs_invalid():
    data = {"documentation": {"files": {}}, "debt": {"issues": []}, "improvement": {"issues": []}, "critical": {"issues": []}}
    with pytest.raises(RuntimeError) as e:
        OutputValidator.validate_all_agents_output(data)
    assert "Missing required documentation files" in str(e.value)
# --- Serialization tests ---
def test_serialize_and_to_dict():
    doc_data = {
        "files": {f: "content" for f in [
            'README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
            'swagger.yaml', 'schema.graphql', 'architecture.svg',
            'ONBOARDING.md', 'RUNBOOK.md', 'SECURITY.md',
            'CHANGELOG.md', 'TESTING.md', 'DEPENDENCY.md', 'LICENSE'
        ]}
    }
    model = OutputValidator.validate_output(doc_data, DocumentationOutput)
    json_str = OutputValidator.serialize(model)
    dict_obj = OutputValidator.to_dict(model)
    assert isinstance(json_str, str)
    assert isinstance(dict_obj, dict)
