"""
Multi-Agent MCP Server - Production-ready codebase review and documentation.

A comprehensive Model Context Protocol (MCP) server providing specialized AI agents
for automated code review, documentation generation, and quality assurance.
"""

__version__ = "0.1.0"
__author__ = "Multi-Agent MCP Server Contributors"

# Intentionally do NOT import server (mcp, main) here to avoid side effects and double-import warnings
# from .server import mcp, main
from .models import AgentReport, DocumentationOutput, IssueOutput
from .config import Settings

__all__ = [
    # "mcp",
    # "main",
    "AgentReport",
    "DocumentationOutput",
    "IssueOutput",
    "Settings",
]