"""Delete a collection from Qdrant"""

from typing import Annotated

import logfire
from pydantic import Field

from src.tools.collection.client import get_qdrant_client


async def delete_collection(
    name: Annotated[str, Field(description="Name of the collection to delete")],
    confirm: Annotated[
        bool, Field(description="Confirmation flag - must be set to true to proceed with deletion")
    ] = False,
) -> str:
    """Delete a collection from Qdrant (DESTRUCTIVE OPERATION - requires confirmation)

    **Important**: ALWAYS ask user for verbal confirmation with all details before calling this tool, even if user
    specifically requested deletion, double check, e.g. are you sure to delete <name>?

    This operation permanently deletes the collection and all its data.
    The confirm parameter must be explicitly set to true.

    Args:
        name: Name of the collection to delete
        confirm: Must be true to confirm deletion

    Returns:
        Success message if deleted, or error if not confirmed
    """
    with logfire.span("Delete Qdrant collection", _level="warn") as span:
        if not confirm:
            span.set_attribute("confirmed", False)
            span.set_attribute("collection_name", name)
            logfire.warn("Collection deletion not confirmed", collection_name=name)
            return (
                f"Deletion of collection '{name}' not confirmed. "
                "Set confirm=true to proceed with this destructive operation."
            )

        client = await get_qdrant_client()

        await client.delete_collection(collection_name=name)

        span.set_attribute("confirmed", True)
        span.set_attribute("collection_name", name)
        span.set_attribute("operation", "deleted")

        return f"Collection '{name}' has been permanently deleted"
