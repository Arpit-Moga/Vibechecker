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
        # Check mypy version for --error-format=json support
        try:
            version_result = subprocess.run(["mypy", "--version"], capture_output=True, text=True)
            version_str = version_result.stdout.strip().split()[-1]
            major, minor, *_ = map(int, version_str.split("."))
            supports_json = (major, minor) >= (1, 0)
        except Exception:
            supports_json = False

        if supports_json:
            cmd = ["mypy", "--error-format=json"] + files
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = json.loads(result.stdout)
                findings = []
                for item in output.get("errors", []):
                    findings.append({
                        "file": item.get("path"),
                        "line": item.get("line"),
                        "severity": item.get("severity", "error"),
                        "message": item.get("message"),
                        "tool": "mypy"
                    })
                return findings
            except Exception as e:
                return [{
                    "tool": "mypy",
                    "error": str(e)
                }]
        else:
            # Fallback: parse plain text output for older mypy
            cmd = ["mypy"] + files
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                findings = []
                for line in result.stdout.splitlines():
                    # Example: path/to/file.py:12: error: Incompatible types in assignment (expression has type "int", variable has type "str")
                    if ":" in line:
                        parts = line.split(":", 3)
                        if len(parts) >= 4:
                            file, line_no, _col, message = parts
                            findings.append({
                                "file": file.strip(),
                                "line": int(line_no.strip()),
                                "severity": "error",
                                "message": message.strip(),
                                "tool": "mypy"
                            })
                return findings
            except Exception as e:
                return [{
                    "tool": "mypy",
                    "error": str(e)
                }]