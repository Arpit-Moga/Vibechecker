"""
Unified models for Multi-Agent MCP Server.

This module provides centralized Pydantic models for all agent outputs,
ensuring consistent validation and type safety across the system.
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from enum import Enum


class IssueType(str, Enum):
    """Unified issue types for agent reports."""
    MAINTAINABILITY = "maintainability"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    OTHER = "other"


class Severity(str, Enum):
    """Valid severity levels for issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IssueOutput(BaseModel):
    """
    Unified issue output model for all agent types.

    Validates that:
    - maintainability and performance issues have suggestions
    - security and compliance issues have remediation steps
    """
    type: IssueType = Field(..., description="Type of issue detected")
    severity: Severity = Field(..., description="Severity level of the issue")
    description: str = Field(..., min_length=10, description="Detailed description of the issue")
    file: str = Field(..., min_length=1, description="File path where issue was found")
    line: int = Field(..., ge=1, description="Line number where issue occurs")
    suggestion: Optional[str] = Field(None, description="Improvement suggestion for maintainability/performance issues")
    remediation: Optional[str] = Field(None, description="Remediation steps for security/compliance issues")
    reference: Optional[str] = Field(None, description="Reference URL or documentation")

    @model_validator(mode="after")
    def validate_issue_requirements(self) -> "IssueOutput":
        """Validate that required fields are present based on issue type."""
        if self.type in [IssueType.MAINTAINABILITY, IssueType.PERFORMANCE]:
            if not self.suggestion:
                raise ValueError(f"{self.type} issues must include a suggestion")
        if self.type in [IssueType.SECURITY, IssueType.COMPLIANCE]:
            if not self.remediation:
                raise ValueError(f"{self.type} issues must include remediation steps")
        return self


class AgentReport(BaseModel):
    """Standard report structure for all issue detection agents."""
    issues: List[IssueOutput] = Field(default_factory=list, description="List of detected issues (all types)")
    review: str = Field(..., min_length=20, description="Comprehensive review summary for all detected issues")
    
    @field_validator('review')
    @classmethod
    def validate_review(cls, v: str) -> str:
        """Ensure review is meaningful."""
        if len(v.strip()) < 20:
            raise ValueError("Review must be at least 20 characters long")
        return v.strip()


class DocumentationFile(BaseModel):
    """Represents a generated documentation file."""
    name: str = Field(..., min_length=1, description="Documentation file name")
    content: str = Field(..., min_length=10, description="Generated content")
    doc_type: str = Field(..., description="Type of documentation")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Ensure content is meaningful."""
        if len(v.strip()) < 10:
            raise ValueError("Documentation content must be at least 10 characters")
        return v.strip()


class DocumentationOutput(BaseModel):
    """Complete documentation generation output."""
    files: Dict[str, DocumentationFile] = Field(..., description="Generated documentation files")
    review: str = Field(..., min_length=20, description="Quality assessment and review")
    metadata: Dict[str, Union[str, int, float]] = Field(default_factory=dict, description="Generation metadata")
    
    @field_validator('files')
    @classmethod
    def validate_files(cls, v: Dict[str, DocumentationFile]) -> Dict[str, DocumentationFile]:
        """Ensure at least one file is generated."""
        if not v:
            raise ValueError("At least one documentation file must be generated")
        return v


class AllAgentOutputs(BaseModel):
    """Aggregated output from all agents (documentation and unified issue detection)."""
    documentation: DocumentationOutput = Field(..., description="Documentation generation results")
    issues: AgentReport = Field(..., description="Unified issue detection results (all types)")
    
    @property
    def total_issues(self) -> int:
        """Calculate total issues detected (all types)."""
        return len(self.issues.issues)
    
    @property
    def high_severity_count(self) -> int:
        """Count of all high severity issues (all types)."""
        return len([issue for issue in self.issues.issues if issue.severity == Severity.HIGH])


class AnalysisMetadata(BaseModel):
    """Metadata for analysis operations."""
    timestamp: str = Field(..., description="Analysis timestamp")
    agent_type: str = Field(..., description="Type of agent that performed analysis")
    total_files: int = Field(..., ge=0, description="Number of files analyzed")
    total_issues: int = Field(..., ge=0, description="Total issues found")
    analysis_duration: Optional[float] = Field(None, ge=0, description="Analysis duration in seconds")
    code_directory: str = Field(..., description="Directory that was analyzed")


# Export all models for easy importing
__all__ = [
    "IssueType",
    "Severity", 
    "IssueOutput",
    "AgentReport",
    "DocumentationFile",
    "DocumentationOutput",
    "AllAgentOutputs",
    "AnalysisMetadata"
]
