from typing import Any, List, Optional

import logfire

from src.tools.collection.client import get_qdrant_client
from src.tools.points.common import get_embedding_model


async def search_points(
    collection_name: str,
    query_text: str,
    limit: int = 10,
    score_threshold: Optional[float] = None,
    embedding_model: str = "BAAI/bge-small-en-v1.5",
) -> List[dict[str, Any]]:
    """Search for points using text query (converts text to vector)

    Args:
        collection_name: Name of the collection
        query_text: Text to search for
        limit: Max number of results (default 10)
        score_threshold: Minimum score threshold
        embedding_model: Fastembed model name (default: BAAI/bge-small-en-v1.5)

    Returns:
        List of matching points with scores
    """
    with logfire.span("Search Qdrant points", collection_name=collection_name, query=query_text) as span:
        with logfire.span("Generate embedding for query text") as embed_span:
            model = get_embedding_model(embedding_model)
            # fastembed returns a generator
            embeddings = list(model.embed([query_text]))
            vector = embeddings[0]

        with logfire.span("Query Qdrant collection") as query_span:
            client = await get_qdrant_client()
            response = await client.query_points(
                collection_name=collection_name,
                query=vector.tolist(),
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True,
            )

        serialized_results = []
        for point in response.points:
            serialized_results.append(
                {"id": point.id, "score": point.score, "payload": point.payload, "version": point.version}
            )

        span.set_attribute("results_count", len(serialized_results))
        return serialized_results
