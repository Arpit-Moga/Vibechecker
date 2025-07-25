from typing import List
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport

import os
from langchain_google_genai import ChatGoogleGenerativeAI

def review_critical_with_gemini(issues):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = "You are an expert security reviewer. Review the following critical issues for severity, risk, and remediation quality. Provide a detailed review and suggestions for improvement.\n\n"
    for issue in issues:
        prompt += f"- {issue.description} (File: {issue.file}, Line: {issue.line}, Severity: {issue.severity})\nRemediation: {issue.remediation}\nReference: {issue.reference}\n\n"
    result = llm.invoke(prompt)
    return result.content

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
    review = review_critical_with_gemini(issues)
    try:
        report = AgentReport(issues=issues, review=review)
    except ValidationError as e:
        raise RuntimeError(f"Critical agent output validation failed: {e}")
    return report
