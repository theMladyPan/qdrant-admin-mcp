import logfire
from src.tools.collection.client import get_qdrant_client


async def get_collection(name: str) -> dict:
    """Get detailed information about a collection
    
    Args:
        name: Name of the collection
    
    Returns:
        Collection details including vector configuration, points count, and status
    """
    with logfire.span("Get Qdrant collection info", collection_name=name) as span:
        client = await get_qdrant_client()
        collection_info = await client.get_collection(collection_name=name)
        
        vectors_config = collection_info.config.params.vectors
        
        result = {
            "name": name,
            "status": collection_info.status.value,
            "vectors_count": collection_info.points_count,
            "indexed_vectors_count": collection_info.indexed_vectors_count,
            "segments_count": collection_info.segments_count,
        }
        
        if hasattr(vectors_config, "size"):
            result["vector_size"] = vectors_config.size
            result["distance"] = vectors_config.distance.value
        else:
            # Handle named vectors
            result["vectors_config"] = str(vectors_config)

        span.set_attributes(result)
        return result
