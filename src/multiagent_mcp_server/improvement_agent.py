"""
Code improvement analysis agent using the unified base agent architecture.

This module provides improvement opportunity detection and analysis capabilities
with significantly reduced code duplication through inheritance.
"""

import logging
from typing import List, Optional

from .base_agent import BaseAgent
from .models import IssueType, AgentReport
from .config import Settings
from .prompt_signatures import ImprovementDetectionSignature

# Configure logging
logger = logging.getLogger(__name__)


class ImprovementAgent(BaseAgent):
    """
    Code improvement analysis agent.
    
    Specializes in detecting:
    - Performance optimization opportunities
    - Code quality improvements
    - Best practice implementations
    - Documentation enhancements
    """
    
    @property
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        return "improvement"
    
    @property
    def agent_name(self) -> str:
        """Return the human-readable agent name."""
        return "Code Improvement Analyzer"
    
    def create_detector(self):
        """Create and return the improvement issue detector using dspy.Signature."""
        from .base_agent import BaseIssueDetector
        return BaseIssueDetector(ImprovementDetectionSignature)
    
    def get_expected_issue_types(self) -> List[IssueType]:
        """Return the issue types this agent should detect."""
        return [IssueType.IMPROVEMENT]
    
    def get_report_recommendations(self) -> List[str]:
        """Return improvement-specific recommendations."""
        return [
            "1. **High Impact:** Prioritize high-impact improvements for maximum benefit",
            "2. **Performance:** Focus on performance optimizations for better user experience",
            "3. **Best Practices:** Implement coding best practices to improve maintainability",
            "4. **Documentation:** Enhance code documentation and inline comments",
            "5. **Testing:** Improve test coverage and quality for modified areas",
            "6. **Security:** Address any security-related improvement opportunities first",
            "7. **Monitoring:** Consider adding monitoring and logging for improved areas"
        ]


def main(output_dir: Optional[str] = None) -> AgentReport:
    """
    Main entry point for the code improvement analyzer.
    
    Args:
        output_dir: Optional output directory override
        
    Returns:
        AgentReport: Analysis results with detected improvement opportunities
    """
    try:
        settings = Settings()
        agent = ImprovementAgent(settings)
        
        logger.info("Starting code improvement analysis...")
        report = agent.run(output_dir=output_dir)
        
        logger.info("Code improvement analysis completed successfully")
        return report
        
    except Exception as e:
        logger.error(f"Code improvement analysis failed: {e}")
        raise


if __name__ == "__main__":
    main()
