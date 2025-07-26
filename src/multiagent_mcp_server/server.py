"""
MCP-enabled server using FastMCP, exposing agent tools as MCP tools.
"""
from mcp.server.fastmcp import FastMCP
from multiagent_mcp_server.debt_agent import DebtAgent
from multiagent_mcp_server.improvement_agent import ImprovementAgent
from multiagent_mcp_server.documentation_agent import DocumentationAgent
from multiagent_mcp_server.critical_agent import CriticalAgent
from multiagent_mcp_server.agent_utils import Settings
from multiagent_mcp_server.models import AgentReport
from multiagent_mcp_server.documentation_agent import DocumentationOutput
from typing import Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server with description
mcp = FastMCP("Multi-Agent MCP Server", description="Production-ready multi-agent code review and documentation system")

@mcp.tool()
def debt_review(code_directory: Optional[str] = None) -> AgentReport:
    """
    Run the DebtAgent on the specified code directory.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        
    Returns:
        AgentReport: Structured report with detected technical debt issues
    """
    try:
        # Use current working directory if not specified
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        agent = DebtAgent(settings)
        logger.info(f"Running DebtAgent on {settings.code_directory}")
        return agent.run()
    except Exception as e:
        logger.error(f"Error in debt_review: {e}")
        # Return empty report on error
        from multiagent_mcp_server.models import AgentReport
        return AgentReport(issues=[], review=f"Error occurred during analysis: {str(e)}")

@mcp.tool()
def improvement_review(code_directory: Optional[str] = None) -> AgentReport:
    """
    Run the ImprovementAgent on the specified code directory.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        
    Returns:
        AgentReport: Structured report with detected improvement opportunities
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        agent = ImprovementAgent(settings)
        logger.info(f"Running ImprovementAgent on {settings.code_directory}")
        return agent.run()
    except Exception as e:
        logger.error(f"Error in improvement_review: {e}")
        from multiagent_mcp_server.models import AgentReport
        return AgentReport(issues=[], review=f"Error occurred during analysis: {str(e)}")

@mcp.tool()
def documentation_generate(code_directory: Optional[str] = None) -> DocumentationOutput:
    """
    Run the DocumentationAgent on the specified code directory.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        
    Returns:
        DocumentationOutput: Generated documentation files and review
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        agent = DocumentationAgent(settings)
        logger.info(f"Running DocumentationAgent on {settings.code_directory}")
        return agent.generate_documentation()
    except Exception as e:
        logger.error(f"Error in documentation_generate: {e}")
        from multiagent_mcp_server.documentation_agent import DocumentationOutput
        return DocumentationOutput(
            files={},
            review=f"Error occurred during documentation generation: {str(e)}",
            metadata={"error": True}
        )

@mcp.tool()
def critical_review(code_directory: Optional[str] = None) -> AgentReport:
    """
    Run the CriticalAgent on the specified code directory.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        
    Returns:
        AgentReport: Structured report with detected critical security and reliability issues
    """
    try:
        target_dir = code_directory or os.getcwd()
        settings = Settings(code_directory=target_dir)
        agent = CriticalAgent(settings)
        logger.info(f"Running CriticalAgent on {settings.code_directory}")
        return agent.run()
    except Exception as e:
        logger.error(f"Error in critical_review: {e}")
        from multiagent_mcp_server.models import AgentReport
        return AgentReport(issues=[], review=f"Error occurred during analysis: {str(e)}")

@mcp.tool()
def comprehensive_review(code_directory: Optional[str] = None) -> dict:
    """
    Run all agents on the specified code directory for a comprehensive analysis.
    
    Args:
        code_directory: Path to code directory to analyze (default: current working directory)
        
    Returns:
        dict: Complete analysis results from all agents
    """
    try:
        target_dir = code_directory or os.getcwd()
        logger.info(f"Running comprehensive review on {target_dir}")
        
        results = {
            "debt_analysis": debt_review(target_dir),
            "improvement_analysis": improvement_review(target_dir),
            "critical_analysis": critical_review(target_dir),
            "documentation_analysis": documentation_generate(target_dir),
            "summary": {
                "total_issues": 0,
                "critical_count": 0,
                "debt_count": 0,
                "improvement_count": 0
            }
        }
        
        # Calculate summary statistics
        for analysis_type in ["debt_analysis", "improvement_analysis", "critical_analysis"]:
            if hasattr(results[analysis_type], 'issues'):
                issue_count = len(results[analysis_type].issues)
                results["summary"]["total_issues"] += issue_count
                
                if analysis_type == "critical_analysis":
                    results["summary"]["critical_count"] = issue_count
                elif analysis_type == "debt_analysis":
                    results["summary"]["debt_count"] = issue_count
                elif analysis_type == "improvement_analysis":
                    results["summary"]["improvement_count"] = issue_count
        
        return results
        
    except Exception as e:
        logger.error(f"Error in comprehensive_review: {e}")
        return {
            "error": f"Comprehensive review failed: {str(e)}",
            "summary": {"total_issues": 0, "critical_count": 0, "debt_count": 0, "improvement_count": 0}
        }

def main():
    """
    Entry point for running the MCP server.
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Agent MCP Server')
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    logger.info("Starting Multi-Agent MCP Server...")
    logger.info("Available tools: debt_review, improvement_review, documentation_generate, critical_review, comprehensive_review")
    
    try:
        # Use standard stdio transport for MCP
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
