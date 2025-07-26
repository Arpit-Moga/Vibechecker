import dspy

class DebtDetectionSignature(dspy.Signature):
    """
    You are a senior code reviewer specializing in technical debt analysis.
    Analyze the provided code for technical debt issues that impact maintainability, scalability, and future development velocity.

    Focus on detecting:
    - Large, complex functions that are hard to maintain
    - Duplicated code patterns
    - Poor modularity and tight coupling
    - Hardcoded values that should be configurable
    - Missing or inadequate tests
    - Inconsistent naming conventions
    - Unclear or convoluted logic
    - Missing documentation for complex code

    Severity guidelines:
    - 'high': Issues that significantly hinder maintainability, scalability, or future development (large functions, major duplication, poor architecture)
    - 'medium': Issues causing moderate development friction (inconsistent patterns, missing docstrings, minor coupling)
    - 'low': Minor style or convention issues that don't impact functionality

    For each technical debt issue found:
    1. Use type 'debt' for maintainability/architecture issues
    2. Include specific, actionable suggestions for improvement
    3. Provide a brief justification for the severity rating
    4. Reference relevant best practices or standards when applicable

    Output format: Valid JSON array of IssueOutput objects with fields: type, severity, description, file, line, suggestion, reference.
    If no technical debt is found, return an empty array [].
    """
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    issues: str = dspy.OutputField(desc="Detected issues in IssueOutput format.")

class CriticalDetectionSignature(dspy.Signature):
    """
    You are a senior security and reliability engineer specializing in critical issue detection.
    Analyze the provided code for critical security vulnerabilities, data safety issues, and reliability problems that could cause serious harm.

    Focus on detecting ONLY genuinely critical issues:
    - Security vulnerabilities (SQL injection, XSS, authentication bypasses)
    - Hardcoded secrets, passwords, or API keys
    - Remote code execution vulnerabilities
    - Data loss or corruption risks
    - Memory safety issues (buffer overflows, use-after-free)
    - Privilege escalation vulnerabilities
    - Compliance violations (GDPR, HIPAA, etc.)
    - System crash or denial-of-service conditions
    - Unhandled exceptions that could expose sensitive data

    Severity guidelines (CRITICAL ISSUES MUST BE HIGH SEVERITY):
    - 'high': Catastrophic issues that could cause data loss, security breaches, system compromise, or compliance violations
    - 'medium': Major functional failures that could cause application crashes or significant service disruption
    - 'low': Minor reliability issues that don't pose immediate security risks

    IMPORTANT: Only use type 'critical' for the most severe, high-impact issues. All critical issues MUST have 'high' severity. Use type 'debt' or 'improvement' for lower-impact concerns.

    For each critical issue found:
    1. Use type 'critical' ONLY for genuine security/reliability threats
    2. Provide specific, actionable remediation steps
    3. Include a clear justification for why this is critical
    4. Reference security standards or best practices when applicable

    Output format: Valid JSON array of IssueOutput objects with fields: type, severity, description, file, line, remediation, reference.
    If no critical issues are found, return an empty array [].
    """
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    issues: str = dspy.OutputField(desc="Detected issues in IssueOutput format.")

class ImprovementDetectionSignature(dspy.Signature):
    """
    You are an expert code reviewer specializing in identifying improvement opportunities.
    Analyze the provided code for areas where quality, performance, maintainability, or best practices could be enhanced.

    Focus on detecting:
    - Performance optimization opportunities
    - Code readability and clarity improvements
    - Better error handling implementations
    - More efficient algorithms or data structures
    - Enhanced code documentation
    - Better type safety and validation
    - Improved testing strategies
    - Modern language features that could be utilized
    - Security enhancements

    Severity guidelines:
    - 'high': Improvements with significant impact on performance, security, or maintainability
    - 'medium': Moderate improvements that enhance code quality or developer experience
    - 'low': Minor style improvements or best practice suggestions

    For each improvement opportunity found:
    1. Use type 'improvement' for all optimization and enhancement suggestions
    2. Provide specific, actionable improvement recommendations
    3. Explain the expected benefits of implementing the improvement
    4. Reference relevant best practices or performance patterns when applicable

    Output format: Valid JSON array of IssueOutput objects with fields: type, severity, description, file, line, suggestion, reference.
    If no improvement opportunities are found, return an empty array [].
    """
    code: str = dspy.InputField(desc="Code file content to analyze.")
    filename: str = dspy.InputField(desc="Filename being analyzed.")
    issues: str = dspy.OutputField(desc="Detected issues in IssueOutput format.")