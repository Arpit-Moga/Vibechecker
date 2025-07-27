"""
Base agent class for Multi-Agent MCP Server.

This module provides a unified base class that eliminates code duplication
across all specialized agents while maintaining extensibility and type safety.
"""

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .error_utils import get_logger, handle_errors
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

import dspy
from pydantic import ValidationError

from .models import IssueOutput, AgentReport, AnalysisMetadata, IssueType
from .config import Settings
from .agent_utils import FileProcessor, CodeFile


# Configure logging
logger = get_logger("multiagent_mcp_server.base_agent")


class BaseIssueDetectionSignature(dspy.Signature):
    """Base DSPy signature for LLM-based issue detection."""
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    prompt: str = dspy.InputField(desc="Explicit instructions for LLM.")
    issues: str = dspy.OutputField(desc="Detected issues in IssueOutput format.")


class BaseIssueReviewSignature(dspy.Signature):
    """Base DSPy signature for issue review."""
    issues: str = dspy.InputField(desc="List of issues with details for review.")
    review_report: str = dspy.OutputField(desc="Detailed review report with analysis and recommendations.")


class BaseIssueDetector(dspy.Module):
    """Base DSPy module for LLM-based issue detection."""
    
    def __init__(self, detection_signature: type = BaseIssueDetectionSignature):
        super().__init__()
        self.detect = dspy.ChainOfThought(detection_signature)
    
    def forward(self, code: str, filename: str) -> str:
        """Detect issues in code using LLM."""
        try:
            result = self.detect(code=code, filename=filename)
            return result.issues
        except Exception as e:
            logger.error(f"Error in LLM-based issue detection for {filename}: {e}")
            return ""


class BaseIssueReviewer(dspy.Module):
    """Base DSPy module for reviewing detected issues."""
    
    def __init__(self, review_signature: type = BaseIssueReviewSignature):
        super().__init__()
        self.review = dspy.ChainOfThought(review_signature)
    
    def forward(self, issues: str) -> str:
        """Review detected issues using LLM."""
        try:
            result = self.review(issues=issues)
            return result.review_report
        except Exception as e:
            logger.error(f"Error reviewing issues: {e}")
            return f"Review failed: {e}"


class BaseAgent(ABC):
    """
    Base class for all analysis agents.
    
    Provides common functionality for:
    - DSPy configuration and LLM setup
    - Code file processing
    - Issue detection and review
    - Report generation and file output
    - Error handling and logging
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the base agent with configuration."""
        self.settings = settings or Settings()
        self.file_processor = FileProcessor(self.settings)
        self._setup_dspy()
        self._setup_components()
    
    def _setup_dspy(self) -> None:
        """Configure DSPy with appropriate LLM provider."""
        try:
            if self.settings.google_api_key:
                dspy.configure(lm=dspy.LM(
                    model="gemini/gemini-2.5-flash",
                    api_key=self.settings.google_api_key
                ))
                logger.info(f"Configured DSPy with Gemini for {self.agent_type}")
            elif self.settings.openai_api_key:
                dspy.configure(lm=dspy.LM(
                    model="openai/gpt-3.5-turbo",
                    api_key=self.settings.openai_api_key
                ))
                logger.info(f"Configured DSPy with OpenAI for {self.agent_type}")
            else:
                logger.warning(f"No API keys found for {self.agent_type}, using default DSPy configuration")
        except Exception as e:
            logger.error(f"Failed to configure DSPy for {self.agent_type}: {e}")
            raise RuntimeError(f"LLM configuration failed for {self.agent_type}: {e}")
    
    def _setup_components(self) -> None:
        """Setup detector and reviewer components."""
        self.detector = self.create_detector()
        self.reviewer = self.create_reviewer()
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the type of agent (e.g., 'debt', 'improvement', 'critical')."""
        pass
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Return the human-readable name of the agent."""
        pass
    
    # get_detection_prompt is removed; prompt logic is now handled by dspy.Signature and dspy.Module.
    
    @abstractmethod
    def get_expected_issue_types(self) -> List[IssueType]:
        """Return the list of issue types this agent should detect."""
        pass
    
    def create_detector(self) -> BaseIssueDetector:
        """Create and return the issue detector. Subclasses must specify the correct signature."""
        raise NotImplementedError("Subclasses must implement create_detector to specify the correct dspy.Signature.")
    
    def create_reviewer(self) -> BaseIssueReviewer:
        """Create and return the issue reviewer."""
        return BaseIssueReviewer()
    
    def format_issues_for_review(self, issues: List[IssueOutput]) -> str:
        """Format issues for LLM review."""
        formatted = []
        for issue in issues:
            action_text = issue.suggestion if issue.suggestion else issue.remediation
            formatted.append(
                f"- {issue.description} (File: {issue.file}, Line: {issue.line}, Severity: {issue.severity})\n"
                f"Action: {action_text}\nReference: {issue.reference}\n"
            )
        return "\n".join(formatted)
    
    def detect_issues_in_file(self, code_file: CodeFile) -> List[IssueOutput]:
        """Detect issues in a single code file using dspy.Signature and dspy.Module."""
        llm_result = self.detector.forward(
            code=code_file.content,
            filename=code_file.name
        )

        # Parse LLM output
        detected_issues = []
        if llm_result.strip():
            try:
                parsed_issues = json.loads(llm_result)
                for issue_data in parsed_issues:
                    try:
                        issue = IssueOutput(**issue_data)
                        # Validate issue type matches what this agent should detect
                        if issue.type in [t.value for t in self.get_expected_issue_types()]:
                            detected_issues.append(issue)
                        else:
                            logger.warning(f"Unexpected issue type {issue.type} from {self.agent_type} agent")
                    except ValidationError as e:
                        logger.warning(f"Invalid issue output in {code_file.name}: {e}")
            except json.JSONDecodeError:
                logger.warning(f"Malformed JSON output from {self.agent_type} agent for {code_file.name}")

        return detected_issues
    
    def review_issues(self, issues: List[IssueOutput]) -> str:
        """Generate a review report for detected issues."""
        if not issues:
            return f"No {self.agent_type} issues detected. The codebase shows good quality in this area."
        
        issues_str = self.format_issues_for_review(issues)
        return self.reviewer.forward(issues=issues_str)
    
    def generate_report_filename_prefix(self) -> str:
        """Generate filename prefix for output files."""
        type_map = {
            "debt": "technical_debt",
            "improvement": "improvement_opportunities", 
            "critical": "critical_issues",
            "documentation": "documentation_generation"
        }
        return type_map.get(self.agent_type, self.agent_type)
    
    def write_output_files_md_only(self, report: AgentReport, output_dir: Path) -> Dict[str, Any]:
        """Write agent output to Markdown file only."""
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_prefix = self.generate_report_filename_prefix()
        md_file = output_dir / f"{filename_prefix}_{timestamp}.md"
        md_content = self.generate_markdown_report(report, timestamp)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        logger.info(f"{self.agent_name} markdown written to: {md_file}")
        return {
            "markdown_file": str(md_file),
            "total_issues": len(report.issues),
            "agent_type": self.agent_type
        }

    def write_output_files_json_only(self, report: AgentReport, output_dir: Path) -> Dict[str, Any]:
        """Write agent output to JSON file only."""
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_prefix = self.generate_report_filename_prefix()
        json_file = output_dir / f"{filename_prefix}_{timestamp}.json"
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "total_issues": len(report.issues),
            "issues": [issue.model_dump() for issue in report.issues],
            "review": report.review,
            "metadata": {
                "code_directory": str(self.settings.code_directory),
                "files_processed": getattr(self, '_files_processed', 0)
            }
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        logger.info(f"{self.agent_name} report written to: {json_file}")
        return {
            "json_file": str(json_file),
            "total_issues": len(report.issues),
            "agent_type": self.agent_type
        }
    
    def generate_markdown_report(self, report: AgentReport, timestamp: str, plugin_results: Optional[Dict[str, List[Dict[str, Any]]]] = None) -> str:
        """Generate a Markdown report with only unified agent and plugin results."""
        md_lines = [
            f"# {self.agent_name} Report",
            "",
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Agent:** {self.agent_name}",
            f"**Total Issues Found:** {len(report.issues)}",
            "",
            f"## {self.agent_name} Details",
            ""
        ]

        if not report.issues:
            md_lines.extend([
                f"✅ **No {self.agent_type} issues detected!**",
                "",
                f"The codebase analysis shows good quality with respect to {self.agent_type} concerns."
            ])
        else:
            # Group issues by severity
            severity_groups = {
                "High": [issue for issue in report.issues if issue.severity.value == "high"],
                "Medium": [issue for issue in report.issues if issue.severity.value == "medium"],
                "Low": [issue for issue in report.issues if issue.severity.value == "low"]
            }

            for severity, issues in severity_groups.items():
                if issues:
                    md_lines.extend([
                        f"### {severity} Severity Issues ({len(issues)})",
                        ""
                    ])

                    for i, issue in enumerate(issues, 1):
                        md_lines.extend([
                            f"#### {i}. {issue.description}",
                            "",
                            f"- **File:** `{issue.file}`",
                            f"- **Line:** {issue.line}",
                            f"- **Type:** {issue.type.value}",
                            f"- **Severity:** {issue.severity.value}",
                            ""
                        ])

                        if issue.suggestion:
                            md_lines.extend([
                                "**Suggested Action:**",
                                issue.suggestion,
                                ""
                            ])

                        if issue.remediation:
                            md_lines.extend([
                                "**Remediation:**",
                                issue.remediation,
                                ""
                            ])

                        if issue.reference:
                            md_lines.extend([
                                f"**Reference:** {issue.reference}",
                                ""
                            ])

                        md_lines.extend(["---", ""])

        # Add plugin results as Markdown tables if provided
        if plugin_results:
            from .orchestrator import plugin_results_to_markdown_tables
            md_lines.extend([
                "",
                "## Static Analysis Plugin Results",
                "",
                plugin_results_to_markdown_tables(plugin_results),
                ""
            ])

        md_lines.extend([
            "## Recommendations",
            "",
            *self.get_report_recommendations(),
            "",
            "---",
            f"*Report generated by Multi-Agent MCP Server - {self.agent_name}*"
        ])

        return "\n".join(md_lines)
    
    @abstractmethod
    def get_report_recommendations(self) -> List[str]:
        """Return agent-specific recommendations for the report."""
        pass
    
    @handle_errors(logger=logger, context="BaseAgent.run")
    def run(self, output_dir: Optional[str] = None, output_format: str = "md") -> AgentReport:
        from .orchestrator import Orchestrator
        from .models import IssueOutput
        """
        Main execution method for the agent with batch and parallel processing.

        Args:
            output_dir: Optional output directory for reports
            output_format: "md" for markdown (default), "json" for JSON output
        """
        logger.info(f"Starting {self.agent_name} analysis...")

        # Validate code directory
        code_dir = Path(self.settings.code_directory)
        if not code_dir.exists():
            raise RuntimeError(f"Code directory not found: {code_dir}")

        # Get code files
        code_files = self.file_processor.get_code_files(code_dir)
        self._files_processed = len(code_files)

        if not code_files:
            logger.warning(f"No code files found in {code_dir}")

        # Detect issues across all files in parallel
        all_issues = []
        max_workers = min(8, len(code_files)) if code_files else 1  # Configurable if needed

        def process_file(code_file):
            return self.detect_issues_in_file(code_file)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(process_file, cf): cf.name for cf in code_files.values()}
            for future in as_completed(future_to_file):
                file_issues = future.result()
                all_issues.extend(file_issues)

        logger.info(f"{self.agent_name} detected {len(all_issues)} issues")

        # Deduplicate issues
        try:
            orchestrator_for_dedupe = Orchestrator()
            deduped = orchestrator_for_dedupe.aggregate_results([issue.model_dump() for issue in all_issues])
            # Convert back to IssueOutput objects
            all_issues = [IssueOutput(**issue) for issue in deduped]
            logger.info(f"{self.agent_name} deduplicated to {len(all_issues)} unique issues")
        except Exception as e:
            logger.warning(f"Could not deduplicate issues: {e}")

        # --- NEW: Run orchestrator plugins and collect results ---
        plugin_results = None
        try:
            from .plugins.ruff_plugin import RuffPlugin
            from .plugins.bandit_plugin import BanditPlugin
            from .plugins.mypy_plugin import MypyPlugin
            from .plugins.semgrep_plugin import SemgrepPlugin
            plugin_classes = [RuffPlugin, BanditPlugin, MypyPlugin, SemgrepPlugin]
            orchestrator = Orchestrator(plugin_classes=plugin_classes)
            plugin_results = orchestrator.run_plugins([str(f.path) for f in code_files.values()])
            logger.info("Static analysis plugin results collected for report.")
        except Exception as e:
            logger.warning(f"Could not collect plugin results: {e}")

        # Generate review
        review = self.review_issues(all_issues)

        # Create and validate report
        try:
            report = AgentReport(issues=all_issues, review=review)
        except ValidationError as e:
            logger.error(f"{self.agent_name} output validation failed: {e}")
            raise RuntimeError(f"{self.agent_name} output validation failed: {e}")

        # Write output files
        if output_dir:
            doc_dir = Path(output_dir) / "DOCUMENTATION"
        else:
            doc_dir = Path(self.settings.code_directory) / "DOCUMENTATION"

        if output_format == "json":
            # Only write JSON file
            file_info = self.write_output_files_json_only(report, doc_dir)
        else:
            # Default: write only markdown file, now with plugin results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            md_file = doc_dir / f"{self.generate_report_filename_prefix()}_{timestamp}.md"
            md_content = self.generate_markdown_report(report, timestamp, plugin_results=plugin_results)
            doc_dir.mkdir(parents=True, exist_ok=True)
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            file_info = {
                "markdown_file": str(md_file),
                "total_issues": len(report.issues),
                "agent_type": self.agent_type
            }

        logger.info(f"{self.agent_name} analysis complete. Files written: {file_info}")

        return report


# Export base classes
__all__ = [
    "BaseAgent",
    "BaseIssueDetector", 
    "BaseIssueReviewer",
    "BaseIssueDetectionSignature",
    "BaseIssueReviewSignature"
]