import logfire
from typing import List, Optional, Any
from src.tools.collection.client import get_qdrant_client
from src.tools.points.common import get_embedding_model

async def search_points(
    collection_name: str, 
    query_text: str, 
    limit: int = 10,
    score_threshold: Optional[float] = None
) -> List[dict[str, Any]]:
    """Search for points using text query (converts text to vector)
    
    Args:
        collection_name: Name of the collection
        query_text: Text to search for
        limit: Max number of results (default 10)
        score_threshold: Minimum score threshold
        
    Returns:
        List of matching points with scores
    """
    with logfire.span("Search Qdrant points", collection_name=collection_name, query=query_text) as span:
        model = get_embedding_model()
        # fastembed returns a generator
        embeddings = list(model.embed([query_text]))
        vector = embeddings[0]
        
        client = await get_qdrant_client()
        results = await client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True
        )
        
        serialized_results = []
        for point in results:
            serialized_results.append({
                "id": point.id,
                "score": point.score,
                "payload": point.payload,
                "version": point.version
            })
            
        span.set_attribute("results_count", len(serialized_results))
        return serialized_results
