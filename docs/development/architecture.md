# Architecture & Standards Reference (Multi-Agent Code Review MCP Server)

This file is the single source of truth for all shared definitions, standards, specifications, schemas, and conventions. All phase files must reference and comply with the details here. No ambiguity or deferred decisions are permitted.

---

## Agent Roles & Responsibilities
- **Master Agent:**
  - Orchestrates the review workflow.
  - Delegates tasks to specialized agents.
  - Aggregates, validates, and serializes outputs.
  - Handles errors and retries.
  - Logs all actions and decisions.
- **Documentation Agent:**
  - Generates the following files for every codebase:
    - README.md: Project overview, setup, usage, architecture summary, contact info.
    - CONTRIBUTING.md: Contribution process, code style, PR review, branching, issue reporting.
    - CODE_OF_CONDUCT.md: Community standards, reporting process, enforcement.
    - API documentation: OpenAPI (swagger.yaml), GraphQL (schema.graphql), gRPC (proto files), with endpoint descriptions, request/response examples, error codes.
    - Architecture diagrams: SVG/PNG and markdown explanations (system, data flow, deployment).
    - Onboarding guide: Step-by-step for new devs, environment setup, common tasks.
    - Operations/runbooks: Monitoring, alerting, backup, recovery, deployment, rollback.
    - Security/compliance: Threat model, authentication, authorization, data privacy, regulatory notes.
    - Changelog.md: Version history, release notes, migration steps.
    - Testing: Test strategy, coverage report, CI config, example test cases.
    - Dependency/license: List of dependencies, license types, compliance notes.
    - Any additional files required by MCP or industry standards.
  - All files must use markdown unless otherwise specified (e.g., OpenAPI YAML, SVG diagrams).
  - All documentation must be clear, complete, and match best practices from top open-source and enterprise projects (see reference library).
- **Debt Agent:**
  - Scans codebase for technical debt using explicit checklists (see below).
  - Flags issues with severity (low/medium/high), remediation suggestions, and code references.
  - Reports must be in JSON, validated by pydantic.
- **Improvement Agent:**
  - Identifies improvement opportunities (refactoring, performance, maintainability, documentation gaps).
  - Provides actionable suggestions, rationale, and code references.
  - Reports in JSON, validated by pydantic.
- **Critical Issue Agent:**
  - Flags urgent problems (security, data loss, crashes, compliance violations).
  - Severity must be high, with remediation steps and code references.
  - Reports in JSON, validated by pydantic.

## MCP Server Endpoints
- `/upload_codebase`:
  - Accepts POST requests with codebase as zip/tar or directory structure.
  - Payload: multipart/form-data, field name `codebase`.
  - Max file size: 500MB. Reject with HTTP 413 if exceeded.
  - Response: 200 OK with JSON `{"status": "uploaded", "id": "<codebase_id>"}`.
  - Error codes: 400 (bad request), 413 (payload too large), 500 (server error).
- `/trigger_review`:
  - Accepts POST with JSON `{"id": "<codebase_id>"}`.
  - Triggers all agents in sequence: Documentation, Debt, Improvement, Critical Issue.
  - Response: 202 Accepted with JSON `{"status": "review_started", "id": "<review_id>"}`.
  - Error codes: 400, 404 (codebase not found), 500.
- `/get_results`:
  - Accepts GET with query param `id=<review_id>`.
  - Returns JSON with all agent outputs, validated and serialized.
  - Response: 200 OK with JSON `{"documentation": {...}, "debt": [...], "improvement": [...], "critical": [...]}`.
  - Error codes: 400, 404 (review not found), 500.

## Documentation Standards
- All documentation files must:
  - Use markdown (except OpenAPI YAML, SVG diagrams).
  - Include required sections as per template.
  - Be clear, complete, and actionable.
  - Reference codebase files and lines where relevant.
  - Use inclusive, professional language.
  - Pass linting (markdownlint, yamllint, etc.).

## Validation Schemas (Pydantic)
- All agent outputs must be validated using pydantic models:
  - Documentation: Each file as a string, with required sections.
  - Debt/Improvement/Critical: List of issues, each with fields:
    - `type`: string ("debt", "improvement", "critical")
    - `severity`: string ("low", "medium", "high")
    - `description`: string
    - `file`: string (relative path)
    - `line`: int (line number)
    - `suggestion`: string (for debt/improvement)
    - `remediation`: string (for critical)
    - `reference`: string (link to docs or standards)
  - All models must be unit tested with sample payloads.

## DSPy & LangChain Integration
- Each agent workflow is implemented as a DSPy/LangChain chain:
  - Steps: input parsing, prompt construction, LLM invocation, output validation, error handling.
  - Prompts must be explicit, reproducible, and versioned.
  - Memory: Use LangChain memory for context across steps.
  - Output: Must match pydantic schema exactly.
  - All chains must be unit/integration tested.

## Packaging & Distribution
- MCP server must be published as an NPM package, executable via npx (e.g., `npx my-mcp-server`).
- Package must include:
  - CLI entry point (`bin` field in package.json).
  - Usage documentation in README.md.
  - Versioning (semver), changelog, license.
  - Automated tests (Jest, Pytest, etc.).
  - All dependencies pinned to compatible versions.

## Security & Compliance
- Input validation: All endpoints must validate payloads and reject malformed requests.
- File size limits: 500MB max for uploads.
- No persistent storage of agent outputs.
- No additional compliance requirements.
- All error codes and messages must be documented and tested.

## Reference Library
- Documentation samples and best practices from:
  - Kubernetes, FastAPI, React, TensorFlow, Apache Kafka, Django, Node.js, etc.
  - All templates and examples must be stored in `/docs/reference/`.

---

*This file is exhaustive. All phase files must reference and comply with these standards. No ambiguity or deferred decisions permitted.*
