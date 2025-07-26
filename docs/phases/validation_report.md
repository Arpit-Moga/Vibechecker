# Validation Report: Agent Output Schemas

This report documents the validation of sample outputs against pydantic schemas, including all edge cases and handling strategies. All details strictly follow architecture.md.

---

## Validation Results

### DocumentationOutput
- **Valid Case:** All required fields present, correct types. Passes validation.
- **Invalid Case:** Non-string field (e.g., `contributing: 12345`). Fails with `ValidationError: str type expected`.
- **Edge Cases:**
  - Missing required fields: Fails with `ValidationError: field required`.
  - Extra fields: Ignored unless `extra=forbid` is set in schema.

### DebtIssue
- **Valid Case:** All fields present, correct types/values. Passes validation.
- **Invalid Case:**
  - Severity not in allowed values (e.g., `critical`): Fails with `ValidationError: unexpected value`.
  - Line not an int (e.g., `line: "forty-two"`): Fails with `ValidationError: int type expected`.
- **Edge Cases:**
  - Missing `suggestion`: Fails with `ValidationError: field required`.
  - Out-of-range line numbers: No explicit range, but negative values should be flagged in business logic.

### ImprovementIssue
- **Valid Case:** All fields present, correct types. Passes validation.
- **Invalid Case:**
  - Missing `line` or `suggestion`: Fails with `ValidationError: field required`.
- **Edge Cases:**
  - Severity must be one of `low`, `medium`, `high`.
  - Reference field is optional; missing is allowed.

### CriticalIssue
- **Valid Case:** All fields present, correct types/values. Passes validation.
- **Invalid Case:**
  - Severity not `high`: Fails with `ValidationError: unexpected value`.
  - Missing `remediation`: Fails with `ValidationError: field required`.
- **Edge Cases:**
  - File path must be string; empty string is allowed but flagged in business logic.
  - Line must be int; negative values should be flagged in business logic.

---

## Edge Case Handling Strategies
- All required fields are enforced by pydantic; missing fields trigger validation errors.
- Type mismatches (e.g., string instead of int) trigger validation errors.
- Allowed values for severity/type are enforced via validators or enums.
- Optional fields are allowed to be missing; business logic may further validate content.
- Out-of-range values (e.g., negative line numbers) are not blocked by schema but should be handled in agent logic.

## Summary
- All sample outputs from schema_examples.md were validated against schemas.py.
- All edge cases are handled via pydantic validation or business logic as specified.
- No ambiguity or deferred decisions; all validation rules are explicit.

---

See schema_tests.py for automated test coverage.