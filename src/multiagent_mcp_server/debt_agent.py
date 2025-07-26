"""
Technical debt analysis agent using the unified base agent architecture.

This module provides technical debt detection and analysis capabilities
with significantly reduced code duplication through inheritance.
"""

import logging
from typing import List, Optional

from .base_agent import BaseAgent
from .models import IssueType, AgentReport
from .config import Settings

# Configure logging
logger = logging.getLogger(__name__)

from .prompt_signatures import DebtDetectionSignature


class DebtAgent(BaseAgent):
    """
    Technical debt analysis agent.
    
    Specializes in detecting:
    - Code maintainability issues
    - Design debt and architectural problems
    - Code quality concerns that hinder development
    """
    
    @property
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        return "debt"
    
    @property
    def agent_name(self) -> str:
        """Return the human-readable agent name."""
        return "Technical Debt Analyzer"
    
    def create_detector(self):
        """Create and return the debt issue detector using dspy.Signature."""
        from .base_agent import BaseIssueDetector
        return BaseIssueDetector(DebtDetectionSignature)
    
    def get_expected_issue_types(self) -> List[IssueType]:
        """Return the issue types this agent should detect."""
        return [IssueType.DEBT]
    
    def get_report_recommendations(self) -> List[str]:
        """Return technical debt specific recommendations."""
        return [
            "1. **High Priority:** Address high-priority technical debt to improve maintainability",
            "2. **Refactoring Plan:** Create a systematic plan to reduce technical debt over time",
            "3. **Code Standards:** Establish and enforce coding standards to prevent future debt",
            "4. **Regular Reviews:** Schedule periodic technical debt assessments",
            "5. **Testing:** Improve test coverage for areas with significant technical debt",
            "6. **Documentation:** Add documentation for complex or unclear code sections"
        ]


def main(output_dir: Optional[str] = None) -> AgentReport:
    """
    Main entry point for the technical debt analyzer.
    
    Args:
        output_dir: Optional output directory override
        
    Returns:
        AgentReport: Analysis results with detected technical debt issues
    """
    try:
        settings = Settings()
        agent = DebtAgent(settings)
        
        logger.info("Starting technical debt analysis...")
        report = agent.run(output_dir=output_dir)
        
        logger.info("Technical debt analysis completed successfully")
        return report
        
    except Exception as e:
        logger.error(f"Technical debt analysis failed: {e}")
        raise


if __name__ == "__main__":
    main()
