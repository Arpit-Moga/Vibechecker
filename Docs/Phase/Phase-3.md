# Phase 3: Core Development

See [architecture.md] for all shared definitions, standards, and specifications. All steps below are fully detailed and must be followed exactly. No ambiguity or deferred decisions permitted.

---

## Step 1: MCP Server Implementation

### 1.1. Build Endpoints
- Implement `/upload_codebase`, `/trigger_review`, `/get_results` endpoints as specified in architecture.md.
- Enforce payload formats, file size limits, error codes, and response schemas.
- All endpoints must be unit/integration tested with valid and invalid payloads.
- Deliverable: `server.py`, `endpoint_tests.py`, and `endpoint_docs.md`.

### 1.2. Integrate Agent Orchestration
- Implement master agent logic to trigger specialized agents in sequence.
- Aggregate outputs, handle errors/retries, log all actions.
- Deliverable: `orchestration.py`, `orchestration_tests.py`, and `orchestration_docs.md`.

---

## Step 2: Specialized Agent Implementation

### 2.1. Documentation Agent
- Implement logic to generate all documentation files using templates and benchmarks from `/docs/templates/`.
- Validate outputs against pydantic models.
- Deliverable: `documentation_agent.py`, sample outputs in `/docs/generated/`, and `agent_tests.py`.

### 2.2. Debt, Improvement, Critical Issue Agents
- Implement logic for each agent using checklists and criteria from `/docs/criteria/`.
- Validate outputs against pydantic models.
- Deliverable: `debt_agent.py`, `improvement_agent.py`, `critical_agent.py`, sample outputs, and `agent_tests.py`.

---

## Step 3: DSPy & LangChain Workflows

### 3.1. Connect Agents to DSPy/LangChain
- Implement agent workflows as DSPy/LangChain chains using templates and specs from `/docs/architecture/`.
- Test prompt engineering and optimization strategies.
- Deliverable: `dspy_workflows.py`, `langchain_workflows.py`, and `workflow_tests.py`.

---

## Step 4: Output Validation
- Serialize and validate all agent outputs via pydantic models.
- Handle validation errors and edge cases as documented in Phase 2.
- Deliverable: `validation.py`, `validation_tests.py`, and `validation_docs.md`.

---

## Step 5: NPX Packaging
- Refactor MCP server for NPX distribution:
  - Add CLI entry point (`bin` in package.json).
  - Write usage documentation in README.md.
  - Ensure semver versioning, changelog, license, and automated tests.
- Publish to NPM and verify npx execution (`npx my-mcp-server`).
- Deliverable: `package.json`, `README.md`, `CHANGELOG.md`, `LICENSE`, and publish log.

---

## Phase 3 Deliverables Checklist
- [ ] `server.py` (Endpoints)
- [ ] `endpoint_tests.py` (Endpoint tests)
- [ ] `endpoint_docs.md` (Endpoint documentation)
- [ ] `orchestration.py` (Agent orchestration)
- [ ] `orchestration_tests.py` (Orchestration tests)
- [ ] `orchestration_docs.md` (Orchestration documentation)
- [ ] `documentation_agent.py` (Documentation agent)
- [ ] `debt_agent.py` (Debt agent)
- [ ] `improvement_agent.py` (Improvement agent)
- [ ] `critical_agent.py` (Critical issue agent)
- [ ] Sample outputs in `/docs/generated/`
- [ ] `agent_tests.py` (Agent tests)
- [ ] `dspy_workflows.py` (DSPy workflows)
- [ ] `langchain_workflows.py` (LangChain workflows)
- [ ] `workflow_tests.py` (Workflow tests)
- [ ] `validation.py` (Output validation)
- [ ] `validation_tests.py` (Validation tests)
- [ ] `validation_docs.md` (Validation documentation)
- [ ] `package.json` (NPX packaging)
- [ ] `README.md` (Usage docs)
- [ ] `CHANGELOG.md` (Version history)
- [ ] `LICENSE` (License)
- [ ] Publish log (NPM publish)

---

*All steps and deliverables are fully specified. No ambiguity or deferred decisions permitted. See architecture.md for all shared standards and schemas.*
