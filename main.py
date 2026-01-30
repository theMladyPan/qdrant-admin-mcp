import tomllib

import logfire
from fastmcp import FastMCP

from src.settings import settings
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
    version=__version__,
)

mcp = FastMCP(
    "Qdrant Admin MCP",
    version=__version__,
    instructions="""
This is a FastMCP server for Qdrant administration.
It provides tools to interact with Qdrant vector database.
    """.strip(),
)

# Register all tools automatically
for tool in TOOLS:
    mcp.tool()(tool)


if __name__ == "__main__":
    mcp.run()
