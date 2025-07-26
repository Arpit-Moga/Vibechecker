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
    
    def get_detection_prompt(self) -> str:
        """Return the LLM prompt for technical debt detection."""
        return (
            "You are a senior code reviewer specializing in technical debt analysis. "
            "Analyze this code for technical debt issues that impact maintainability, "
            "scalability, and future development velocity.\n\n"
            
            "Focus on detecting:\n"
            "- Large, complex functions that are hard to maintain\n"
            "- Duplicated code patterns\n"
            "- Poor modularity and tight coupling\n"
            "- Hardcoded values that should be configurable\n"
            "- Missing or inadequate tests\n"
            "- Inconsistent naming conventions\n"
            "- Unclear or convoluted logic\n"
            "- Missing documentation for complex code\n\n"
            
            "Severity guidelines:\n"
            "- 'high': Issues that significantly hinder maintainability, scalability, "
            "or future development (large functions, major duplication, poor architecture)\n"
            "- 'medium': Issues causing moderate development friction "
            "(inconsistent patterns, missing docstrings, minor coupling)\n"
            "- 'low': Minor style or convention issues that don't impact functionality\n\n"
            
            "For each technical debt issue found:\n"
            "1. Use type 'debt' for maintainability/architecture issues\n"
            "2. Include specific, actionable suggestions for improvement\n"
            "3. Provide a brief justification for the severity rating\n"
            "4. Reference relevant best practices or standards when applicable\n\n"
            
            "Output format: Valid JSON array of IssueOutput objects with fields: "
            "type, severity, description, file, line, suggestion, reference.\n"
            "If no technical debt is found, return an empty array []."
        )
    
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
