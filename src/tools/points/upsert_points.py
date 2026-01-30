from typing import Any

import logfire
from qdrant_client.http.models import PointStruct

from src.tools.collection.client import get_qdrant_client
from src.tools.points.common import get_embedding_model


async def upsert_points(
    collection_name: str, points: list[dict[str, Any]], embedding_model: str = "BAAI/bge-small-en-v1.5"
) -> dict[str, Any]:
    """Upsert points with automatic text embedding generation

    before upserting, query the collection for vector size, if the dimensionality is likely to differ from the
    default embedding model, provide user a few examples which model might be more suitable for embedding and let
    the user choose the embedding model to use.

    Args:
        collection_name: Name of the collection
        points: List of dicts, each containing:
            - id: Point ID (int or str)
            - text: Text to embed (optional if vector provided)
            - payload: dict of metadata (optional)
            - vector: list[float] (optional, overrides text embedding)
        embedding_model: Fastembed model name (default: BAAI/bge-small-en-v1.5)

    Returns:
        Operation status
    """
    with logfire.span("Upsert Qdrant points", collection_name=collection_name, count=len(points)) as span:
        model = get_embedding_model(embedding_model)

        points_to_upsert = []

        # separate points that need embedding
        texts_to_embed = []
        indices_to_embed = []

        for i, point in enumerate(points):
            if "vector" not in point and "text" in point:
                texts_to_embed.append(point["text"])
                indices_to_embed.append(i)

        if texts_to_embed:
            embeddings = list(model.embed(texts_to_embed))
            for i, embedding in zip(indices_to_embed, embeddings):
                points[i]["vector"] = embedding.tolist()

        for point in points:
            if "vector" not in point:
                # Skip points without vector
                continue

            payload = point.get("payload", {})
            if "text" in point:
                payload["text"] = point["text"]

            points_to_upsert.append(PointStruct(id=point["id"], vector=point["vector"], payload=payload))

        if not points_to_upsert:
            return {"status": "no_points_to_upsert"}

        client = await get_qdrant_client()
        result = await client.upsert(collection_name=collection_name, points=points_to_upsert)

        return {"operation_id": result.operation_id, "status": result.status.value}
