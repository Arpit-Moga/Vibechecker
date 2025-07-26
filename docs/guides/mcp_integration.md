# MCP Integration Guide

This document explains how to integrate the Multi-Agent MCP Server with your MCP-compatible AI assistants.

## Quick Setup

### 1. Install Dependencies

```bash
cd /path/to/multi-agent-mcp-server
uv sync
```

### 2. Add to MCP Configuration

Add this to your MCP configuration file (e.g., `mcp_settings.json`):

```json
{
  "mcpServers": {
    "multi-agent-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--project", "/path/to/multi-agent-mcp-server",
        "python",
        "-m", "multiagent_mcp_server.server"
      ],
      "cwd": "/path/to/multi-agent-mcp-server",
      "disabled": false,
      "alwaysAllow": [
        "debt_review",
        "improvement_review", 
        "documentation_generate",
        "critical_review",
        "comprehensive_review"
      ],
      "description": "Multi-agent code review and documentation system"
    }
  }
}
```

### 3. Restart Your AI Assistant

Restart your MCP-compatible AI assistant (Roo, Cline, etc.) to load the new server.

## Available Tools

Once configured, you'll have access to these MCP tools:

### `debt_review`
- **Purpose**: Analyze technical debt in your codebase
- **Usage**: "Analyze this project for technical debt"
- **Returns**: Structured report with debt issues and suggestions

### `improvement_review`
- **Purpose**: Find improvement opportunities
- **Usage**: "What improvements can be made to this code?"
- **Returns**: Detailed improvement recommendations

### `documentation_generate` 
- **Purpose**: Generate comprehensive project documentation
- **Usage**: "Generate documentation for this project"
- **Returns**: Complete documentation suite (README, CONTRIBUTING, etc.)

### `critical_review`
- **Purpose**: Identify critical security and reliability issues
- **Usage**: "Check this code for critical issues"
- **Returns**: High-priority security and reliability findings

### `comprehensive_review`
- **Purpose**: Run all analyses together
- **Usage**: "Perform a comprehensive code review"
- **Returns**: Combined results from all agents with summary statistics

## Example Usage

Once set up, you can use natural language with your AI assistant:

- "Analyze the current directory for technical debt"
- "Generate documentation for my Python project"
- "Check this codebase for critical security issues"
- "Perform a complete code review of the src/ directory"

## Configuration Options

### Environment Variables

- `CODE_DIRECTORY`: Default directory to analyze (default: current working directory)
- `TEMPLATE_DIRECTORY`: Location of documentation templates
- `MAX_FILE_SIZE_MB`: Maximum file size to process (default: 5.0)
- `MAX_FILES_TO_PROCESS`: Maximum number of files to analyze (default: 100)
- `GOOGLE_API_KEY`: Google AI API key for LLM access
- `OPENAI_API_KEY`: OpenAI API key for LLM access

### Logging

Set log level with `--log-level` argument:
```bash
uv run python -m multiagent_mcp_server.server --log-level DEBUG
```

## Troubleshooting

### Server Won't Start
1. Ensure all dependencies are installed: `uv sync`
2. Check Python path in MCP configuration
3. Verify working directory is correct

### No Tools Available
1. Check MCP configuration syntax
2. Restart your AI assistant
3. Check server logs for errors

### Import Errors
1. Ensure you're using `uv run` for execution
2. Check that the project structure is intact
3. Verify all agent files have correct imports

## Verification

Run the verification script to check your setup:

```bash
uv run python scripts/verify_mcp_setup.py
```

This will validate:
- All imports work correctly
- Core functionality is available
- MCP server can be loaded
- Configuration appears correct
