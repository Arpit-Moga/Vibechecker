"""
MCP-enabled server using FastMCP, exposing agent tools as MCP tools.
"""
from mcp.server.fastmcp import FastMCP
from mcp_server.debt_agent import DebtAgent
from mcp_server.improvement_agent import ImprovementAgent
from mcp_server.documentation_agent import DocumentationAgent
from mcp_server.critical_agent import CriticalAgent
from mcp_server.agent_utils import Settings
from mcp_server.models import AgentReport, DocumentationOutput
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("Multi-Agent MCP Server")

@mcp.tool()
def debt_review(code_directory: Optional[str] = None) -> AgentReport:
    """
    Run the DebtAgent on the specified code directory (default: Example-project).
    Returns a structured AgentReport with all detected technical debt issues and review.
    """
    settings = Settings(code_directory=code_directory or "Example-project")
    agent = DebtAgent(settings)
    logger.info(f"Running DebtAgent on {settings.code_directory}")
    return agent.run()

@mcp.tool()
def improvement_review(code_directory: Optional[str] = None) -> AgentReport:
    """
    Run the ImprovementAgent on the specified code directory (default: Example-project).
    Returns a structured AgentReport with all detected improvement opportunities and review.
    """
    settings = Settings(code_directory=code_directory or "Example-project")
    agent = ImprovementAgent(settings)
    logger.info(f"Running ImprovementAgent on {settings.code_directory}")
    return agent.run()

@mcp.tool()
def documentation_generate(code_directory: Optional[str] = None) -> DocumentationOutput:
    """
    Run the DocumentationAgent on the specified code directory (default: Example-project).
    Returns a structured DocumentationOutput with generated documentation and review.
    """
    settings = Settings(code_directory=code_directory or "Example-project")
    agent = DocumentationAgent(settings)
    logger.info(f"Running DocumentationAgent on {settings.code_directory}")
    return agent.generate_documentation()

@mcp.tool()
def critical_review(code_directory: Optional[str] = None) -> AgentReport:
    """
    Run the CriticalAgent on the specified code directory (default: Example-project).
    Returns a structured AgentReport with all detected critical issues and review.
    """
    settings = Settings(code_directory=code_directory or "Example-project")
    agent = CriticalAgent(settings)
    logger.info(f"Running CriticalAgent on {settings.code_directory}")
    return agent.run()


def main():
    """
    Entry point for running the MCP server. Uses streamable-http transport by default.
    """
    logger.info("Starting MCP server with FastMCP...")
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
