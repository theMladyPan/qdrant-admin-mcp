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
        
        result = {
            "name": name,
            "status": collection_info.status.value,
            "vectors_count": collection_info.points_count,
            "indexed_vectors_count": collection_info.indexed_vectors_count,
            "vector_size": collection_info.config.params.vectors.size,
            "distance": collection_info.config.params.vectors.distance.value,
            "segments_count": collection_info.segments_count,
        }
        
        span.set_attributes(result)
        return result
