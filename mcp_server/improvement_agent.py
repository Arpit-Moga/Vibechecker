from typing import List
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport

import os
from langchain_google_genai import ChatGoogleGenerativeAI

def review_improvement_with_gemini(issues):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = "You are an expert code reviewer. Review the following improvement suggestions for impact, feasibility, and clarity. Provide a detailed review and suggestions for improvement.\n\n"
    for issue in issues:
        prompt += f"- {issue.description} (File: {issue.file}, Line: {issue.line}, Severity: {issue.severity})\nSuggestion: {issue.suggestion}\nReference: {issue.reference}\n\n"
    result = llm.invoke(prompt)
    return result.content

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
    review = review_improvement_with_gemini(issues)
    try:
        report = AgentReport(issues=issues, review=review)
    except ValidationError as e:
        raise RuntimeError(f"Improvement agent output validation failed: {e}")
    return report
