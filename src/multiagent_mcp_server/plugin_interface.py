from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class StaticAnalysisPlugin(ABC):
    """
    Abstract base class for static analysis tool plugins.
    """

    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the tool.
        """
        pass

    @abstractmethod
    def supported_languages(self) -> List[str]:
        """
        Returns a list of supported programming languages.
        """
        pass

    @abstractmethod
    def run(self, files: List[str], config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Runs the tool on the given files and returns a list of normalized findings.
        Each finding should be a dict with at least: file, line, severity, message, tool.
        """
        pass