"""
Critical security and reliability analysis agent using the unified base agent architecture.

This module provides critical issue detection and analysis capabilities
with significantly reduced code duplication through inheritance.
"""

import logging
from typing import List, Optional

from .base_agent import BaseAgent
from .models import IssueType, AgentReport
from .config import Settings

# Configure logging
logger = logging.getLogger(__name__)

from .prompt_signatures import CriticalDetectionSignature


class CriticalAgent(BaseAgent):
    """
    Critical security and reliability analysis agent.
    
    Specializes in detecting:
    - Security vulnerabilities
    - Data safety issues
    - System reliability problems
    - Compliance violations
    """
    
    @property
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        return "critical"
    
    @property
    def agent_name(self) -> str:
        """Return the human-readable agent name."""
        return "Critical Issues Analyzer"
    
    def create_detector(self):
        """Create and return the critical issue detector using dspy.Signature."""
        from .base_agent import BaseIssueDetector
        return BaseIssueDetector(CriticalDetectionSignature)
    
    def get_expected_issue_types(self) -> List[IssueType]:
        """Return the issue types this agent should detect."""
        return [IssueType.CRITICAL]
    
    def get_report_recommendations(self) -> List[str]:
        """Return critical issue specific recommendations."""
        return [
            "1. **Immediate Action Required:** Address all high-severity critical issues immediately",
            "2. **Security Review:** Conduct a thorough security audit of identified vulnerabilities",
            "3. **Code Review Process:** Implement automated security scanning in CI/CD pipeline",
            "4. **Documentation:** Update security documentation and incident response procedures",
            "5. **Testing:** Add security and reliability tests for affected components",
            "6. **Monitoring:** Implement monitoring and alerting for critical system components",
            "7. **Training:** Provide security awareness training for development team"
        ]


def main(output_dir: Optional[str] = None) -> AgentReport:
    """
    Main entry point for the critical issues analyzer.
    
    Args:
        output_dir: Optional output directory override
        
    Returns:
        AgentReport: Analysis results with detected critical issues
    """
    try:
        settings = Settings()
        agent = CriticalAgent(settings)
        
        logger.info("Starting critical issues analysis...")
        report = agent.run(output_dir=output_dir)
        
        logger.info("Critical issues analysis completed successfully")
        return report
        
    except Exception as e:
        logger.error(f"Critical issues analysis failed: {e}")
        raise


if __name__ == "__main__":
    main()
