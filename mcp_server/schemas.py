from pydantic import BaseModel, Field, validator
from typing import List, Optional

# Documentation output: Each file as a string, with required sections
class DocumentationOutput(BaseModel):
    readme: str = Field(..., description="README.md content")
    contributing: str = Field(..., description="CONTRIBUTING.md content")
    code_of_conduct: str = Field(..., description="CODE_OF_CONDUCT.md content")
    api_docs: Optional[str] = Field(None, description="API documentation (OpenAPI YAML, GraphQL, gRPC)")
    diagrams: Optional[List[str]] = Field(None, description="SVG/PNG diagrams")
    onboarding: Optional[str] = Field(None, description="Onboarding guide")
    runbooks: Optional[str] = Field(None, description="Operations/runbooks")
    security: Optional[str] = Field(None, description="Security/compliance docs")
    changelog: Optional[str] = Field(None, description="Changelog.md content")
    testing: Optional[str] = Field(None, description="Testing strategy and examples")
    dependencies: Optional[str] = Field(None, description="Dependency/license list")

# Shared issue fields for Debt, Improvement, Critical
class IssueBase(BaseModel):
    type: str = Field(..., description="Issue type: debt, improvement, critical")
    severity: str = Field(..., description="Severity: low, medium, high")
    description: str = Field(..., description="Issue description")
    file: str = Field(..., description="Relative file path")
    line: int = Field(..., description="Line number")
    reference: Optional[str] = Field(None, description="Link to docs or standards")

class DebtIssue(IssueBase):
    suggestion: str = Field(..., description="Remediation suggestion")

class ImprovementIssue(IssueBase):
    suggestion: str = Field(..., description="Improvement suggestion")

class CriticalIssue(IssueBase):
    remediation: str = Field(..., description="Remediation steps")

# Agent outputs
class DebtOutput(BaseModel):
    issues: List[DebtIssue]

class ImprovementOutput(BaseModel):
    issues: List[ImprovementIssue]

class CriticalOutput(BaseModel):
    issues: List[CriticalIssue]

# Aggregated output for /get_results
class ReviewResults(BaseModel):
    documentation: DocumentationOutput
    debt: DebtOutput
    improvement: ImprovementOutput
    critical: CriticalOutput
