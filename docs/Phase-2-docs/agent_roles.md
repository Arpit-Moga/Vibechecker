# Agent Roles & Responsibilities

This document specifies the roles and responsibilities of all agents in the Multi-Agent Code Review MCP Server, strictly following the standards in architecture.md.

---

## Master Agent
- Orchestrates the review workflow for each codebase.
- Delegates tasks to specialized agents in sequence.
- Aggregates, validates, and serializes outputs from all agents.
- Handles errors and retries for failed agent invocations.
- Logs all actions, decisions, and errors for auditability.

## Documentation Agent
- Generates comprehensive documentation for every codebase:
  - README.md: Project overview, setup, usage, architecture summary, contact info.
  - CONTRIBUTING.md: Contribution process, code style, PR review, branching, issue reporting.
  - CODE_OF_CONDUCT.md: Community standards, reporting process, enforcement.
  - API documentation: OpenAPI (swagger.yaml), GraphQL (schema.graphql), gRPC (proto files), endpoint descriptions, request/response examples, error codes.
  - Architecture diagrams: SVG/PNG and markdown explanations (system, data flow, deployment).
  - Onboarding guide: Step-by-step for new devs, environment setup, common tasks.
  - Operations/runbooks: Monitoring, alerting, backup, recovery, deployment, rollback.
  - Security/compliance: Threat model, authentication, authorization, data privacy, regulatory notes.
  - Changelog.md: Version history, release notes, migration steps.
  - Testing: Test strategy, coverage report, CI config, example test cases.
  - Dependency/license: List of dependencies, license types, compliance notes.
  - Any additional files required by MCP or industry standards.
- All documentation must be clear, complete, and match best practices from top open-source and enterprise projects.

## Debt Agent
- Scans the codebase for technical debt using explicit checklists.
- Flags issues with severity (low/medium/high), remediation suggestions, and code references.
- Outputs a JSON report validated by pydantic schemas.

## Improvement Agent
- Identifies improvement opportunities (refactoring, performance, maintainability, documentation gaps).
- Provides actionable suggestions, rationale, and code references.
- Outputs a JSON report validated by pydantic schemas.

## Critical Issue Agent
- Flags urgent problems (security, data loss, crashes, compliance violations).
- Severity must be high, with remediation steps and code references.
- Outputs a JSON report validated by pydantic schemas.

---

All agents must:
- Use explicit input/output formats as specified in agent_interfaces.md.
- Handle errors and retries as documented in orchestration_flow.md.
- Comply with all standards in architecture.md.
