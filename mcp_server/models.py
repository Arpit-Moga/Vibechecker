from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator

class DocumentationOutput(BaseModel):
    files: Dict[str, str]  # filename -> content

    @validator('files')
    def check_required_files(cls, v):
        required = [
            'README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
            'swagger.yaml', 'schema.graphql', 'architecture.svg',
            'ONBOARDING.md', 'RUNBOOK.md', 'SECURITY.md',
            'CHANGELOG.md', 'TESTING.md', 'DEPENDENCY.md', 'LICENSE'
        ]
        missing = [f for f in required if f not in v]
        if missing:
            raise ValueError(f"Missing required documentation files: {missing}")
        return v

class IssueOutput(BaseModel):
    type: str = Field(..., regex='^(debt|improvement|critical)$')
    severity: str = Field(..., regex='^(low|medium|high)$')
    description: str
    file: str
    line: int
    suggestion: Optional[str] = None  # For debt/improvement
    remediation: Optional[str] = None  # For critical
    reference: Optional[str] = None

    @validator('suggestion', always=True)
    def suggestion_required_for_debt_improvement(cls, v, values):
        if values.get('type') in ['debt', 'improvement'] and not v:
            raise ValueError('suggestion is required for debt/improvement issues')
        return v

    @validator('remediation', always=True)
    def remediation_required_for_critical(cls, v, values):
        if values.get('type') == 'critical' and not v:
            raise ValueError('remediation is required for critical issues')
        return v

    @validator('severity')
    def severity_for_critical(cls, v, values):
        if values.get('type') == 'critical' and v != 'high':
            raise ValueError('Critical issues must have severity "high"')
        return v

class AgentReport(BaseModel):
    issues: List[IssueOutput]

class AllAgentOutputs(BaseModel):
    documentation: DocumentationOutput
    debt: AgentReport
    improvement: AgentReport
    critical: AgentReport
