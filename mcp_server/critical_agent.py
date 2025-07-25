from typing import List
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport

def run_critical_agent(codebase_path: str) -> AgentReport:
    # Simulate scanning codebase for critical issues
    issues = [
        IssueOutput(
            type="critical",
            severity="high",
            description="SQL injection vulnerability in 'db.py'.",
            file="db.py",
            line=120,
            remediation="Sanitize all SQL inputs and use parameterized queries.",
            reference="/docs/criteria/critical_checklist.md#sql-injection"
        ),
        IssueOutput(
            type="critical",
            severity="high",
            description="Unhandled exception in 'main.py' causing crash.",
            file="main.py",
            line=77,
            remediation="Add try/except block and proper error logging.",
            reference="/docs/criteria/critical_checklist.md#crash"
        ),
    ]
    try:
        report = AgentReport(issues=issues)
    except ValidationError as e:
        raise RuntimeError(f"Critical agent output validation failed: {e}")
    return report
