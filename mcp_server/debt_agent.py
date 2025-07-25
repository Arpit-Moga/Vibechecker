from typing import List
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport

import os
from langchain_google_genai import ChatGoogleGenerativeAI

def review_debt_with_gemini(issues):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = "You are an expert code reviewer. Review the following technical debt issues for severity, impact, and remediation quality. Provide a detailed review and suggestions for improvement.\n\n"
    for issue in issues:
        prompt += f"- {issue.description} (File: {issue.file}, Line: {issue.line}, Severity: {issue.severity})\nSuggestion: {issue.suggestion}\nReference: {issue.reference}\n\n"
    result = llm.invoke(prompt)
    return result.content

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
    review = review_debt_with_gemini(issues)
    try:
        report = AgentReport(issues=issues, review=review)
    except ValidationError as e:
        raise RuntimeError(f"Debt agent output validation failed: {e}")
    return report