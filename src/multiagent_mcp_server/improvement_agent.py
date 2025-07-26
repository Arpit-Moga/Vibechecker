"""
Production-ready improvement agent using DSPy and Pydantic.

This module scans code files for improvement opportunities using LLMs, validates outputs, and generates a review report.
Writes outputs to JSON and Markdown files in DOCUMENTATION folder.
"""

import logging
import os
import json
from typing import List, Optional
from datetime import datetime
from pydantic import ValidationError
from multiagent_mcp_server.models import IssueOutput, AgentReport
import dspy
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from multiagent_mcp_server.agent_utils import SupportedFileType, Settings, CodeFile, FileProcessor

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
            "For each opportunity, specify severity ('low', 'medium', 'high'), with a clear description, file, line, actionable suggestion, and reference. "
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
    
    def _write_output_files(self, report: AgentReport, output_dir: Path) -> dict:
        """Write agent output to JSON and Markdown files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = output_dir / f"improvement_opportunities_{timestamp}.json"
        md_file = output_dir / f"improvement_opportunities_{timestamp}.md"
        
        # Write JSON file
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": "improvement",
            "total_issues": len(report.issues),
            "issues": [issue.model_dump() for issue in report.issues],
            "review": report.review
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Write Markdown file
        md_content = self._generate_markdown_report(report, timestamp)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"Improvement opportunities report written to: {json_file}")
        logger.info(f"Improvement opportunities markdown written to: {md_file}")
        
        return {
            "json_file": str(json_file),
            "markdown_file": str(md_file),
            "total_issues": len(report.issues)
        }
    
    def _generate_markdown_report(self, report: AgentReport, timestamp: str) -> str:
        """Generate a comprehensive Markdown report."""
        md_lines = [
            "# Code Improvement Opportunities Report",
            f"",
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Agent:** Code Improvement Analyzer",
            f"**Total Opportunities Found:** {len(report.issues)}",
            f"",
            "## Executive Summary",
            f"",
            report.review,
            f"",
            "## Improvement Opportunities",
            f""
        ]
        
        if not report.issues:
            md_lines.extend([
                "✅ **Excellent code quality!**",
                "",
                "The codebase analysis shows high-quality code with minimal improvement opportunities."
            ])
        else:
            # Group issues by severity
            high_issues = [issue for issue in report.issues if issue.severity == "high"]
            medium_issues = [issue for issue in report.issues if issue.severity == "medium"]
            low_issues = [issue for issue in report.issues if issue.severity == "low"]
            
            for severity, issues in [("High", high_issues), ("Medium", medium_issues), ("Low", low_issues)]:
                if issues:
                    md_lines.extend([
                        f"### {severity} Impact Improvements ({len(issues)})",
                        ""
                    ])
                    
                    for i, issue in enumerate(issues, 1):
                        md_lines.extend([
                            f"#### {i}. {issue.description}",
                            f"",
                            f"- **File:** `{issue.file}`",
                            f"- **Line:** {issue.line}",
                            f"- **Type:** {issue.type}",
                            f"- **Impact:** {issue.severity}",
                            ""
                        ])
                        
                        if issue.suggestion:
                            md_lines.extend([
                                f"**Suggested Improvement:**",
                                f"{issue.suggestion}",
                                ""
                            ])
                        
                        if issue.reference:
                            md_lines.extend([
                                f"**Reference:** {issue.reference}",
                                ""
                            ])
                        
                        md_lines.append("---")
                        md_lines.append("")
        
        md_lines.extend([
            "## Implementation Strategy",
            "",
            "1. **High Impact:** Prioritize high-impact improvements for maximum benefit",
            "2. **Performance:** Focus on performance optimizations for better user experience", 
            "3. **Best Practices:** Implement coding best practices to improve maintainability",
            "4. **Documentation:** Enhance code documentation and comments",
            "",
            "---",
            f"*Report generated by Multi-Agent MCP Server - Code Improvement Analyzer*"
        ])
        
        return "\n".join(md_lines)
    def run(self, output_dir: Optional[str] = None) -> AgentReport:
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
        
        # Write output files
        if output_dir:
            doc_dir = Path(output_dir) / "DOCUMENTATION"
        else:
            doc_dir = Path(self.settings.code_directory) / "DOCUMENTATION"
        
        file_info = self._write_output_files(report, doc_dir)
        logger.info(f"Improvement opportunities analysis complete. Files written: {file_info}")
        
        return report

def _create_code_summary(code_files: dict) -> str:
    summary_parts = []
    summary_parts.append("## Project Structure Overview")
    summary_parts.append(f"Total files analyzed: {len(code_files)}")
    summary_parts.append("\n### File List:")
    for code_file in code_files.values():
        summary_parts.append(f"- {code_file.name} ({code_file.size_bytes} bytes)")
    return "\n".join(summary_parts)

def main(output_dir: Optional[str] = None):
    """Main entry point for the improvement agent."""
    try:
        settings = Settings()
        agent = ImprovementAgent(settings)
        logger.info("Starting improvement review...")
        code_dir = Path(settings.code_directory)
        code_files = FileProcessor(settings).get_code_files(code_dir)
        code_summary = _create_code_summary(code_files)
        output = agent.run(output_dir=output_dir)
        
        # Also print to console for backwards compatibility
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
