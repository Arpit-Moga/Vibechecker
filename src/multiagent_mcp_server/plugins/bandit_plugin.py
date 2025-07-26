import subprocess
import json
from typing import List, Dict, Any, Optional
from ..plugin_interface import StaticAnalysisPlugin

class BanditPlugin(StaticAnalysisPlugin):
    def name(self) -> str:
        return "bandit"

    def supported_languages(self) -> List[str]:
        return ["python"]

    def run(self, files: List[str], config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not files:
            return []
        # Bandit supports JSON output with -f json
        cmd = ["bandit", "-f", "json", "-q"] + files
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)
            findings = []
            for item in output.get("results", []):
                findings.append({
                    "file": item.get("filename"),
                    "line": item.get("line_number"),
                    "severity": item.get("issue_severity"),
                    "message": item.get("issue_text"),
                    "tool": "bandit"
                })
            return findings
        except subprocess.CalledProcessError as e:
            return [{
                "tool": "bandit",
                "error": e.stderr or str(e)
            }]
        except Exception as e:
            return [{
                "tool": "bandit",
                "error": str(e)
            }]