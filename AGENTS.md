# Qdrant Admin MCP

FastMCP server for Qdrant administration with async-first architecture.

## Features

- ✅ **Async-First**: All Qdrant operations use AsyncQdrantClient for optimal performance
- ✅ **Collection Management**: Create, list, and delete collections
- ✅ **Snapshot Management**: Create, list, delete, and restore from snapshots
- ✅ **Type Safety**: Full Pydantic validation with detailed type hints
- ✅ **MCP Annotations**: Proper hints for destructive operations
- ✅ **Confirmation Required**: All destructive operations require explicit confirmation
- ✅ **Comprehensive Logging**: All operations logged via Logfire

## Structure

```
.
├── main.py                 # Main FastMCP server entry point
├── src/
│   ├── settings.py        # Pydantic settings for environment configuration
│   └── tools/             # All MCP tools
│       ├── __init__.py    # Tool registry (TOOLS list)
│       └── collection/    # Collection management tools (async)
│           ├── client.py            # Async Qdrant client helper
│           ├── list_collections.py
│           ├── create_collection.py
│           ├── delete_collection.py
│           └── snapshots.py         # Snapshot management
├── Dockerfile             # Docker image definition
├── compose.yml            # Docker Compose configuration
├── .dockerignore          # Docker build exclusions
├── .env.example           # Example environment variables
└── pyproject.toml         # Project dependencies
```

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Run the server:
```bash
uv run python main.py
```

## Docker Compose

Run the entire stack (MCP server + Qdrant):

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

The compose setup includes:
- **qdrant**: Vector database on ports 6333 (HTTP) and 6334 (gRPC)
- **qdrant-admin-mcp**: MCP server connected to Qdrant

Qdrant data is persisted in `./qdrant` directory.

## Docker

Build and run with Docker:

```bash
# Build the image
docker build -t qdrant-admin-mcp .

# Or with a deploy key for private dependencies
docker build --secret id=GITHUB_DEPLOY_KEY,src=$HOME/.ssh/id_rsa -t qdrant-admin-mcp .

# Run the container
docker run -it --rm \
  --env-file .env \
  qdrant-admin-mcp
```

## Adding New Tools

1. Create a new file in `src/tools/` (or subdirectory) with your tool function
2. Add the tool to the `TOOLS` list in `src/tools/__init__.py`
3. Optionally add annotations in `main.py` TOOL_ANNOTATIONS dict
4. The tool will be automatically registered with the MCP server

Example:
```python
# src/tools/my_tool.py
def my_tool(arg: str) -> str:
    """Tool description
    
    Args:
        arg: Argument description
    
    Returns:
        Return value description
    """
    return f"Result: {arg}"

# src/tools/__init__.py
from src.tools.greet import greet
from src.tools.my_tool import my_tool

TOOLS = [
    greet,
    my_tool,  # Add your new tool here
]

# main.py (optional - add annotations)
TOOL_ANNOTATIONS = {
    "my_tool": {
        "title": "My Tool",
        "readOnlyHint": True,
        "openWorldHint": False,
    }
}
```

## HTTP Endpoints

The server provides HTTP endpoints in addition to MCP tools:

### GET /status

Health check endpoint that verifies Qdrant availability and measures latency.

**Response:**
```json
{
  "status": "healthy",
  "qdrant_available": true,
  "latency_ms": 7.35,
  "collections_count": 1,
  "error": null
}
```

**Fields:**
- `status` - "healthy" or "unhealthy"
- `qdrant_available` - Boolean indicating if Qdrant is reachable
- `latency_ms` - Response time in milliseconds (null if unavailable)
- `collections_count` - Number of collections (null if unavailable)
- `error` - Error message if unhealthy (null if healthy)

**Example:**
```bash
curl http://localhost:4600/status
```

## Configuration

The server uses `pydantic-settings` to manage environment variables. See `src/settings.py` for available options:

- `LOGFIRE_TOKEN` - Optional Logfire token for observability
- `ENVIRONMENT` - Environment name (default: "dev")
- `PROJECT` - Project name (default: "qdrant-admin-mcp")
- `QDRANT_URL` - Qdrant server URL (default: "http://localhost:6333")
- `QDRANT_API_KEY` - Optional Qdrant API key

## Tools

### Collection Management

#### list_collections
List all collections in the Qdrant instance.

**Returns:**
- List of collection names

**Annotations:** Read-only, external system access

---

#### create_collection
Create a new collection in Qdrant with specified vector configuration.

**Args:**
- `name` (str): Name of the collection to create
- `vector_size` (int): Size/dimensionality of vectors (must be >= 1)
- `distance` (Literal["Cosine", "Euclid", "Dot", "Manhattan"]): Distance metric. Default: "Cosine"

**Returns:**
- Success message with collection details

**Annotations:** Non-destructive write, external system access

---

#### delete_collection
Delete a collection from Qdrant (DESTRUCTIVE OPERATION - requires confirmation).

This operation permanently deletes the collection and all its data.

**Args:**
- `name` (str): Name of the collection to delete
- `confirm` (bool): Must be true to confirm deletion. Default: false

**Returns:**
- Success message if deleted, or error if not confirmed

**Annotations:** Destructive operation, external system access

---

### Snapshot Management

#### create_snapshot
Create a snapshot of a collection for backup or restoration.

**Args:**
- `collection_name` (str): Name of the collection to snapshot

**Returns:**
- Success message with snapshot name

**Annotations:** Non-destructive write, external system access

---

#### list_snapshots
List all snapshots for a collection.

**Args:**
- `collection_name` (str): Name of the collection

**Returns:**
- List of snapshot names

**Annotations:** Read-only, external system access

---

#### delete_snapshot
Delete a snapshot from a collection (DESTRUCTIVE OPERATION - requires confirmation).

This operation permanently deletes the snapshot file.

**Args:**
- `collection_name` (str): Name of the collection
- `snapshot_name` (str): Name of the snapshot to delete
- `confirm` (bool): Must be true to confirm deletion. Default: false

**Returns:**
- Success message if deleted, or error if not confirmed

**Annotations:** Destructive operation, external system access

---

#### recover_from_snapshot
Recover a collection from a snapshot (DESTRUCTIVE OPERATION - requires confirmation).

This operation will restore the collection to the state captured in the snapshot.
Any data added after the snapshot was created will be lost.

**Args:**
- `collection_name` (str): Name of the collection to recover
- `snapshot_name` (str): Name of the snapshot to restore from
- `confirm` (bool): Must be true to confirm recovery. Default: false

**Returns:**
- Success message if recovered, or error if not confirmed

**Annotations:** Destructive operation, external system access
