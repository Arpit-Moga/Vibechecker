# Technical Debt Checklist

## Patterns & Code Smells
- Large, monolithic functions/classes
- Duplicate code (copy-paste, repeated logic)
- Poor naming conventions
- Lack of comments or documentation
- Hardcoded values
- Magic numbers
- Deeply nested logic
- Excessive use of global variables
- Outdated dependencies
- Deprecated APIs
- Inconsistent formatting
- Unused code (dead code)
- Lack of error handling
- Tight coupling between modules
- Missing or inadequate tests

## Risk Factors
- High cyclomatic complexity
- Low test coverage
- Frequent bug reports in specific modules
- Unclear ownership or maintainers

## Severity Levels
- Low: Minor maintainability issues
- Medium: Moderate refactoring required
- High: Major risk to stability or maintainability

## Remediation Steps
- Refactor large functions/classes
- Remove duplicate or dead code
- Improve naming and documentation
- Replace hardcoded values with config
- Update dependencies
- Add or improve tests
- Decouple tightly coupled modules

## Example Issues
- Function `process_data` in `main.py` exceeds 100 lines (high severity)
- Variable `x` in `utils.py` is poorly named (low severity)
- Outdated dependency `requests==2.18.0` in `requirements.txt` (medium severity)

---

*All checklist items must be used by the Debt Agent. Outputs must match the pydantic schema in architecture.md.*
