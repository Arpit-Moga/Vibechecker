#!/usr/bin/env python3
"""
Entry script for smithery.ai deployment.
This script sets up the Python path and runs the MCP server.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the server
from multiagent_mcp_server.server import main

if __name__ == "__main__":
    main()
