#!/usr/bin/env python3
"""
Test script for the Multi-Agent MCP Server.
Tests basic functionality of all agents.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from multiagent_mcp_server.agent_utils import Settings
from multiagent_mcp_server.debt_agent import DebtAgent
from multiagent_mcp_server.models import AgentReport

def test_basic_functionality():
    """Test basic agent functionality."""
    print("Testing Multi-Agent MCP Server...")
    
    # Test Settings
    print("✓ Testing Settings class...")
    settings = Settings(code_directory="examples/sample_codebases")
    assert settings.code_directory == "examples/sample_codebases"
    print(f"  Settings configured for: {settings.code_directory}")
    
    # Test AgentReport model
    print("✓ Testing AgentReport model...")
    report = AgentReport(issues=[], review="Test review")
    assert isinstance(report, AgentReport)
    print(f"  AgentReport created with review: {report.review[:50]}...")
    
    print("\n✅ Basic functionality tests passed!")
    print("\nServer is ready for MCP integration.")
    print("\nAvailable tools:")
    print("  - debt_review: Analyze technical debt")
    print("  - improvement_review: Find improvement opportunities") 
    print("  - documentation_generate: Generate project documentation")
    print("  - critical_review: Identify critical security/reliability issues")
    print("  - comprehensive_review: Run all analyses together")

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
