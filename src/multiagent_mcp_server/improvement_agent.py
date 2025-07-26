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
    
    def get_detection_prompt(self) -> str:
        """Return the LLM prompt for improvement opportunity detection."""
        return (
            "You are an expert code reviewer specializing in identifying improvement opportunities. "
            "Analyze this code for areas where quality, performance, maintainability, or "
            "best practices could be enhanced.\n\n"
            
            "Focus on detecting:\n"
            "- Performance optimization opportunities\n"
            "- Code readability and clarity improvements\n"
            "- Better error handling implementations\n"
            "- More efficient algorithms or data structures\n"
            "- Enhanced code documentation\n"
            "- Better type safety and validation\n"
            "- Improved testing strategies\n"
            "- Modern language features that could be utilized\n"
            "- Security enhancements\n\n"
            
            "Severity guidelines:\n"
            "- 'high': Improvements with significant impact on performance, security, "
            "or maintainability\n"
            "- 'medium': Moderate improvements that enhance code quality or developer experience\n"
            "- 'low': Minor style improvements or best practice suggestions\n\n"
            
            "For each improvement opportunity found:\n"
            "1. Use type 'improvement' for all optimization and enhancement suggestions\n"
            "2. Provide specific, actionable improvement recommendations\n"
            "3. Explain the expected benefits of implementing the improvement\n"
            "4. Reference relevant best practices or performance patterns when applicable\n\n"
            
            "Output format: Valid JSON array of IssueOutput objects with fields: "
            "type, severity, description, file, line, suggestion, reference.\n"
            "If no improvement opportunities are found, return an empty array []."
        )
    
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
