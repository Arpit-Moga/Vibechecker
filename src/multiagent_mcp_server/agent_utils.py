"""
Shared agent utilities for MCP agents.
Includes: Settings, SupportedFileType, CodeFile, FileProcessor
"""
import os
from typing import Optional
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field
from dataclasses import dataclass

class SupportedFileType(str, Enum):
    PYTHON = ".py"

class DocumentationType(str, Enum):
    """Types of documentation that can be generated."""
    README = "README.md"
    CONTRIBUTING = "CONTRIBUTING.md"
    ONBOARDING = "ONBOARDING.md"
    RUNBOOK = "RUNBOOK.md"
    TESTING = "TESTING.md"
    DEPENDENCY = "DEPENDENCY.md"
    LICENSE = "LICENSE"

class TemplateFile(BaseModel):
    """Represents a documentation template."""
    name: str = Field(..., description="Template name")
    content: str = Field(..., description="Template content")
    doc_type: DocumentationType = Field(..., description="Documentation type")

@dataclass
class Settings:
    """Settings for agent configuration."""
    code_directory: str = "Example-project"
    template_directory: str = "templates"
    max_file_size_mb: float = 5.0
    max_files_to_process: int = 100
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    def __post_init__(self):
        # Override with environment variables if available
        env_code_dir = os.getenv("CODE_DIRECTORY")
        if env_code_dir:
            self.code_directory = env_code_dir
            
        env_template_dir = os.getenv("TEMPLATE_DIRECTORY")
        if env_template_dir:
            self.template_directory = env_template_dir
            
        env_max_size = os.getenv("MAX_FILE_SIZE_MB")
        if env_max_size:
            self.max_file_size_mb = float(env_max_size)
            
        env_max_files = os.getenv("MAX_FILES_TO_PROCESS")
        if env_max_files:
            self.max_files_to_process = int(env_max_files)
            
        env_google_key = os.getenv("GOOGLE_API_KEY")
        if env_google_key:
            self.google_api_key = env_google_key
            
        env_openai_key = os.getenv("OPENAI_API_KEY")
        if env_openai_key:
            self.openai_api_key = env_openai_key

class CodeFile(BaseModel):
    name: str = Field(...)
    path: str = Field(...)
    content: str = Field(...)
    size_bytes: int = Field(...)
    file_type: SupportedFileType = Field(...)

class FileProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.supported_extensions = {ext.value for ext in SupportedFileType}
    def get_code_files(self, code_dir: Path) -> dict:
        code_files = {}
        files_processed = 0
        for file_path in code_dir.rglob("*"):
            if files_processed >= self.settings.max_files_to_process:
                break
            if (file_path.is_file() and file_path.suffix in self.supported_extensions and
                not self._should_ignore_file(file_path)):
                file_size = file_path.stat().st_size
                max_size = self.settings.max_file_size_mb * 1024 * 1024
                if file_size > max_size:
                    continue
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                code_file = CodeFile(
                    name=file_path.name,
                    path=str(file_path.relative_to(code_dir)),
                    content=content,
                    size_bytes=file_size,
                    file_type=SupportedFileType(file_path.suffix)
                )
                code_files[file_path.name] = code_file
                files_processed += 1
        return code_files
    def get_template_files(self) -> dict:
        """Scan the template directory and return a dict of TemplateFile objects keyed by DocumentationType."""
        template_dir = Path(self.settings.template_directory)
        template_files = {}
        if not template_dir.exists():
            return template_files
        for doc_type in DocumentationType:
            template_path = template_dir / doc_type.value
            if template_path.exists() and template_path.is_file():
                with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                template_files[doc_type] = TemplateFile(
                    name=doc_type.value,
                    content=content,
                    doc_type=doc_type
                )
        return template_files
    def _should_ignore_file(self, file_path: Path) -> bool:
        ignore_patterns = {'__pycache__', '.git', '.pytest_cache', 'node_modules', '.venv', 'venv', '.env', 'dist', 'build'}
        return any(pattern in str(file_path) for pattern in ignore_patterns)
