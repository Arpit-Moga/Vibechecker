import subprocess
import json
from typing import List, Dict, Any, Optional
from ..plugin_interface import StaticAnalysisPlugin

class MypyPlugin(StaticAnalysisPlugin):
    def name(self) -> str:
        return "mypy"

    def supported_languages(self) -> List[str]:
        return ["python"]

    def run(self, files: List[str], config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not files:
            return []
        # Mypy supports JSON output with --show-error-codes --no-color-output --no-error-summary --error-format=json
        cmd = ["mypy", "--show-error-codes", "--no-color-output", "--no-error-summary", "--error-format=json"] + files
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)
            findings = []
            for item in output.get("errors", []):
                findings.append({
                    "file": item.get("path"),
                    "line": item.get("line"),
                    "severity": "error" if item.get("severity") == "error" else "note",
                    "message": item.get("message"),
                    "tool": "mypy"
                })
            return findings
        except subprocess.CalledProcessError as e:
            # mypy returns nonzero exit code if errors found, but still outputs JSON
            try:
                output = json.loads(e.stdout)
                findings = []
                for item in output.get("errors", []):
                    findings.append({
                        "file": item.get("path"),
                        "line": item.get("line"),
                        "severity": "error" if item.get("severity") == "error" else "note",
                        "message": item.get("message"),
                        "tool": "mypy"
                    })
                return findings
            except Exception:
                return [{
                    "tool": "mypy",
                    "error": e.stderr or str(e)
                }]
        except Exception as e:
            return [{
                "tool": "mypy",
                "error": str(e)
            }]