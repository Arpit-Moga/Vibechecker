import os
import importlib
import pkgutil
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from typing import List, Dict, Any, Optional, Type

from .plugin_interface import StaticAnalysisPlugin

class Orchestrator:
    """
    Orchestrates static analysis plugins and aggregates results.
    """

    def __init__(self, plugin_classes: Optional[List[Type[StaticAnalysisPlugin]]] = None, config: Optional[Dict[str, Any]] = None):
        self.plugins = [cls() for cls in (plugin_classes or [])]
        self.config = config or {}

    def register_plugin(self, plugin_cls: Type[StaticAnalysisPlugin]):
        self.plugins.append(plugin_cls())

    def run_plugins(self, files: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run all plugins in parallel and return a dict keyed by tool/plugin name.
        Applies a per-run timeout to prevent hangs in constrained environments.
        """
        results_by_plugin: Dict[str, List[Dict[str, Any]]] = {}
        if not self.plugins:
            return results_by_plugin

        timeout_sec = float(self.config.get("plugin_timeout_sec", 20))
        with ThreadPoolExecutor(max_workers=len(self.plugins)) as executor:
            future_to_plugin = {executor.submit(plugin.run, files, self.config): plugin for plugin in self.plugins}
            unfinished: Dict[Any, Any] = {}
            try:
                for future in as_completed(future_to_plugin, timeout=timeout_sec):
                    plugin = future_to_plugin[future]
                    try:
                        plugin_results = future.result()
                        results_by_plugin[plugin.name()] = plugin_results
                    except Exception as e:
                        results_by_plugin[plugin.name()] = [{
                            "tool": plugin.name(),
                            "error": str(e)
                        }]
            except TimeoutError:
                # Mark any unfinished plugins as timed out
                for future, plugin in future_to_plugin.items():
                    if not future.done():
                        future.cancel()
                        results_by_plugin[plugin.name()] = [{
                            "tool": plugin.name(),
                            "error": f"timeout after {timeout_sec}s"
                        }]
        return results_by_plugin

    def get_supported_languages(self) -> List[str]:
        langs = set()
        for plugin in self.plugins:
            langs.update(plugin.supported_languages())
        return list(langs)

    def aggregate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Simple deduplication by file/line/message/tool
        seen = set()
        deduped = []
        for r in results:
            key = (r.get("file"), r.get("line"), r.get("message"), r.get("tool"))
            if key not in seen:
                seen.add(key)
                deduped.append(r)
        return deduped
def plugin_results_to_markdown_tables(results_by_plugin: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Generate Markdown tables for each plugin's findings.
    """
    md = []
    for tool, findings in results_by_plugin.items():
        md.append(f"### {tool.capitalize()} Results")
        if not findings:
            md.append("_No findings._\n")
            continue
        # Get all possible columns
        columns = set()
        for f in findings:
            columns.update(f.keys())
        columns = [c for c in ["file", "line", "severity", "message", "error"] if c in columns] + [c for c in columns if c not in {"file", "line", "severity", "message", "error", "tool"}]
        if not columns:
            columns = list(findings[0].keys())
        # Table header
        md.append("| " + " | ".join(columns) + " |")
        md.append("|" + "|".join(["---"] * len(columns)) + "|")
        # Table rows
        for f in findings:
            row = []
            for col in columns:
                val = f.get(col, "")
                if isinstance(val, str):
                    val = val.replace("\n", " ").replace("|", "\\|")
                row.append(str(val))
            md.append("| " + " | ".join(row) + " |")
        md.append("")  # Blank line after table
    return "\n".join(md)