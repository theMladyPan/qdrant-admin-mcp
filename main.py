import tomllib

import logfire
from fastmcp import FastMCP

from src.settings import settings
from src.status import get_status
from src.tools import TOOLS

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

__version__ = data["project"]["version"]

logfire.configure(
    token=settings.logfire_token,
    send_to_logfire="if-token-present",
    distributed_tracing=False,
    environment=settings.environment,
    service_name=settings.project,
    service_version=__version__,
)

mcp = FastMCP(
    "Qdrant Admin MCP",
    version=__version__,
    instructions="""
This is a FastMCP server for Qdrant administration.
It provides tools to interact with Qdrant vector database.
    """.strip(),
)

# Map of tool names to their annotations
TOOL_ANNOTATIONS = {
    "list_collections": {
        "title": "List Collections",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
    "create_collection": {
        "title": "Create Collection",
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    },
    "delete_collection": {
        "title": "Delete Collection",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    },
    "list_snapshots": {
        "title": "List Snapshots",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
    "create_snapshot": {
        "title": "Create Snapshot",
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    },
    "delete_snapshot": {
        "title": "Delete Snapshot",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    },
    "recover_from_snapshot": {
        "title": "Recover from Snapshot",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    },
    "get_points": {
        "title": "Get Points",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
    "delete_points": {
        "title": "Delete Points",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    },
    "search_points": {
        "title": "Search Points",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
    "upsert_points": {
        "title": "Upsert Points",
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    },
}

# Register all tools automatically with annotations
for tool in TOOLS:
    tool_name = tool.__name__
    annotations = TOOL_ANNOTATIONS.get(tool_name, {})
    mcp.tool(annotations=annotations)(tool)


# Add custom HTTP routes using FastMCP's custom_route decorator
@mcp.custom_route("/status", methods=["GET"])
async def status_endpoint(request):
    """Check Qdrant availability and latency"""
    from starlette.responses import JSONResponse

    status_data = await get_status()
    return JSONResponse(status_data)


if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8080)
