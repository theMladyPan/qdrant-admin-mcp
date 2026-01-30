"""
All tools for the Qdrant Admin MCP server.
Add new tools to the TOOLS list for automatic registration.
"""

from src.tools.collection import (
    list_collections,
    get_collection,
    create_collection,
    delete_collection,
    create_snapshot,
    list_snapshots,
    delete_snapshot,
    recover_from_snapshot,
)
from src.tools.points import (
    get_points,
    delete_points,
    search_points,
    upsert_points,
)

# List of all tools to be registered with the MCP server
TOOLS = [
    # Collection management
    list_collections,
    get_collection,
    create_collection,
    delete_collection,
    # Snapshot management
    create_snapshot,
    list_snapshots,
    delete_snapshot,
    recover_from_snapshot,
    # Points management
    get_points,
    delete_points,
    search_points,
    upsert_points,
]
