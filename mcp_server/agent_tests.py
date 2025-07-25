import pytest
from pydantic import ValidationError
from mcp_server.documentation_agent import run_documentation_agent
from mcp_server.debt_agent import run_debt_agent
from mcp_server.improvement_agent import run_improvement_agent
from mcp_server.critical_agent import run_critical_agent
from mcp_server.models import DocumentationOutput, AgentReport, IssueOutput

def test_documentation_agent_valid():
    output = run_documentation_agent()
    assert isinstance(output, DocumentationOutput)
    assert 'README.md' in output.files
    assert 'CONTRIBUTING.md' in output.files
    assert 'swagger.yaml' in output.files
    # Check required sections in README
    assert 'Multi-Agent MCP Server' in output.files['README.md']

def test_debt_agent_valid():
    report = run_debt_agent('dummy_path')
    assert isinstance(report, AgentReport)
    for issue in report.issues:
        assert issue.type == 'debt'
        assert issue.suggestion is not None
        assert issue.severity in ['low', 'medium', 'high']

def test_improvement_agent_valid():
    report = run_improvement_agent('dummy_path')
    assert isinstance(report, AgentReport)
    for issue in report.issues:
        assert issue.type == 'improvement'
        assert issue.suggestion is not None
        assert issue.severity in ['low', 'medium', 'high']

def test_critical_agent_valid():
    report = run_critical_agent('dummy_path')
    assert isinstance(report, AgentReport)
    for issue in report.issues:
        assert issue.type == 'critical'
        assert issue.remediation is not None
        assert issue.severity == 'high'

def test_debt_agent_missing_suggestion():
    with pytest.raises(ValidationError):
        IssueOutput(
            type="debt",
            severity="high",
            description="Missing suggestion field.",
            file="main.py",
            line=1
        )

def test_critical_agent_wrong_severity():
    with pytest.raises(ValidationError):
        IssueOutput(
            type="critical",
            severity="low",
            description="Critical issue with wrong severity.",
            file="main.py",
            line=1,
            remediation="Fix immediately."
        )

def test_improvement_agent_missing_suggestion():
    with pytest.raises(ValidationError):
        IssueOutput(
            type="improvement",
            severity="medium",
            description="Missing suggestion field.",
            file="api.py",
            line=2
        )

def test_critical_agent_missing_remediation():
    with pytest.raises(ValidationError):
        IssueOutput(
            type="critical",
            severity="high",
            description="Missing remediation field.",
            file="main.py",
            line=3
        )
