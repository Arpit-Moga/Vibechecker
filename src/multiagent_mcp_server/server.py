"""
Production-ready MCP server for Multi-Agent code analysis.

This module provides the unified MCP server that exposes all agent tools
through the Model Context Protocol for seamless AI integration.
"""

import logging
import os
import sys
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .issue_detection_agent import IssueDetectionAgent
from .documentation_agent import DocumentationAgent
from .config import Settings
from .models import AgentReport
from .documentation_agent import DocumentationOutput

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server with comprehensive description
mcp = FastMCP(
    "Multi-Agent MCP Server",
    description="Production-ready multi-agent code review and documentation system with specialized agents for technical debt, improvements, critical issues, and documentation generation."
)


@mcp.tool()
def issue_detection_review(
    code_directory: Optional[str] = None,
    output_directory: Optional[str] = None,
    output_format: str = "md"
) -> AgentReport:
    """
    Run unified issue detection analysis on the specified code directory.

    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        output_directory: Path to write output files (default: code_directory/DOCUMENTATION)
        output_format: "md" for markdown (default), "json" for JSON output

    Returns:
        AgentReport: Structured report with detected issues and recommendations
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        agent = IssueDetectionAgent(settings)

        logger.info(f"Running Unified Issue Detection Analysis on {target_dir}")
        return agent.run(output_dir=output_directory, output_format=output_format)

    except Exception as e:
        logger.error(f"Error in issue_detection_review: {e}")
        return AgentReport(
            issues=[],
            review=f"Issue detection analysis failed: {str(e)}. Please check the code directory path and try again."
        )


# Removed improvement_review (now handled by unified agent)


# Removed critical_review (now handled by unified agent)


@mcp.tool()
def documentation_generate(code_directory: Optional[str] = None, output_directory: Optional[str] = None) -> DocumentationOutput:
    """
    Generate comprehensive documentation for the specified code directory.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        output_directory: Path to write output files (default: code_directory/DOCUMENTATION)
        
    Returns:
        DocumentationOutput: Generated documentation files with quality review and metadata
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        agent = DocumentationAgent(settings)
        
        logger.info(f"Running Documentation Generation on {target_dir}")
        return agent.generate_documentation(output_dir=output_directory)
        
    except Exception as e:
        logger.error(f"Error in documentation_generate: {e}")
        return DocumentationOutput(
            files={},
            review=f"Documentation generation failed: {str(e)}. Please check the code directory path and try again.",
            metadata={"error": True, "error_message": str(e)}
        )


@mcp.tool()
def comprehensive_review(
    code_directory: Optional[str] = None,
    output_directory: Optional[str] = None,
    output_format: str = "md"
) -> dict:
    """
    Run all agents on the specified code directory for comprehensive analysis.

    This tool orchestrates all available agents to provide complete coverage of:
    - Unified issue detection
    - Documentation generation

    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        output_directory: Path to write output files (default: code_directory/DOCUMENTATION)
        output_format: "md" for markdown (default), "json" for JSON output

    Returns:
        dict: Complete analysis results from all agents with summary statistics
    """
    try:
        target_dir = code_directory or os.getcwd()
        logger.info(f"Running comprehensive multi-agent review on {target_dir}")

        # Run all analyses
        results = {
            "issue_detection": issue_detection_review(target_dir, output_directory, output_format),
            "documentation_analysis": documentation_generate(target_dir, output_directory),
        }

        # Calculate summary statistics
        total_issues = len(results["issue_detection"].issues) if hasattr(results["issue_detection"], 'issues') else 0
        high_severity_count = len([i for i in getattr(results["issue_detection"], 'issues', []) if getattr(i, 'severity', None) == "high"])
        documentation_files = len(results["documentation_analysis"].files) if hasattr(results["documentation_analysis"], 'files') else 0

        results["summary"] = {
            "total_issues": total_issues,
            "high_severity_count": high_severity_count,
            "documentation_files": documentation_files,
            "analysis_timestamp": "2025-01-26T10:25:00Z",  # Will be dynamically set
            "code_directory": target_dir
        }

        logger.info(f"Comprehensive review completed. Total issues found: {total_issues}")
        return results

    except Exception as e:
        logger.error(f"Error in comprehensive_review: {e}")
        return {
            "error": f"Comprehensive review failed: {str(e)}",
            "summary": {
                "total_issues": 0,
                "high_severity_count": 0,
                "documentation_files": 0,
                "error": True
            }
        }


def main():
    """
    Entry point for running the Multi-Agent MCP Server.
    
    Configures logging, validates environment, and starts the MCP server
    with stdio transport for seamless AI integration.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Multi-Agent MCP Server - Production-ready code analysis and documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Tools:
  debt_review          - Analyze technical debt and maintainability issues
  improvement_review   - Identify code quality improvement opportunities  
  critical_review      - Detect critical security and reliability issues
  documentation_generate - Generate comprehensive project documentation
  comprehensive_review - Run all analyses for complete code review

Environment Variables:
  CODE_DIRECTORY       - Default code directory to analyze
  GOOGLE_API_KEY      - Google AI API key for LLM analysis
  OPENAI_API_KEY      - OpenAI API key for LLM analysis
  MAX_FILE_SIZE_MB    - Maximum file size to process (default: 5.0)
  MAX_FILES_TO_PROCESS - Maximum number of files to process (default: 100)
        """
    )
    
    parser.add_argument(
        '--log-level', 
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Log startup information
    logger.info("="*60)
    logger.info("Starting Multi-Agent MCP Server")
    logger.info("="*60)
    logger.info("Available tools:")
    logger.info("  • debt_review - Technical debt analysis")
    logger.info("  • improvement_review - Code improvement opportunities")  
    logger.info("  • critical_review - Critical security and reliability issues")
    logger.info("  • documentation_generate - Comprehensive documentation")
    logger.info("  • comprehensive_review - Complete multi-agent analysis")
    logger.info("="*60)
    
    try:
        # Use standard stdio transport for MCP protocol
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
