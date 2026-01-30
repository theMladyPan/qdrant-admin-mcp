import logfire
from typing import List, Union, Any
from src.tools.collection.client import get_qdrant_client

async def get_points(collection_name: str, ids: List[Union[int, str]]) -> List[dict[str, Any]]:
    """Retrieve specific points by their IDs
    
    Args:
        collection_name: Name of the collection
        ids: List of point IDs (integers or UUID strings)
    
    Returns:
        List of points with their payload and vector info
    """
    with logfire.span("Get Qdrant points", collection_name=collection_name, point_ids=ids) as span:
        client = await get_qdrant_client()
        points = await client.retrieve(
            collection_name=collection_name,
            ids=ids,
            with_payload=True,
            with_vectors=True
        )
        
        results = []
        for point in points:
            results.append({
                "id": point.id,
                "payload": point.payload,
                "vector": point.vector,
            })
            
        span.set_attribute("found_count", len(results))
        return results
