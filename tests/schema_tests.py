import pytest
from pydantic import ValidationError
from mcp_server.schemas import (
    DocumentationOutput,
    DebtIssue, DebtOutput,
    ImprovementIssue, ImprovementOutput,
    CriticalIssue, CriticalOutput,
    ReviewResults
)

def test_documentation_output_valid():
    doc = DocumentationOutput(
        readme="# Project Title\n...",
        contributing="# Contributing\n...",
        code_of_conduct="# Code of Conduct\n...",
        api_docs="openapi: 3.0.0\n...",
        diagrams=["<svg>...</svg>", "diagram.png"],
        onboarding="# Onboarding Guide\n...",
        runbooks="# Runbook\n...",
        security="# Security\n...",
        changelog="# Changelog\n...",
        testing="# Testing\n...",
        dependencies="# Dependencies\n..."
    )
    assert doc.readme.startswith("# Project Title")

def test_documentation_output_invalid():
    with pytest.raises(ValidationError):
        DocumentationOutput(
            readme="# Project Title\n...",
            contributing=12345,  # Invalid: not a string
            code_of_conduct="# Code of Conduct\n..."
        )

def test_debt_issue_valid():
    issue = DebtIssue(
        type="debt",
        severity="high",
        description="Hardcoded credentials found.",
        file="src/app.py",
        line=42,
        suggestion="Use environment variables.",
        reference="https://docs.example.com/security"
    )
    assert issue.severity == "high"

def test_debt_issue_invalid():
    with pytest.raises(ValidationError):
        DebtIssue(
            type="debt",
            severity="critical",  # Invalid value
            description="...",
            file="src/app.py",
            line="forty-two",      # Invalid: not an int
            suggestion="..."
        )

def test_improvement_issue_valid():
    issue = ImprovementIssue(
        type="improvement",
        severity="medium",
        description="Refactor nested loops for readability.",
        file="src/utils.py",
        line=88,
        suggestion="Extract to helper function.",
        reference="https://docs.example.com/refactoring"
    )
    assert issue.type == "improvement"

def test_improvement_issue_invalid():
    with pytest.raises(ValidationError):
        ImprovementIssue(
            type="improvement",
            severity="low",
            description="...",
            file="src/utils.py"
            # Missing 'line' and 'suggestion'
        )

def test_critical_issue_valid():
    issue = CriticalIssue(
        type="critical",
        severity="high",
        description="SQL injection vulnerability detected.",
        file="src/db.py",
        line=12,
        remediation="Use parameterized queries.",
        reference="https://docs.example.com/sql-injection"
    )
    assert issue.type == "critical"

def test_critical_issue_invalid():
    with pytest.raises(ValidationError):
        CriticalIssue(
            type="critical",
            severity="medium",  # Invalid: must be 'high'
            description="...",
            file="src/db.py",
            line=12
            # Missing 'remediation'
        )
