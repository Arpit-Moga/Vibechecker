#!/usr/bin/env python3
"""
Main entry point for the Multi-Agent MCP Server.

This module serves as the primary entry point for running the MCP server
both standalone and as a module.
"""

import sys
from pathlib import Path

# Add the src directory to Python path to ensure imports work
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

from multiagent_mcp_server.server import main

if __name__ == "__main__":
    main()
