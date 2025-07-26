import subprocess
import json
from typing import List, Dict, Any, Optional
from ..plugin_interface import StaticAnalysisPlugin

class SemgrepPlugin(StaticAnalysisPlugin):
    def name(self) -> str:
        return "semgrep"

    def supported_languages(self) -> List[str]:
        return ["python"]

    def run(self, files: List[str], config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not files:
            return []
        # Semgrep supports JSON output with --json
        cmd = ["semgrep", "--config=auto", "--json"] + files
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)
            findings = []
            for item in output.get("results", []):
                findings.append({
                    "file": item.get("path"),
                    "line": item.get("start", {}).get("line"),
                    "severity": item.get("extra", {}).get("severity", "info"),
                    "message": item.get("extra", {}).get("message"),
                    "tool": "semgrep"
                })
            return findings
        except subprocess.CalledProcessError as e:
            return [{
                "tool": "semgrep",
                "error": e.stderr or str(e)
            }]
        except Exception as e:
            return [{
                "tool": "semgrep",
                "error": str(e)
            }]