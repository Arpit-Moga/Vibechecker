"""
Production-ready MCP server for Multi-Agent code analysis.

This module provides the unified MCP server that exposes all agent tools
through the Model Context Protocol for seamless AI integration.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import Optional, Any, Dict

from mcp.server.fastmcp import FastMCP

# NOTE: Avoid importing heavy agent modules at import time to keep startup fast
# and prevent Smithery/stdio timeouts. We'll lazy-import them inside tool funcs.
from .config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server (no description kwarg to support older FastMCP versions)
mcp = FastMCP("Multi-Agent MCP Server")


@mcp.tool()
def issue_detection_review(
    code_directory: Optional[str] = None,
    output_directory: Optional[str] = None,
    output_format: str = "md",
    scan_mode: str = "quick"
) -> Dict[str, Any]:
    """
    Run unified issue detection analysis on the specified code directory.

    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        output_directory: Path to write output files (default: code_directory/DOCUMENTATION)
        output_format: "md" for markdown (default), "json" for JSON output
        scan_mode: "quick" (fastest tools only) or "deep" (all tools + LLM). Default is "quick".

    Returns:
        dict: Structured report with detected issues and recommendations
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        # Lazy import to avoid heavy dependency import at server startup
        from .issue_detection_agent import IssueDetectionAgent
        agent = IssueDetectionAgent(settings)
        logger.info(f"Running Unified Issue Detection Analysis on {target_dir} with scan_mode={scan_mode}")
        report = agent.run(output_dir=output_directory, output_format=output_format)
        # Convert Pydantic model to plain dict for safe MCP serialization
        return report.model_dump()

    except Exception as e:
        logger.error(f"Error in issue_detection_review: {e}")
        # Return a plain dict to avoid importing models on error path
        return {
            "issues": [],
            "review": f"Issue detection analysis failed: {str(e)}. Please check the code directory path and try again.",
            "error": True,
            "error_message": str(e),
        }


@mcp.tool()
def documentation_generate(code_directory: Optional[str] = None, output_directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate comprehensive documentation for the specified code directory.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        output_directory: Path to write output files (default: code_directory/DOCUMENTATION)
        
    Returns:
        dict: Generated documentation files with quality review and metadata
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        # Lazy import to avoid heavy dependency import at server startup
        from .documentation_agent import DocumentationAgent
        logger.info(f"Running Documentation Generation on {target_dir}")
        agent = DocumentationAgent(settings)
        output = agent.generate_documentation(output_dir=output_directory)
        return output.model_dump()
        
    except Exception as e:
        logger.error(f"Error in documentation_generate: {e}")
        return {
            "files": {},
            "review": f"Documentation generation failed: {str(e)}. Please check the code directory path and try again.",
            "metadata": {"error": True, "error_message": str(e)},
        }


@mcp.tool()
def comprehensive_review(
    code_directory: Optional[str] = None,
    output_directory: Optional[str] = None,
    output_format: str = "md",
    scan_mode: str = "quick"
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
        scan_mode: "quick" (fastest tools only) or "deep" (all tools + LLM). Default is "quick".

    Returns:
        dict: Complete analysis results from all agents with summary statistics
    """
    try:
        target_dir = code_directory or os.getcwd()
        logger.info(f"Running comprehensive multi-agent review on {target_dir} with scan_mode={scan_mode}")

        # Run all analyses (each returns plain dicts)
        issues_dict = issue_detection_review(target_dir, output_directory, output_format, scan_mode)
        docs_dict = documentation_generate(target_dir, output_directory)

        # Calculate summary statistics from dicts
        issues_list = issues_dict.get("issues", []) if isinstance(issues_dict, dict) else []
        total_issues = len(issues_list)
        high_severity_count = sum(1 for i in issues_list if str(i.get("severity", "")).lower() == "high")
        documentation_files = len(docs_dict.get("files", {})) if isinstance(docs_dict, dict) else 0

        results = {
            "issue_detection": issues_dict,
            "documentation_analysis": docs_dict,
            "summary": {
                "total_issues": total_issues,
                "high_severity_count": high_severity_count,
                "documentation_files": documentation_files,
                "analysis_timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "code_directory": target_dir,
            },
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
                "error": True,
                "error_message": str(e),
            },
        }



def main():
    """
    Entry point for running the Multi-Agent MCP Server.
    
    Configures logging, validates environment, and starts the MCP server
    with stdio transport for seamless AI integration.
    """
    
    parser = argparse.ArgumentParser(
        description='Multi-Agent MCP Server - Production-ready code analysis and documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Tools:
  issue_detection_review - Run unified issue detection analysis
  documentation_generate - Generate comprehensive project documentation
  comprehensive_review   - Run all analyses for complete code review

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
    logger.info("  • issue_detection_review - Unified issue detection analysis")
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
