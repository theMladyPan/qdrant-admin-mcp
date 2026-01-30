# Qdrant Admin MCP - Developer Documentation

## Architecture & Decisions

### Async-First Architecture
*   **Decision:** Use `AsyncQdrantClient` exclusively.
*   **Reasoning:** To ensure high performance and non-blocking I/O, especially when handling multiple concurrent requests in an MCP environment.
*   **Source:** `src/tools/collection/client.py`

### Authentication & Multi-Tenancy
*   **Decision:** Authentication via Request Headers (`x-qdrant-url`, `x-qdrant-api-key`).
*   **Reasoning:** 
    *   Enables the MCP server to be deployed as a stateless public service.
    *   Allows a single MCP instance to connect to multiple Qdrant instances based on client request.
    *   Removes sensitive credentials from server-side environment variables (`.env`).
*   **Implementation:** 
    *   `src/tools/collection/client.py` extracts headers from the `fastmcp` request context.
    *   Client instances are cached by URL to optimize connection reuse while respecting security boundaries (key change = new client).

### Tool Organization
*   **Structure:** Tools are modularized in `src/tools/` subdirectories (e.g., `collection/`, `points/`).
*   **Registration:** 
    *   `src/tools/__init__.py` acts as the central registry list `TOOLS`.
    *   `main.py` iterates over this list to register tools with the FastMCP server.
*   **Annotations:** Tool capabilities (destructive, read-only) are defined in `TOOL_ANNOTATIONS` in `main.py` to provide hints to the LLM.

### Observability
*   **Decision:** Integration with Logfire.
*   **Reasoning:** To provide distributed tracing and structured logging for monitoring tool usage and performance in production.
*   **Source:** `main.py` (configuration), `src/tools/status.py` (spans).

## Source Map

| Component | Source File | Description |
| :--- | :--- | :--- |
| **Server Entry** | `main.py` | FastMCP setup, tool registration, annotations. |
| **Configuration** | `src/settings.py` | Pydantic settings for general server config (Logfire, Env). |
| **Qdrant Client** | `src/tools/collection/client.py` | Async client factory, header extraction, connection caching. |
| **Tool Registry** | `src/tools/__init__.py` | List of all active tools. |
| **Status Tool** | `src/tools/status.py` | Health check logic. |
| **Collection Tools** | `src/tools/collection/*.py` | `list`, `create`, `delete`, `get`. |
| **Snapshot Tools** | `src/tools/collection/snapshots.py` | Snapshot management logic. |
| **Points Tools** | `src/tools/points/*.py` | `search`, `get`, `upsert`, `delete` points. |

## Development

*   **Dependency Management:** `uv` is used for package management.
*   **Linting/Formatting:** Standard Python tooling.
*   **Docker:** Multi-stage build in `Dockerfile` for optimized image size.
