# Project Overview: Multi-Agent Code Review MCP Server

**Goal:**  
Build a Python-only MCP (Model Context Protocol) server that reads an entire codebase and generates professional-grade documentation, highlights technical debt, scopes improvements, and flags critical issues. The system will use a multi-agent architecture, with a master agent orchestrating specialized agents. Output validation will be handled via pydantic, and agent prompting will be customized using dspy and langchain.

---

## Key Concepts & Technologies

### 1. MCP Server (Model Context Protocol)
- **Definition:** MCP is an open protocol and framework for standardizing how AI models (especially LLMs) interact with external tools, data, and APIs. MCP servers act as intermediaries, exposing controlled, secure interfaces for LLMs to access code, files, databases, etc.
- **Python Implementation:** FastMCP is the standard Python framework for building MCP servers, offering high-level abstractions and robust transport options.
- **Reference:** [MCP servers GitHub](https://github.com/modelcontextprotocol/servers), [FastMCP PyPI](https://pypi.org/project/fastmcp/)

### 2. Vibe Coders
- **Definition:** Vibe coding is an intent-driven, AI-assisted development style. Coders focus on expressing what they want, letting AI agents handle the details, and staying in a creative flow. The target audience expects tools that are intuitive, collaborative, and minimize micromanagement.
- **UX Implication:** The tool should be easy to use, provide actionable feedback, and support a “flow” state for developers.

### 3. FastMCP
- **Definition:** FastMCP is a Pythonic framework for building MCP servers. It simplifies server creation, agent orchestration, and transport bridging.
- **Role in Project:** Use FastMCP to implement the MCP server, manage agent communication, and expose endpoints for LLMs and other clients.

### 4. Pydantic
- **Definition:** Pydantic is a Python library for data validation and settings management using Python type annotations. It ensures structured, validated output from agents.
- **Role in Project:** Use pydantic models to validate and serialize agent responses (documentation, issue highlights, etc.).

### 5. DSPy
- **Definition:** DSPy (Declarative Self-improving Python) is a framework for building modular, self-improving LLM pipelines. It enables advanced prompt engineering, agent composition, and optimization.
- **Role in Project:** Use DSPy to customize agent prompting, optimize agent workflows, and compose complex review tasks.

### 6. LangChain
- **Definition:** LangChain is a popular Python framework for building LLM-powered applications. It provides abstractions for chains, agents, memory, and integrations.
- **Role in Project:** Use LangChain to build and manage multi-agent workflows, integrate with LLMs, and orchestrate agent collaboration under the master agent.

---

## Implementation Outline

1. **MCP Server Foundation**
   - Use FastMCP to build the server, define endpoints, and manage agent orchestration.
   - Expose APIs for codebase ingestion, agent review, and output retrieval.

2. **Multi-Agent Architecture**
   - Implement a master agent to coordinate specialized agents (documentation, technical debt, improvement scope, critical issues).
   - Each agent focuses on a specific review task, using DSPy and LangChain for prompt customization and workflow management.

3. **Professional Documentation Generation**
   - Agents analyze the codebase and generate documentation files (README, API docs, architecture guides, etc.) matching standards from large professional projects.

4. **Issue Highlighting**
   - Agents scan for technical debt, improvement opportunities, and critical issues, highlighting them (not auto-fixing).
   - Use best practices and research to define what constitutes technical debt and critical issues.

5. **Output Validation**
   - All agent outputs are validated and serialized using pydantic models, ensuring consistency and reliability.

6. **Vibe Coders UX**
   - Design the system for intent-driven, flow-state coding. Provide clear, actionable feedback and minimize friction.

---

## Example Workflow

1. **User uploads codebase to MCP server.**
2. **Master agent triggers specialized agents:**
   - Documentation Agent: Generates professional docs.
   - Debt Agent: Highlights technical debt.
   - Improvement Agent: Flags scope for improvements.
   - Critical Issue Agent: Flags urgent problems.
3. **Agents use DSPy and LangChain for advanced prompting and workflow composition.**
4. **All outputs are validated via pydantic and returned to the user in structured formats.**

---

## Next Steps

- Deep dive into FastMCP server setup and agent orchestration.
- Define pydantic models for output schemas.
- Design agent prompts and workflows using DSPy and LangChain.
- Research documentation standards from large professional Python projects for reference.
