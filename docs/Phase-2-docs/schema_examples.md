# Schema Examples (Valid & Invalid)

This document provides example payloads for all agent output schemas, including valid and invalid cases, strictly following architecture.md.

---

## DocumentationOutput (Valid)
```json
{
  "readme": "# Project Title\n...",
  "contributing": "# Contributing\n...",
  "code_of_conduct": "# Code of Conduct\n...",
  "api_docs": "openapi: 3.0.0\n...",
  "diagrams": ["<svg>...</svg>", "diagram.png"],
  "onboarding": "# Onboarding Guide\n...",
  "runbooks": "# Runbook\n...",
  "security": "# Security\n...",
  "changelog": "# Changelog\n...",
  "testing": "# Testing\n...",
  "dependencies": "# Dependencies\n..."
}
```

## DocumentationOutput (Invalid)
```json
{
  "readme": "# Project Title\n...",
  "contributing": 12345,  // Invalid: not a string
  "code_of_conduct": "# Code of Conduct\n..."
}
```

---

## DebtIssue (Valid)
```json
{
  "type": "debt",
  "severity": "high",
  "description": "Hardcoded credentials found.",
  "file": "src/app.py",
  "line": 42,
  "suggestion": "Use environment variables.",
  "reference": "https://docs.example.com/security"
}
```

## DebtIssue (Invalid)
```json
{
  "type": "debt",
  "severity": "critical",  // Invalid: not allowed value
  "description": "...",
  "file": "src/app.py",
  "line": "forty-two",      // Invalid: not an int
  "suggestion": "..."
}
```

---

## ImprovementIssue (Valid)
```json
{
  "type": "improvement",
  "severity": "medium",
  "description": "Refactor nested loops for readability.",
  "file": "src/utils.py",
  "line": 88,
  "suggestion": "Extract to helper function.",
  "reference": "https://docs.example.com/refactoring"
}
```

## ImprovementIssue (Invalid)
```json
{
  "type": "improvement",
  "severity": "low",
  "description": "...",
  "file": "src/utils.py",
  // Missing 'line' and 'suggestion' fields
}
```

---

## CriticalIssue (Valid)
```json
{
  "type": "critical",
  "severity": "high",
  "description": "SQL injection vulnerability detected.",
  "file": "src/db.py",
  "line": 12,
  "remediation": "Use parameterized queries.",
  "reference": "https://docs.example.com/sql-injection"
}
```

## CriticalIssue (Invalid)
```json
{
  "type": "critical",
  "severity": "medium",  // Invalid: must be 'high'
  "description": "...",
  "file": "src/db.py",
  "line": 12
  // Missing 'remediation' field
}
```

---

All examples are strictly validated against schemas.py. See validation_report.md for edge case handling.