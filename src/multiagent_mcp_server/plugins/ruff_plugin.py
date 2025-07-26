import subprocess
import json
from typing import List, Dict, Any, Optional
from ..plugin_interface import StaticAnalysisPlugin

class RuffPlugin(StaticAnalysisPlugin):
    def name(self) -> str:
        return "ruff"

    def supported_languages(self) -> List[str]:
        return ["python"]

    def run(self, files: List[str], config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not files:
            return []
        # Ruff supports JSON output with --output-format=json
        cmd = ["ruff", "check", "--output-format=json"] + files
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)
            findings = []
            for item in output.get("diagnostics", []):
                findings.append({
                    "file": item.get("filename"),
                    "line": item.get("location", {}).get("row"),
                    "severity": "warning",  # Ruff doesn't provide severity, default to warning
                    "message": item.get("message"),
                    "tool": "ruff"
                })
            return findings
        except subprocess.CalledProcessError as e:
            return [{
                "tool": "ruff",
                "error": e.stderr or str(e)
            }]
        except Exception as e:
            return [{
                "tool": "ruff",
                "error": str(e)
            }]