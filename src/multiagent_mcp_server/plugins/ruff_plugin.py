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
            # Do not use check=True, so we can parse output even if exit code is 1 (lint errors)
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = json.loads(result.stdout)
            findings = []
            # Ruff 0.4.x and later: output is a list of dicts, not a dict with "diagnostics"
            if isinstance(output, list):
                for item in output:
                    findings.append({
                        "file": item.get("filename"),
                        "line": item.get("location", {}).get("row"),
                        "severity": "warning",  # Ruff doesn't provide severity, default to warning
                        "message": item.get("message"),
                        "tool": "ruff"
                    })
            elif isinstance(output, dict) and "diagnostics" in output:
                for item in output["diagnostics"]:
                    findings.append({
                        "file": item.get("filename"),
                        "line": item.get("location", {}).get("row"),
                        "severity": "warning",
                        "message": item.get("message"),
                        "tool": "ruff"
                    })
            return findings
        except Exception as e:
            return [{
                "tool": "ruff",
                "error": str(e)
            }]