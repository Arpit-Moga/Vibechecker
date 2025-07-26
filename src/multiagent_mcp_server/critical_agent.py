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
    
    def get_detection_prompt(self) -> str:
        """Return the LLM prompt for critical issue detection."""
        return (
            "You are a senior security and reliability engineer specializing in critical issue detection. "
            "Analyze this code for critical security vulnerabilities, data safety issues, and "
            "reliability problems that could cause serious harm.\n\n"
            
            "Focus on detecting ONLY genuinely critical issues:\n"
            "- Security vulnerabilities (SQL injection, XSS, authentication bypasses)\n"
            "- Hardcoded secrets, passwords, or API keys\n"
            "- Remote code execution vulnerabilities\n"
            "- Data loss or corruption risks\n"
            "- Memory safety issues (buffer overflows, use-after-free)\n"
            "- Privilege escalation vulnerabilities\n"
            "- Compliance violations (GDPR, HIPAA, etc.)\n"
            "- System crash or denial-of-service conditions\n"
            "- Unhandled exceptions that could expose sensitive data\n\n"
            
            "Severity guidelines (CRITICAL ISSUES MUST BE HIGH SEVERITY):\n"
            "- 'high': Catastrophic issues that could cause data loss, security breaches, "
            "system compromise, or compliance violations\n"
            "- 'medium': Major functional failures that could cause application crashes "
            "or significant service disruption\n"
            "- 'low': Minor reliability issues that don't pose immediate security risks\n\n"
            
            "IMPORTANT: Only use type 'critical' for the most severe, high-impact issues. "
            "All critical issues MUST have 'high' severity. Use type 'debt' or 'improvement' "
            "for lower-impact concerns.\n\n"
            
            "For each critical issue found:\n"
            "1. Use type 'critical' ONLY for genuine security/reliability threats\n"
            "2. Provide specific, actionable remediation steps\n"
            "3. Include a clear justification for why this is critical\n"
            "4. Reference security standards or best practices when applicable\n\n"
            
            "Output format: Valid JSON array of IssueOutput objects with fields: "
            "type, severity, description, file, line, remediation, reference.\n"
            "If no critical issues are found, return an empty array []."
        )
    
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
