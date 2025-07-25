"""
Production-ready improvement agent using DSPy and Pydantic.

This module scans code files for improvement opportunities using LLMs, validates outputs, and generates a review report.
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

# Logging setup
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

class ImprovementDetectionSignature(dspy.Signature):
    """DSPy signature for LLM-based improvement detection."""
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    prompt: str = dspy.InputField(desc="Explicit instructions for LLM.")
    issues: str = dspy.OutputField(desc="Detected improvement opportunities in IssueOutput format.")

class ImprovementReviewSignature(dspy.Signature):
    """DSPy signature for improvement review."""
    issues: str = dspy.InputField(
        desc="List of improvement opportunities with file, line, severity, description, suggestion, and reference."
    )
    review_report: str = dspy.OutputField(
        desc="Detailed review report with impact, feasibility, clarity, and suggestions for improvement."
    )

class ImprovementDetector(dspy.Module):
    """DSPy module for LLM-based improvement detection."""
    def __init__(self):
        super().__init__()
        self.detect = dspy.ChainOfThought(ImprovementDetectionSignature)
    def forward(self, code: str, filename: str) -> str:
        prompt = (
            "You are an expert code reviewer. Identify improvement opportunities in this file. "
            "For each opportunity, specify severity ('low', 'medium', 'high'), a clear description, file, line, actionable suggestion, and reference. "
            "Use type 'improvement' for code quality, performance, maintainability, documentation, or best practice suggestions. "
            "Output valid JSON as a list of IssueOutput objects. If no improvements, output an empty list."
        )
        try:
            result = self.detect(code=code, filename=filename, prompt=prompt)
            return result.issues
        except Exception as e:
            logger.error(f"Error in LLM-based improvement detection for {filename}: {e}")
            return ""

class ImprovementReviewer(dspy.Module):
    """DSPy module for reviewing improvement opportunities."""
    def __init__(self):
        super().__init__()
        self.review = dspy.ChainOfThought(ImprovementReviewSignature)
    def forward(self, issues: str) -> str:
        try:
            result = self.review(issues=issues)
            return result.review_report
        except Exception as e:
            logger.error(f"Error reviewing improvements: {e}")
            return f"Review failed: {e}"

class ImprovementAgent:
    """Main improvement agent."""
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._setup_dspy()
        self.reviewer = ImprovementReviewer()
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
    def review_improvements(self, issues: List[IssueOutput]) -> str:
        issues_str = self._format_issues(issues)
        return self.reviewer.forward(issues=issues_str)
    def run(self) -> AgentReport:
        code_dir = Path(self.settings.code_directory)
        if not code_dir.exists():
            raise RuntimeError(f"Code directory not found: {code_dir}")
        code_files = FileProcessor(self.settings).get_code_files(code_dir)
        detector = ImprovementDetector()
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
            logger.info("No improvement opportunities detected.")
        review = self.review_improvements(unique_issues)
        try:
            report = AgentReport(issues=unique_issues, review=review)
        except ValidationError as e:
            logger.error(f"Improvement agent output validation failed: {e}")
            raise RuntimeError(f"Improvement agent output validation failed: {e}")
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
    """Main entry point for the improvement agent."""
    try:
        settings = Settings()
        agent = ImprovementAgent(settings)
        logger.info("Starting improvement review...")
        code_dir = Path(settings.code_directory)
        code_files = FileProcessor(settings).get_code_files(code_dir)
        code_summary = _create_code_summary(code_files)
        output = agent.run()
        print("\n" + "="*80)
        print("IMPROVEMENT REVIEW COMPLETE")
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
        logger.info("Improvement review completed successfully")
        return output
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()
