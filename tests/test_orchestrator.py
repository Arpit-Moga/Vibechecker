import os
import tempfile
from src.multiagent_mcp_server.orchestrator import Orchestrator
from src.multiagent_mcp_server.plugins.ruff_plugin import RuffPlugin

def test_orchestrator_with_ruff(tmp_path):
    # Create a simple Python file with a lint issue
    code = "import os\n\n\nprint('hello')\n"
    test_file = tmp_path / "test.py"
    test_file.write_text(code)

    orchestrator = Orchestrator(plugin_classes=[RuffPlugin])
    results = orchestrator.run_plugins([str(test_file)])
    assert isinstance(results, list)
    assert any("tool" in r and r["tool"] == "ruff" for r in results)
    assert any("message" in r for r in results)