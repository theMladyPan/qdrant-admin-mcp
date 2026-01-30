"""List all collections in Qdrant"""
import logfire
from src.tools.collection.client import get_qdrant_client


async def list_collections() -> list[str]:
    """List all collections in the Qdrant instance
    
    Returns:
        List of collection names
    """
    client = await get_qdrant_client()
    logfire.info("Listing Qdrant collections")
    
    collections = await client.get_collections()
    collection_names = [col.name for col in collections.collections]
    
    logfire.info("Found {count} collections", count=len(collection_names))
    return collection_names
