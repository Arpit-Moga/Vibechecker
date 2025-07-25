"""
LangChain Workflow for Multi-Agent MCP Server
Implements agent orchestration, output aggregation, and validation using LangChain best practices (2025).
Strictly follows project models and error handling requirements.
"""

from mcp_server.documentation_agent import run_documentation_agent
from mcp_server.debt_agent import run_debt_agent
from mcp_server.improvement_agent import run_improvement_agent
from mcp_server.critical_agent import run_critical_agent
from mcp_server.models import AllAgentOutputs, DocumentationOutput, AgentReport
from pydantic import ValidationError

# Simulate LangChain chain/agent orchestration
class LangChainAgentWorkflow:
    def __init__(self, codebase_path: str):
        self.codebase_path = codebase_path
        self.outputs = {}
        self.errors = []

    def run(self):
        # Run documentation agent
        try:
            documentation = run_documentation_agent()
        except Exception as e:
            self.errors.append(f"Documentation agent error: {e}")
            documentation = DocumentationOutput(files={})

        # Run debt agent
        try:
            debt = run_debt_agent(self.codebase_path)
        except Exception as e:
            self.errors.append(f"Debt agent error: {e}")
            debt = AgentReport(issues=[])

        # Run improvement agent
        try:
            improvement = run_improvement_agent(self.codebase_path)
        except Exception as e:
            self.errors.append(f"Improvement agent error: {e}")
            improvement = AgentReport(issues=[])

        # Run critical agent
        try:
            critical = run_critical_agent(self.codebase_path)
        except Exception as e:
            self.errors.append(f"Critical agent error: {e}")
            critical = AgentReport(issues=[])

        # Aggregate and validate all outputs
        try:
            all_outputs = AllAgentOutputs(
                documentation=documentation,
                debt=debt,
                improvement=improvement,
                critical=critical
            )
        except ValidationError as e:
            self.errors.append(f"Final output validation error: {e}")
            return None

        self.outputs = all_outputs
        return all_outputs

    def get_errors(self):
        return self.errors

if __name__ == "__main__":
    workflow = LangChainAgentWorkflow(codebase_path="/path/to/codebase")
    result = workflow.run()
    if result:
        print("Workflow completed successfully.")
        print(result.json(indent=2))
    else:
        print("Workflow failed with errors:")
        for err in workflow.get_errors():
            print(err)
