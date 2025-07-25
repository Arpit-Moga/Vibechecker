from typing import List
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport

def run_debt_agent(codebase_path: str) -> AgentReport:
    # Simulate scanning codebase for technical debt
    issues = [
        IssueOutput(
            type="debt",
            severity="high",
            description="Function 'process_data' in 'main.py' exceeds 100 lines.",
            file="main.py",
            line=42,
            suggestion="Refactor into smaller functions.",
            reference="/docs/criteria/debt_checklist.md#large-functions"
        ),
        IssueOutput(
            type="debt",
            severity="low",
            description="Variable 'x' in 'utils.py' is poorly named.",
            file="utils.py",
            line=10,
            suggestion="Rename variable to something descriptive.",
            reference="/docs/criteria/debt_checklist.md#naming"
        ),
    ]
    try:
        report = AgentReport(issues=issues)
    except ValidationError as e:
        raise RuntimeError(f"Debt agent output validation failed: {e}")
    return report
