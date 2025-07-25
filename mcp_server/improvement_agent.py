from typing import List
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport

def run_improvement_agent(codebase_path: str) -> AgentReport:
    # Simulate scanning codebase for improvements
    issues = [
        IssueOutput(
            type="improvement",
            severity="high",
            description="Function 'sort_items' in 'items.py' uses bubble sort.",
            file="items.py",
            line=15,
            suggestion="Replace with a more efficient sorting algorithm.",
            reference="/docs/criteria/improvement_checklist.md#algorithms"
        ),
        IssueOutput(
            type="improvement",
            severity="medium",
            description="API endpoint '/get_user' lacks documentation.",
            file="api.py",
            line=88,
            suggestion="Add endpoint documentation.",
            reference="/docs/criteria/improvement_checklist.md#documentation"
        ),
    ]
    try:
        report = AgentReport(issues=issues)
    except ValidationError as e:
        raise RuntimeError(f"Improvement agent output validation failed: {e}")
    return report
