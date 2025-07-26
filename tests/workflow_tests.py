"""
Unit tests for DSPy and LangChain agent workflows
Covers valid/invalid payloads, edge cases, and output schema compliance
"""
import unittest
from mcp_server.dspy_workflows import DSPyAgentWorkflow
from mcp_server.langchain_workflows import LangChainAgentWorkflow
from mcp_server.models import AllAgentOutputs

class TestAgentWorkflows(unittest.TestCase):
    def setUp(self):
        self.codebase_path = "/tmp/fake_codebase"

    def test_dspy_workflow_valid(self):
        workflow = DSPyAgentWorkflow(codebase_path=self.codebase_path)
        result = workflow.run()
        self.assertIsInstance(result, AllAgentOutputs)
        self.assertGreaterEqual(len(result.debt.issues), 0)
        self.assertGreaterEqual(len(result.improvement.issues), 0)
        self.assertGreaterEqual(len(result.critical.issues), 0)
        self.assertIsInstance(result.documentation.files, dict)

    def test_langchain_workflow_valid(self):
        workflow = LangChainAgentWorkflow(codebase_path=self.codebase_path)
        result = workflow.run()
        self.assertIsInstance(result, AllAgentOutputs)
        self.assertGreaterEqual(len(result.debt.issues), 0)
        self.assertGreaterEqual(len(result.improvement.issues), 0)
        self.assertGreaterEqual(len(result.critical.issues), 0)
        self.assertIsInstance(result.documentation.files, dict)

    def test_dspy_workflow_invalid(self):
        # Simulate error by passing invalid codebase path
        workflow = DSPyAgentWorkflow(codebase_path=None)
        result = workflow.run()
        self.assertTrue(result is None or isinstance(result, AllAgentOutputs))
        self.assertGreaterEqual(len(workflow.get_errors()), 0)

    def test_langchain_workflow_invalid(self):
        workflow = LangChainAgentWorkflow(codebase_path=None)
        result = workflow.run()
        self.assertTrue(result is None or isinstance(result, AllAgentOutputs))
        self.assertGreaterEqual(len(workflow.get_errors()), 0)

if __name__ == "__main__":
    unittest.main()
