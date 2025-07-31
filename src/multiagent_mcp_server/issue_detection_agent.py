"""
Unified Issue Detection Agent for Multi-Agent MCP Server.

Detects and classifies all code issues (maintainability, security, performance, compliance, other)
in a single pass, tagging each with type and severity.
"""

from .error_utils import get_logger, handle_errors
from typing import List, Optional
from .base_agent import BaseAgent
from .models import IssueType, Severity, IssueOutput, AgentReport
from .config import Settings
from .prompt_signatures import IssueDetectionSignature

logger = get_logger("multiagent_mcp_server.issue_detection_agent")

class IssueDetectionAgent(BaseAgent):
    """
    Unified agent for detecting all code issues.
    Tags each finding with type and severity.
    """

    @property
    def agent_type(self) -> str:
        return "issue_detection"

    @property
    def agent_name(self) -> str:
        return "Unified Issue Detection Agent"

    def create_detector(self):
        from .base_agent import BaseIssueDetector
        return BaseIssueDetector(IssueDetectionSignature)

    def get_expected_issue_types(self) -> List[IssueType]:
        return [
            IssueType.MAINTAINABILITY,
            IssueType.SECURITY,
            IssueType.PERFORMANCE,
            IssueType.COMPLIANCE,
            IssueType.OTHER,
        ]

    def get_report_recommendations(self) -> List[str]:
        return [
            "1. Address high-severity issues as a priority.",
            "2. Review security and compliance findings carefully.",
            "3. Plan remediation for maintainability and performance issues.",
            "4. Use references and suggestions for actionable improvements.",
        ]

@handle_errors(logger=logger, context="IssueDetectionAgent.main")
def main(output_dir: Optional[str] = None, output_format: str = "md") -> AgentReport:
    """
    Main entry point for the unified issue detection agent.

    Args:
        output_dir: Optional output directory override
        output_format: "md" for markdown (default), "json" for JSON output

    Returns:
        AgentReport: Analysis results with detected issues
    """
    settings = Settings()
    agent = IssueDetectionAgent(settings)

    logger.info("Starting unified issue detection analysis...")
    report = agent.run(output_dir=output_dir, output_format=output_format)

    logger.info("Unified issue detection analysis completed successfully")
    return report

if __name__ == "__main__":
    main()