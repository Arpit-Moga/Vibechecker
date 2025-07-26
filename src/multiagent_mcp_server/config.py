"""
Centralized configuration management for Multi-Agent MCP Server.

This module provides unified configuration handling with environment variable
support, validation, and default values for all server components.
"""

import os
from typing import Optional, List
from pathlib import Path
from dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class Settings:
    """
    Centralized configuration settings for Multi-Agent MCP Server.
    
    This class provides configuration management with environment variable
    support and reasonable defaults for all components.
    """
    
    # Core paths
    code_directory: str = "."
    template_directory: str = "docs/templates"
    output_directory: str = "DOCUMENTATION"
    
    # LLM configuration
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    default_model: str = "gemini/gemini-2.5-flash"
    
    # Processing limits
    max_file_size_mb: float = 5.0
    max_files_to_process: int = 100
    supported_extensions: Optional[List[str]] = None
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    max_file_upload_size: int = 524288000  # 500MB
    
    # Agent enablement
    enable_debt_agent: bool = True
    enable_improvement_agent: bool = True
    enable_critical_agent: bool = True
    enable_documentation_agent: bool = True
    
    # Agent thresholds
    debt_severity_threshold: str = "low"
    improvement_severity_threshold: str = "low"
    critical_severity_threshold: str = "medium"
    
    def __post_init__(self):
        """Initialize settings from environment variables."""
        # Override with environment variables if available
        self.code_directory = os.getenv("CODE_DIRECTORY", self.code_directory)
        self.template_directory = os.getenv("TEMPLATE_DIRECTORY", self.template_directory)
        
        # LLM keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY", self.google_api_key)
        self.openai_api_key = os.getenv("OPENAI_API_KEY", self.openai_api_key)
        
        # Processing limits
        env_max_size = os.getenv("MAX_FILE_SIZE_MB")
        if env_max_size:
            self.max_file_size_mb = float(env_max_size)
            
        env_max_files = os.getenv("MAX_FILES_TO_PROCESS")
        if env_max_files:
            self.max_files_to_process = int(env_max_files)
        
        # Server config
        self.host = os.getenv("MCP_HOST", self.host)
        env_port = os.getenv("MCP_PORT")
        if env_port:
            self.port = int(env_port)
        self.log_level = os.getenv("LOG_LEVEL", self.log_level).upper()
        
        env_upload_size = os.getenv("MCP_MAX_FILE_SIZE")
        if env_upload_size:
            self.max_file_upload_size = int(env_upload_size)
        
        # Set default supported extensions
        if self.supported_extensions is None:
            self.supported_extensions = [".py"]
    
    @property
    def has_google_key(self) -> bool:
        """Check if Google API key is available."""
        return bool(self.google_api_key)
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.openai_api_key)
    
    @property
    def has_any_llm_key(self) -> bool:
        """Check if any LLM API key is available."""
        return self.has_google_key or self.has_openai_key
    
    @property
    def absolute_code_directory(self) -> Path:
        """Get absolute path to code directory."""
        return Path(self.code_directory).resolve()
    
    @property
    def absolute_template_directory(self) -> Path:
        """Get absolute path to template directory."""
        return Path(self.template_directory).resolve()
    
    def get_output_directory(self, base_path: Optional[str] = None) -> Path:
        """Get output directory path."""
        if base_path:
            return Path(base_path) / self.output_directory
        return self.absolute_code_directory / self.output_directory
    
    def validate_environment(self) -> List[str]:
        """Validate the environment and return any warnings."""
        warnings = []
        
        if not self.has_any_llm_key:
            warnings.append(
                "No LLM API keys found. Set GOOGLE_API_KEY or OPENAI_API_KEY "
                "environment variables for full functionality."
            )
        
        if not self.absolute_code_directory.exists():
            warnings.append(f"Code directory does not exist: {self.absolute_code_directory}")
        
        # Template directory is optional
        if not self.absolute_template_directory.exists():
            warnings.append(f"Template directory does not exist: {self.absolute_template_directory}")
        
        # Validate file size limits
        if self.max_file_size_mb <= 0 or self.max_file_size_mb > 100:
            warnings.append(f"Invalid max_file_size_mb: {self.max_file_size_mb}. Should be between 0.1 and 100.")
        
        if self.max_files_to_process <= 0:
            warnings.append(f"Invalid max_files_to_process: {self.max_files_to_process}. Should be > 0.")
        
        # Validate log level
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if self.log_level not in valid_levels:
            warnings.append(f"Invalid log level: {self.log_level}. Should be one of {valid_levels}")
        
        return warnings
    
    def get_preferred_llm_config(self) -> tuple[str, Optional[str]]:
        """Get the preferred LLM configuration (model, api_key)."""
        if self.has_google_key:
            return "gemini/gemini-2.5-flash", self.google_api_key
        elif self.has_openai_key:
            return "openai/gpt-3.5-turbo", self.openai_api_key
        else:
            return self.default_model, None


class AdvancedSettings(BaseSettings):
    """
    Advanced settings using Pydantic BaseSettings for complex environment handling.
    This is an alternative to the simple Settings class above.
    """
    
    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Core settings
    code_directory: str = "."
    template_directory: str = "docs/templates"
    output_directory: str = "DOCUMENTATION"
    
    # LLM configuration  
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    default_model: str = "gemini/gemini-2.5-flash"
    
    # Processing limits
    max_file_size_mb: float = 5.0
    max_files_to_process: int = 100
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    max_file_upload_size: int = 524288000
    
    # Agent configuration
    enable_debt_agent: bool = True
    enable_improvement_agent: bool = True
    enable_critical_agent: bool = True
    enable_documentation_agent: bool = True
    
    @property
    def has_any_llm_key(self) -> bool:
        """Check if any LLM API key is available."""
        return bool(self.google_api_key or self.openai_api_key)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment (useful for testing)."""
    global _settings
    _settings = Settings()
    return _settings


def create_advanced_settings() -> AdvancedSettings:
    """Create advanced settings instance using Pydantic."""
    return AdvancedSettings()


# Export main classes and functions
__all__ = [
    "Settings",
    "AdvancedSettings",
    "get_settings",
    "reload_settings",
    "create_advanced_settings"
]