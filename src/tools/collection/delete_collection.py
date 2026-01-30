"""Delete a collection from Qdrant"""
from typing import Annotated
import logfire
from pydantic import Field
from src.tools.collection.client import get_qdrant_client


async def delete_collection(
    name: Annotated[str, Field(description="Name of the collection to delete")],
    confirm: Annotated[
        bool,
        Field(description="Confirmation flag - must be set to true to proceed with deletion")
    ] = False,
) -> str:
    """Delete a collection from Qdrant (DESTRUCTIVE OPERATION - requires confirmation)
    
    This operation permanently deletes the collection and all its data.
    The confirm parameter must be explicitly set to true.
    
    Args:
        name: Name of the collection to delete
        confirm: Must be true to confirm deletion
    
    Returns:
        Success message if deleted, or error if not confirmed
    """
    if not confirm:
        return (
            f"Deletion of collection '{name}' not confirmed. "
            "Set confirm=true to proceed with this destructive operation."
        )
    
    client = await get_qdrant_client()
    logfire.warn("Deleting collection {name}", name=name)
    
    await client.delete_collection(collection_name=name)
    
    logfire.info("Collection {name} deleted successfully", name=name)
    return f"Collection '{name}' has been permanently deleted"
