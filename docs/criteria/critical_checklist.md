# Critical Issue Checklist

## Patterns & Risks
- Security vulnerabilities (e.g., SQL injection, XSS)
- Data loss or corruption risks
- Application crashes or unhandled exceptions
- Compliance violations (GDPR, HIPAA, etc.)
- Hardcoded credentials or secrets
- Unprotected endpoints
- Missing authentication/authorization
- Unsafe file operations
- Use of deprecated or insecure libraries
- Failure to log critical events

## Severity Levels
- High: All critical issues must be high severity

## Remediation Steps
- Patch vulnerabilities immediately
- Add authentication/authorization
- Implement proper error handling
- Remove hardcoded secrets
- Update or replace insecure libraries
- Add compliance documentation

## Example Issues
- SQL injection vulnerability in `db.py` (high severity)
- Unhandled exception in `main.py` causing crash (high severity)
- Hardcoded password in `config.py` (high severity)

---

*All checklist items must be used by the Critical Issue Agent. Outputs must match the pydantic schema in architecture.md.*
