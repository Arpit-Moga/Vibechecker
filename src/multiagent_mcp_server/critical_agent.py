"""
Production-ready critical issue reviewer using DSPy and Pydantic.

This module provides a robust critical issue review system that:
- Analyzes critical issues and generates a detailed review
- Uses DSPy for LLM calls and composable modules
- Provides validation and error handling
- Supports multiple LLM providers with fallback
"""

import logging
import os
from typing import List, Optional
from pydantic import ValidationError
from multiagent_mcp_server.models import IssueOutput, AgentReport
import dspy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pathlib import Path
from multiagent_mcp_server.agent_utils import SupportedFileType, Settings, CodeFile, FileProcessor

class CriticalIssueReviewSignature(dspy.Signature):
    """DSPy signature for critical issue review."""
    issues: str = dspy.InputField(
        desc="List of critical issues with file, line, severity, description, remediation, and reference."
    )
    review_report: str = dspy.OutputField(
        desc="Detailed review report with severity, risk, remediation quality, and improvement suggestions."
    )

class CriticalIssueDetectionSignature(dspy.Signature):
    """DSPy signature for LLM-based critical issue detection."""
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    prompt: str = dspy.InputField(desc="Explicit instructions for LLM.")
    issues: str = dspy.OutputField(desc="Detected critical issues in IssueOutput format.")

class CriticalIssueDetector(dspy.Module):
    """DSPy module for LLM-based critical issue detection."""
    def __init__(self):
        super().__init__()
        self.detect = dspy.ChainOfThought(CriticalIssueDetectionSignature)
    def forward(self, code: str, filename: str) -> str:
        # Prompt for genuinely critical issues only
        prompt = (
            "You are a senior code reviewer. For every issue you find, rank and sort it by the real-world damage it could cause. Use severity 'high' for catastrophic issues (loss of files/data, security exploits, compliance violations, remote code execution, hardcoded secrets, etc.), 'medium' for major functional failures (application crashes, unhandled exceptions), and 'low' for minor bugs (not working code, incorrect datatypes, small inefficiencies, style issues). For each issue, include a brief justification for its ranking. Only use type 'critical' for the highest-impact issues (must be severity 'high'). Use type 'debt' or 'improvement' for lower-impact issues. If you are unsure about the severity or impact, include the issue and explain your reasoning. Output valid JSON as a list of IssueOutput objects, sorted from highest to lowest impact. Each issue must include: type ('critical', 'debt', or 'improvement'), severity ('low', 'medium', 'high'), description, file, line, specific actionable remediation (for critical) or suggestion (for debt/improvement), a relevant code snippet (3-5 lines), and a justification for its ranking. If there are no issues at all, output an empty list."
        )
        try:
            result = self.detect(code=code, filename=filename, prompt=prompt)
            return result.issues
        except Exception as e:
            logger.error(f"Error in LLM-based critical issue detection for {filename}: {e}")
            return ""

class CriticalIssueReviewer(dspy.Module):
    """DSPy module for reviewing critical issues."""
    def __init__(self):
        super().__init__()
        self.review = dspy.ChainOfThought(CriticalIssueReviewSignature)
    def forward(self, issues: str) -> str:
        try:
            result = self.review(issues=issues)
            return result.review_report
        except Exception as e:
            logger.error(f"Error reviewing critical issues: {e}")
            return f"Review failed: {e}"

class CriticalAgent:
    """Main critical issue review agent."""
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._setup_dspy()
        self.reviewer = CriticalIssueReviewer()
    def _setup_dspy(self):
        try:
            if self.settings.google_api_key:
                dspy.configure(lm=dspy.LM(
                    model="gemini/gemini-2.5-flash",
                    api_key=self.settings.google_api_key
                ))
                logger.info("Configured DSPy with Gemini")
            elif self.settings.openai_api_key:
                dspy.configure(lm=dspy.LM(
                    model="openai/gpt-3.5-turbo",
                    api_key=self.settings.openai_api_key
                ))
                logger.info("Configured DSPy with OpenAI")
            else:
                logger.warning("No API keys found, using default DSPy configuration")
        except Exception as e:
            logger.error(f"Failed to configure DSPy: {e}")
            raise RuntimeError(f"LLM configuration failed: {e}")
    def _format_issues(self, issues: List[IssueOutput]) -> str:
        formatted = []
        for issue in issues:
            formatted.append(
                f"- {issue.description} (File: {issue.file}, Line: {issue.line}, Severity: {issue.severity})\nRemediation: {issue.remediation}\nReference: {issue.reference}\n"
            )
        return "\n".join(formatted)
    def review_critical_issues(self, issues: List[IssueOutput]) -> str:
        issues_str = self._format_issues(issues)
        return self.reviewer.forward(issues=issues_str)


    # Heuristic detection removed: now fully LLM-based

    def run(self) -> AgentReport:
        code_dir = Path(self.settings.code_directory)
        if not code_dir.exists():
            raise RuntimeError(f"Code directory not found: {code_dir}")
        code_files = FileProcessor(self.settings).get_code_files(code_dir)
        # LLM-based detection only
        detector = CriticalIssueDetector()
        llm_issues = []
        import json
        for file in code_files.values():
            llm_result = detector.forward(code=file.content, filename=file.name)
            # Try to parse LLM output as IssueOutput list
            try:
                parsed = json.loads(llm_result)
                for issue in parsed:
                    llm_issues.append(IssueOutput(**issue))
            except Exception:
                # If not JSON, fallback: ignore malformed output
                logger.warning(f"Malformed LLM output for {file.name}, skipping.")
        # Deduplicate issues (optional, can be removed if you want all raw LLM output)
        unique_issues = llm_issues
        if not unique_issues:
            logger.info("No critical issues detected.")
        review = self.review_critical_issues(unique_issues)
        try:
            report = AgentReport(issues=unique_issues, review=review)
        except ValidationError as e:
            logger.error(f"Critical agent output validation failed: {e}")
            raise RuntimeError(f"Critical agent output validation failed: {e}")
        return report


def _create_code_summary(code_files: dict) -> str:
    summary_parts = []
    summary_parts.append("## Project Structure Overview")
    summary_parts.append(f"Total files analyzed: {len(code_files)}")
    summary_parts.append("\n### File List:")
    for code_file in code_files.values():
        summary_parts.append(f"- {code_file.name} ({code_file.size_bytes} bytes)")
    return "\n".join(summary_parts)

def main():
    """Main entry point for the critical issue reviewer."""
    try:
        settings = Settings()
        agent = CriticalAgent(settings)
        logger.info("Starting critical issue review...")
        code_dir = Path(settings.code_directory)
        code_files = FileProcessor(settings).get_code_files(code_dir)
        code_summary = _create_code_summary(code_files)
        output = agent.run()
        print("\n" + "="*80)
        print("CRITICAL ISSUE REVIEW COMPLETE")
        print("="*80)
        print(f"\n--- CODEBASE SUMMARY ---\n{code_summary}")
        for idx, issue in enumerate(output.issues, 1):
            print(f"\n--- Issue {idx} ---")
            print(f"Type: {issue.type}")
            print(f"Severity: {issue.severity}")
            print(f"Description: {issue.description}")
            print(f"File: {issue.file}")
            print(f"Line: {issue.line}")
            print(f"Remediation: {issue.remediation}")
            print(f"Reference: {issue.reference}")
        print(f"\n--- REVIEW REPORT ---")
        print(output.review)
        print(f"\n--- METADATA ---")
        print(f"total_files_processed: {len(code_files)}")
        print(f"issues_detected: {len(output.issues)}")
        print(f"code_directory: {settings.code_directory}")
        logger.info("Critical issue review completed successfully")
        return output
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()
