"""Create a new collection in Qdrant"""

from typing import Annotated, Literal

import logfire
from pydantic import Field
from qdrant_client import models

from src.tools.collection.client import get_qdrant_client


async def create_collection(
    name: Annotated[str, Field(description="Name of the collection to create")],
    vector_size: Annotated[int, Field(description="Size of the vector (dimensionality)", ge=1)],
    distance: Annotated[
        Literal["Cosine", "Euclid", "Dot", "Manhattan"],
        Field(description="Distance metric to use for similarity search"),
    ] = "Cosine",
) -> str:
    """Create a new collection in Qdrant with specified vector configuration.

    Before using this tool, suggest 3 possible vector sizes and appropriate embedding models for the user's use case,
    then let user decide on the vector size.

    Args:
        name: Name of the collection to create
        vector_size: Size/dimensionality of vectors (must be >= 1)
        distance: Distance metric (Cosine, Euclid, Dot, or Manhattan). Default: Cosine

    Returns:
        Success message with collection details
    """
    with logfire.span("Create Qdrant collection") as span:
        client = await get_qdrant_client()

        # Map string distance to Qdrant Distance enum
        distance_map = {
            "Cosine": models.Distance.COSINE,
            "Euclid": models.Distance.EUCLID,
            "Dot": models.Distance.DOT,
            "Manhattan": models.Distance.MANHATTAN,
        }

        await client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(size=vector_size, distance=distance_map[distance]),
        )

        span.set_attribute("collection_name", name)
        span.set_attribute("vector_size", vector_size)
        span.set_attribute("distance_metric", distance)

        return f"Collection '{name}' created successfully with vector size {vector_size} and {distance} distance metric"
