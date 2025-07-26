from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class DocumentationOutput(BaseModel):
    files: Dict[str, str]  # filename -> content
    review: str

    @field_validator('files')
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
    type: str = Field(..., pattern='^(debt|improvement|critical)$')
    severity: str = Field(..., pattern='^(low|medium|high)$')
    description: str
    file: str
    line: int
    suggestion: Optional[str] = None  # For debt/improvement
    remediation: Optional[str] = None  # For critical
    reference: Optional[str] = None

from pydantic import model_validator, ValidationError

class IssueOutput(BaseModel):
    type: str = Field(..., pattern='^(debt|improvement|critical)$')
    severity: str = Field(..., pattern='^(low|medium|high)$')
    description: str
    file: str
    line: int
    suggestion: Optional[str] = None  # For debt/improvement
    remediation: Optional[str] = None  # For critical
    reference: Optional[str] = None

    @model_validator(mode="after")
    def check_required_fields(cls, values):
        errors = []
        t = values.type
        if t in ['debt', 'improvement'] and not values.suggestion:
            errors.append({"loc": ("suggestion",), "msg": "suggestion is required for debt/improvement issues", "type": "value_error"})
        if t == 'critical' and not values.remediation:
            errors.append({"loc": ("remediation",), "msg": "remediation is required for critical issues", "type": "value_error"})
        if t == 'critical' and values.severity != 'high':
            errors.append({"loc": ("severity",), "msg": "Critical issues must have severity 'high'", "type": "value_error"})
        if errors:
            raise ValidationError(errors, cls)
        return values


    @field_validator('suggestion', mode='before')
    def suggestion_required_for_debt_improvement(cls, v, info):
        values = info.data
        if values.get('type') in ['debt', 'improvement'] and not v:
            raise ValueError('suggestion is required for debt/improvement issues')
        return v
        if values.get('type') in ['debt', 'improvement'] and not v:
            raise ValueError('suggestion is required for debt/improvement issues')
        return v

    @field_validator('remediation', mode='before')
    def remediation_required_for_critical(cls, v, info):
        values = info.data
        if values.get('type') == 'critical' and not v:
            raise ValueError('remediation is required for critical issues')
        return v
        if values.get('type') == 'critical' and not v:
            raise ValueError('remediation is required for critical issues')
        return v

    @field_validator('severity', mode='before')
    def severity_for_critical(cls, v, info):
        values = info.data
        if values.get('type') == 'critical' and v != 'high':
            raise ValueError('Critical issues must have severity "high"')
        return v
        if values.get('type') == 'critical' and v != 'high':
            raise ValueError('Critical issues must have severity "high"')
        return v

class AgentReport(BaseModel):
    issues: List[IssueOutput]
    review: str

class AllAgentOutputs(BaseModel):
    documentation: DocumentationOutput
    debt: AgentReport
    improvement: AgentReport
    critical: AgentReport
