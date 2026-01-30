# Qdrant Admin MCP

FastMCP server for Qdrant administration.

## Structure

```
.
├── main.py                 # Main FastMCP server entry point
├── src/
│   ├── settings.py        # Pydantic settings for environment configuration
│   └── tools/             # All MCP tools
│       ├── __init__.py    # Tool registry (TOOLS list)
│       └── greet.py       # Example tool
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

1. Create a new file in `src/tools/` with your tool function
2. Add the tool to the `TOOLS` list in `src/tools/__init__.py`
3. The tool will be automatically registered with the MCP server

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
```

## Configuration

The server uses `pydantic-settings` to manage environment variables. See `src/settings.py` for available options:

- `LOGFIRE_TOKEN` - Optional Logfire token for observability
- `ENVIRONMENT` - Environment name (default: "dev")
- `PROJECT` - Project name (default: "qdrant-admin-mcp")
- `QDRANT_URL` - Qdrant server URL (default: "http://localhost:6333")
- `QDRANT_API_KEY` - Optional Qdrant API key

## Tools

### greet
Greets a person by name.

**Args:**
- `name` (str): The name of the person to greet

**Returns:**
- A greeting message
