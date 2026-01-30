"""List all collections in Qdrant"""
import logfire
from src.tools.collection.client import get_qdrant_client


async def list_collections() -> list[str]:
    """List all collections in the Qdrant instance
    
    Returns:
        List of collection names
    """
    with logfire.span("List Qdrant collections") as span:
        client = await get_qdrant_client()
        
        collections = await client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        span.set_attribute("collection_count", len(collection_names))
        span.set_attribute("collections", collection_names)
        
        return collection_names
