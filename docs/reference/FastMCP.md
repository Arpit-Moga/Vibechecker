# FastMCP Summary

This document provides a comprehensive summary of how to build, configure, and secure a Model Context Protocol (MCP) server using the FastMCP framework, based on the provided documentation.

## 1. Initializing a FastMCP Server

Initializing a server is the first step in any FastMCP application. It involves creating an instance of the `FastMCP` class, which serves as the container for all tools, resources, and prompts.

### Required Imports and Instantiation
A basic server can be created with a single import and instantiation. It's best practice to include a `__name__ == "__main__"` block to make the server runnable.

```python
# Required import for the server
from fastmcp import FastMCP

# Instantiate the server, giving it a human-readable name
mcp = FastMCP(name="CodeReviewServer")

# Add tools and resources here...

# Best practice: make the server runnable
if __name__ == "__main__":
    # Runs the server using the default STDIO transport
    mcp.run()
```

### Key Configuration Options
The `FastMCP` constructor accepts several arguments to configure its behavior at a high level.

*   `name` (str): A human-readable name for the server.
*   `instructions` (str): A description to guide clients on how to interact with the server.
*   `lifespan` (callable): An async context manager for handling startup and shutdown logic, like database connections.
*   `on_duplicate_tools` (str): Defines behavior for duplicate tool names ('error', 'warn', 'replace', 'ignore').
*   `mask_error_details` (bool): If `True`, hides detailed exception messages from clients for security.

```python
mcp = FastMCP(
    name="SecureCodeReviewServer",
    instructions="This server provides tools to analyze and review codebases.",
    on_duplicate_tools="error",
    mask_error_details=True
)
```

## 2. Defining Endpoints (Tools & Resources)

FastMCP exposes functionality through **Tools** (for actions) and **Resources** (for data retrieval). The specific endpoints requested (`/upload_codebase`, `/trigger_review`, `/get_results`) are not explicitly defined in the documentation. However, this section explains how to create analogous, powerful endpoints using FastMCP's core features.

### Defining Tools for Actions

Tools are Python functions that an LLM can execute, analogous to `POST` endpoints in a REST API. They are ideal for performing actions, such as uploading data or starting a process.

You define a tool by decorating a function with `@mcp.tool`. FastMCP automatically infers the tool's name, description (from the docstring), and input schema (from type hints).

**Example: Simulating `/upload_codebase` and `/trigger_review`**

To handle complex data payloads, such as a codebase, you can use Pydantic models for automatic validation and parsing.

```python
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List

mcp = FastMCP(name="CodeReviewServer")

class CodeFile(BaseModel):
    path: str
    content: str

class Codebase(BaseModel):
    repo_url: str
    files: List[CodeFile]

@mcp.tool
def analyze_codebase(codebase: Codebase) -> dict:
    """
    Analyzes a given codebase for quality and returns a summary.
    This tool serves as a combined upload and trigger mechanism.
    """
    num_files = len(codebase.files)
    total_lines = sum(len(file.content.splitlines()) for file in codebase.files)

    # In a real application, this would trigger a complex review process.
    review_id = "review_12345"

    return {
        "status": "Analysis started",
        "review_id": review_id,
        "files_analyzed": num_files,
        "total_lines": total_lines
    }
```

### Defining Resources for Data Retrieval

Resources provide read-only access to data, similar to `GET` endpoints. For a functionality like `/get_results`, a **Resource Template** is the ideal pattern. It allows clients to request data based on parameters in the URI.

**Example: Simulating `/get_results`**

This example creates a dynamic resource that retrieves analysis results using a `review_id`.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="CodeReviewServer")

# Dummy data for demonstration
mock_results_db = {
    "review_12345": {
        "status": "Completed",
        "score": 85,
        "issues_found": 12,
        "summary": "The codebase is well-structured but has minor performance issues."
    }
}

@mcp.resource("reviews://{review_id}/results")
def get_review_results(review_id: str) -> dict:
    """Retrieves the analysis results for a given review ID."""
    if review_id in mock_results_db:
        return mock_results_db[review_id]
    else:
        # Raising a specific error is handled gracefully by FastMCP
        from fastmcp.exceptions import ResourceError
        raise ResourceError(f"Results for review ID '{review_id}' not found.")
```

## 3. Handling Errors and Retries

FastMCP provides robust mechanisms for managing errors and implementing retry logic.

### Error Handling in Tools and Resources

*   **Standard Exceptions**: You can raise standard Python exceptions (e.g., `ValueError`, `FileNotFoundError`). If `mask_error_details` is `False`, the exception message will be sent to the client.
*   **FastMCP Exceptions**: For more control, raise specific exceptions like `fastmcp.exceptions.ToolError` or `ResourceError`. The messages from these exceptions are always sent to the client, regardless of the `mask_error_details` setting.

```python
from fastmcp.exceptions import ToolError

@mcp.tool
def divide(a: int, b: int) -> float:
    """Divides two numbers."""
    if b == 0:
        raise ToolError("Division by zero is not permitted.")
    return a / b
```

### Retry Logic with Middleware

For handling transient failures, such as network issues, FastMCP provides `RetryMiddleware`. This middleware can automatically retry a failed operation with an exponential backoff strategy.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import RetryMiddleware
from httpx import TimeoutException # Example of a transient error

mcp = FastMCP(name="ResilientServer")

# Configure middleware to retry up to 3 times on specific exceptions
mcp.add_middleware(
    RetryMiddleware(max_retries=3, retry_exceptions=(TimeoutException,))
)
```

## 4. Security Features

FastMCP includes several features for building secure servers.

### Authentication
FastMCP supports securing HTTP-based servers with Bearer Token authentication. The `BearerAuthProvider` validates JWTs using a public key or a JWKS URI, ensuring that the server does not need to handle private keys or secrets.

```python
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider

# Public key for verifying JWT signatures
public_key = """-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----"""

auth_provider = BearerAuthProvider(
    public_key=public_key,
    issuer="https://my-auth-server.com/",
    audience="my-mcp-server"
)

mcp = FastMCP(name="SecureServer", auth=auth_provider)
```

### Input Validation
FastMCP leverages Python type hints and Pydantic for automatic, robust input validation. You can define complex validation rules directly in your tool's signature using `Annotated` and `Field`.

```python
from typing import Annotated
from pydantic import Field

@mcp.tool
def create_user(
    username: Annotated[str, Field(min_length=3, max_length=20)],
    age: Annotated[int, Field(ge=18, description="User must be 18 or older.")]
) -> dict:
    """Creates a user with validated input."""
    return {"status": "User created", "username": username}
```

### File Size Limits
The provided documentation does not contain explicit information about configuring file size limits for uploads. This would typically be handled at the web server (e.g., NGINX) or application framework level when using an HTTP transport.

### STDIO Isolation
When using the default STDIO transport, FastMCP runs servers in a sandboxed environment. This is a key security feature that prevents the server process from inheriting environment variables or having broad access to the host system.

## 5. Agent Orchestration

The term "agent orchestration" is broad. While the provided text does not detail a specific orchestration framework within FastMCP itself, it provides the necessary building blocks for it. A separate framework, `fast-agent`, is mentioned, which is designed for creating and testing MCP-capable agents and workflows.

Within FastMCP, orchestration can be achieved by:

*   **Chaining Tool Calls**: A tool can call other tools via an in-memory `Client`, allowing for complex workflows.
*   **Using the Context Object**: The `Context` object allows tools to perform advanced actions like logging, reporting progress, or even requesting LLM completions from the client (`ctx.sample()`), enabling more dynamic agent-like behaviors.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Orchestrator")

@mcp.tool
async def main_task(prompt: str, ctx: Context) -> str:
    """Orchestrates a series of actions."""
    await ctx.info("Starting main task...")

    # Step 1: Call another tool on the same server for data
    # (Requires creating a client to self)
    data = "some data" # In a real scenario, this would be a tool call

    # Step 2: Use the client's LLM to reason about the data
    analysis = await ctx.sample(f"Analyze the following: {data}")

    await ctx.info("Task complete.")
    return analysis.text
```