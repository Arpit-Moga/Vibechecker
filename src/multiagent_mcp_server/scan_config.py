from typing import List, Dict, Any

DEFAULT_CONFIG = {
    "scan_mode": "quick",  # "quick" or "deep"
    "tools": {
        "quick": ["ruff", "bandit"],
        "deep": ["ruff", "bandit", "mypy", "semgrep"]
    },
    "execution": {
        "synchronous": ["ruff", "bandit"],
        "asynchronous": ["mypy", "semgrep"]
    }
}

def get_tools_for_mode(mode: str) -> List[str]:
    return DEFAULT_CONFIG["tools"].get(mode, DEFAULT_CONFIG["tools"]["quick"])

def get_execution_type(tool: str) -> str:
    if tool in DEFAULT_CONFIG["execution"]["synchronous"]:
        return "synchronous"
    return "asynchronous"

def merge_user_config(user_config: Dict[str, Any]) -> Dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    config.update(user_config or {})
    return config