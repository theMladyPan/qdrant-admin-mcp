"""
All tools for the Qdrant Admin MCP server.
Add new tools to the TOOLS list for automatic registration.
"""

from src.tools.greet import greet

# List of all tools to be registered with the MCP server
TOOLS = [
    greet,
]
