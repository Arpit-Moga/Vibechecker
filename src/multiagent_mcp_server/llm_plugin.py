from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMPlugin(ABC):
    """
    Abstract base class for LLM integration plugins.
    """

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def explain_findings(self, findings: List[Dict[str, Any]], code: Optional[str] = None, batch_size: int = 10) -> List[Dict[str, Any]]:
        """
        Consumes findings (and optionally code) and returns LLM explanations or triage.
        """
        pass

    @abstractmethod
    def propose_fixes(self, findings: List[Dict[str, Any]], code: Optional[str] = None, batch_size: int = 10) -> List[Dict[str, Any]]:
        """
        Optionally propose auto-fixes for findings.
        """
        pass

class DummyLLMPlugin(LLMPlugin):
    """
    Example LLM plugin that returns dummy explanations for demonstration.
    Replace with real LLM integration as needed.
    """

    def name(self) -> str:
        return "dummy-llm"

    def explain_findings(self, findings: List[Dict[str, Any]], code: Optional[str] = None, batch_size: int = 10) -> List[Dict[str, Any]]:
        explained = []
        for i, finding in enumerate(findings):
            if i % batch_size == 0:
                # Simulate batching
                pass
            finding = finding.copy()
            finding["llm_explanation"] = f"Explanation for: {finding.get('message')}"
            explained.append(finding)
        return explained

    def propose_fixes(self, findings: List[Dict[str, Any]], code: Optional[str] = None, batch_size: int = 10) -> List[Dict[str, Any]]:
        # Dummy: no fixes proposed
        return []