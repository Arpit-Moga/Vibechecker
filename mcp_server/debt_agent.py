"""
Production-ready technical debt reviewer using DSPy and Pydantic.

This module provides a robust technical debt review system that:
- Analyzes codebase for technical debt issues using LLMs
- Uses DSPy for LLM calls and composable modules
- Provides validation and error handling
- Supports multiple LLM providers with fallback
"""

import logging
import os
from typing import List, Optional
from pydantic import ValidationError
from mcp_server.models import IssueOutput, AgentReport
import dspy
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupportedFileType(str, Enum):
    PYTHON = ".py"

class Settings:
    """Settings for agent configuration."""
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    code_directory: str = os.getenv("CODE_DIRECTORY", "Example-project")
    max_file_size_mb: float = float(os.getenv("MAX_FILE_SIZE_MB", 5.0))
    max_files_to_process: int = int(os.getenv("MAX_FILES_TO_PROCESS", 100))

class CodeFile(BaseModel):
    name: str = Field(...)
    path: str = Field(...)
    content: str = Field(...)
    size_bytes: int = Field(...)
    file_type: SupportedFileType = Field(...)

class FileProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.supported_extensions = {ext.value for ext in SupportedFileType}
    def get_code_files(self, code_dir: Path) -> dict:
        code_files = {}
        files_processed = 0
        for file_path in code_dir.rglob("*"):
            if files_processed >= self.settings.max_files_to_process:
                break
            if (file_path.is_file() and file_path.suffix in self.supported_extensions and
                not self._should_ignore_file(file_path)):
                file_size = file_path.stat().st_size
                max_size = self.settings.max_file_size_mb * 1024 * 1024
                if file_size > max_size:
                    continue
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                code_file = CodeFile(
                    name=file_path.name,
                    path=str(file_path.relative_to(code_dir)),
                    content=content,
                    size_bytes=file_size,
                    file_type=SupportedFileType(file_path.suffix)
                )
                code_files[file_path.name] = code_file
                files_processed += 1
        return code_files
    def _should_ignore_file(self, file_path: Path) -> bool:
        ignore_patterns = {'__pycache__', '.git', '.pytest_cache', 'node_modules', '.venv', 'venv', '.env', 'dist', 'build'}
        return any(pattern in str(file_path) for pattern in ignore_patterns)

class DebtIssueDetectionSignature(dspy.Signature):
    """DSPy signature for LLM-based technical debt detection."""
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    prompt: str = dspy.InputField(desc="Explicit instructions for LLM.")
    issues: str = dspy.OutputField(desc="Detected technical debt issues in IssueOutput format.")

class DebtIssueReviewSignature(dspy.Signature):
    """DSPy signature for technical debt review."""
    issues: str = dspy.InputField(
        desc="List of technical debt issues with file, line, severity, description, suggestion, and reference."
    )
    review_report: str = dspy.OutputField(
        desc="Detailed review report with severity, impact, remediation quality, and improvement suggestions."
    )

class DebtIssueDetector(dspy.Module):
    """DSPy module for LLM-based technical debt detection."""
    def __init__(self):
        super().__init__()
        self.detect = dspy.ChainOfThought(DebtIssueDetectionSignature)
    def forward(self, code: str, filename: str) -> str:
        # Prompt for technical debt issues only
        prompt = (
            "You are a senior code reviewer. For every technical debt issue you find, rank and sort it by the real-world impact and maintainability cost. Use severity 'high' for issues that significantly hinder maintainability, scalability, or future development (large functions, duplicated code, poor modularity, hardcoded values, lack of tests, etc.), 'medium' for issues that cause moderate pain (inconsistent naming, unclear logic, missing docstrings), and 'low' for minor style or convention violations. For each issue, include a brief justification for its ranking. Only use type 'debt' for maintainability issues, and 'improvement' for style or best-practice suggestions. If you are unsure about the severity or impact, include the issue and explain your reasoning. Output valid JSON as a list of IssueOutput objects, sorted from highest to lowest impact. Each issue must include: type ('debt' or 'improvement'), severity ('low', 'medium', 'high'), description, file, line, specific actionable suggestion, a relevant code snippet (3-5 lines), and a justification for its ranking. If there are no issues at all, output an empty list."
        )
        try:
            result = self.detect(code=code, filename=filename, prompt=prompt)
            return result.issues
        except Exception as e:
            logger.error(f"Error in LLM-based technical debt detection for {filename}: {e}")
            return ""

class DebtIssueReviewer(dspy.Module):
    """DSPy module for reviewing technical debt issues."""
    def __init__(self):
        super().__init__()
        self.review = dspy.ChainOfThought(DebtIssueReviewSignature)
    def forward(self, issues: str) -> str:
        try:
            result = self.review(issues=issues)
            return result.review_report
        except Exception as e:
            logger.error(f"Error reviewing technical debt issues: {e}")
            return f"Review failed: {e}"

class DebtAgent:
    """Main technical debt review agent."""
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._setup_dspy()
        self.reviewer = DebtIssueReviewer()
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
                f"- {issue.description} (File: {issue.file}, Line: {issue.line}, Severity: {issue.severity})\nSuggestion: {issue.suggestion}\nReference: {issue.reference}\n"
            )
        return "\n".join(formatted)
    def review_debt_issues(self, issues: List[IssueOutput]) -> str:
        issues_str = self._format_issues(issues)
        return self.reviewer.forward(issues=issues_str)

    # Heuristic detection removed: now fully LLM-based
    def run(self) -> AgentReport:
        code_dir = Path(self.settings.code_directory)
        if not code_dir.exists():
            raise RuntimeError(f"Code directory not found: {code_dir}")
        code_files = FileProcessor(self.settings).get_code_files(code_dir)
        detector = DebtIssueDetector()
        llm_issues = []
        import json
        for file in code_files.values():
            llm_result = detector.forward(code=file.content, filename=file.name)
            try:
                parsed = json.loads(llm_result)
                for issue in parsed:
                    llm_issues.append(IssueOutput(**issue))
            except Exception:
                logger.warning(f"Malformed LLM output for {file.name}, skipping.")
        unique_issues = llm_issues
        if not unique_issues:
            logger.info("No technical debt issues detected.")
        review = self.review_debt_issues(unique_issues)
        try:
            report = AgentReport(issues=unique_issues, review=review)
        except ValidationError as e:
            logger.error(f"Debt agent output validation failed: {e}")
            raise RuntimeError(f"Debt agent output validation failed: {e}")
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
    """Main entry point for the technical debt reviewer."""
    try:
        settings = Settings()
        agent = DebtAgent(settings)
        logger.info("Starting technical debt review...")
        code_dir = Path(settings.code_directory)
        code_files = FileProcessor(settings).get_code_files(code_dir)
        code_summary = _create_code_summary(code_files)
        output = agent.run()
        print("\n" + "="*80)
        print("TECHNICAL DEBT REVIEW COMPLETE")
        print("="*80)
        print(f"\n--- CODEBASE SUMMARY ---\n{code_summary}")
        for idx, issue in enumerate(output.issues, 1):
            print(f"\n--- Issue {idx} ---")
            print(f"Type: {issue.type}")
            print(f"Severity: {issue.severity}")
            print(f"Description: {issue.description}")
            print(f"File: {issue.file}")
            print(f"Line: {issue.line}")
            print(f"Suggestion: {issue.suggestion}")
            print(f"Reference: {issue.reference}")
        print(f"\n--- REVIEW REPORT ---")
        print(output.review)
        print(f"\n--- METADATA ---")
        print(f"total_files_processed: {len(code_files)}")
        print(f"issues_detected: {len(output.issues)}")
        print(f"code_directory: {settings.code_directory}")
        logger.info("Technical debt review completed successfully")
        return output
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()
