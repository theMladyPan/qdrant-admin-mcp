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

## Tools

### greet
Greets a person by name.

**Args:**
- `name` (str): The name of the person to greet

**Returns:**
- A greeting message
