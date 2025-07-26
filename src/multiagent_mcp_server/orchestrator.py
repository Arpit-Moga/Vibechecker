import os
import importlib
import pkgutil
from concurrent.futures import ThreadPoolExecutor, as_completed
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

    def run_plugins(self, files: List[str]) -> List[Dict[str, Any]]:
        results = []
        with ThreadPoolExecutor(max_workers=len(self.plugins)) as executor:
            future_to_plugin = {executor.submit(plugin.run, files, self.config): plugin for plugin in self.plugins}
            for future in as_completed(future_to_plugin):
                plugin = future_to_plugin[future]
                try:
                    plugin_results = future.result()
                    for res in plugin_results:
                        res["tool"] = plugin.name()
                    results.extend(plugin_results)
                except Exception as e:
                    results.append({
                        "tool": plugin.name(),
                        "error": str(e)
                    })
        return results

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