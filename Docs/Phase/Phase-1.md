# Phase 1: Foundation & Research

See [architecture.md] for all shared definitions, standards, and specifications. All steps below are fully detailed and must be followed exactly. No ambiguity or deferred decisions permitted.

---

## Step 1: Deep Dive into FastMCP

### 1.1. Study FastMCP Documentation and Example Servers
- Read [FastMCP PyPI](https://pypi.org/project/fastmcp/) and [MCP servers GitHub](https://github.com/modelcontextprotocol/servers) in full.
- Document:
  - How to initialize a FastMCP server (required imports, main entry point, config options).
  - How to define endpoints (`/upload_codebase`, `/trigger_review`, `/get_results`) with exact payloads and error codes as in architecture.md.
  - How to orchestrate agents and handle errors/retries.
  - Security features: file size limits, input validation, error handling.
- Deliverable: `fastmcp_summary.md` with all findings, code snippets, and best practices.

### 1.2. Prototype Minimal MCP Server
- Implement a Python FastMCP server with all endpoints as specified in architecture.md.
- Endpoints must:
  - Accept and validate payloads exactly as described (multipart/form-data for uploads, JSON for review triggers, etc.).
  - Enforce file size limits (500MB max).
  - Return documented error codes/messages for all failure cases.
- Use placeholder agent logic (return static sample outputs matching pydantic schemas).
- Deliverable: `prototype_server.py` and `endpoint_spec.md` documenting all endpoint behaviors and payloads.

### 1.3. Document Protocol Compliance
- For each endpoint, list:
  - Required headers, payload schemas, authentication (if any), error codes, and sample requests/responses.
  - How each endpoint matches MCP protocol standards.
- Deliverable: `protocol_compliance.md` with full endpoint specs and compliance checklist.

---

## Step 2: Research Professional Documentation Standards

### 2.1. Build Reference Library
- Select 10 top open-source/enterprise projects (Kubernetes, FastAPI, React, TensorFlow, Apache Kafka, Django, Node.js, etc.).
- For each, collect:
  - README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, API docs, architecture diagrams, onboarding guides, runbooks, security/compliance docs, changelog, testing strategy, dependency/license docs.
  - Store all samples in `/docs/reference/`.
- Deliverable: `/docs/reference/` directory with all files, plus `reference_index.md` listing sources and file types.

### 2.2. Define Templates and Quality Benchmarks
- For each documentation file type, create a markdown template specifying:
  - Required sections, formatting, tone, code references, links to standards.
  - Example content for each section.
- Quality benchmarks:
  - Clarity, completeness, actionable guidance, professional language, compliance with linting tools.
- Deliverable: `/docs/templates/` directory with all templates, plus `quality_benchmarks.md`.

---

## Step 3: Define Technical Debt & Critical Issue Criteria

### 3.1. Research and Document Criteria
- Review academic papers, industry blogs, and standards (SEI, IEEE, Google Engineering Practices).
- For each agent (Debt, Improvement, Critical Issue), create:
  - Explicit checklists of patterns, code smells, risk factors, severity levels, remediation steps.
  - Example issues for each checklist item.
- Deliverable: `/docs/criteria/` directory with `debt_checklist.md`, `improvement_checklist.md`, `critical_checklist.md`.

### 3.2. Finalize Agent Checklists
- All checklists must:
  - Be exhaustive, with no “TBD” or “decide later.”
  - Specify how LLMs will use them (prompt examples, output formats).
  - Include sample JSON outputs matching pydantic schemas in architecture.md.
- Deliverable: Finalized checklists and sample outputs in `/docs/criteria/`.

---

## Phase 1 Deliverables Checklist
- [ ] `fastmcp_summary.md` (FastMCP architecture and best practices)
- [ ] `prototype_server.py` (Minimal MCP server)
- [ ] `endpoint_spec.md` (Endpoint documentation)
- [ ] `protocol_compliance.md` (Protocol compliance checklist)
- [ ] `/docs/reference/` (Reference documentation samples)
- [ ] `reference_index.md` (Index of reference docs)
- [ ] `/docs/templates/` (Documentation templates)
- [ ] `quality_benchmarks.md` (Quality standards)
- [ ] `/docs/criteria/` (Agent checklists)
- [ ] Sample outputs for each agent in `/docs/criteria/`

---

*All steps and deliverables are fully specified. No ambiguity or deferred decisions permitted. See architecture.md for all shared standards and schemas.*
