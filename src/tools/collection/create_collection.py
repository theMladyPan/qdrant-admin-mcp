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
        Field(description="Distance metric to use for similarity search")
    ] = "Cosine",
) -> str:
    """Create a new collection in Qdrant with specified vector configuration
    
    Args:
        name: Name of the collection to create
        vector_size: Size/dimensionality of vectors (must be >= 1)
        distance: Distance metric (Cosine, Euclid, Dot, or Manhattan). Default: Cosine
    
    Returns:
        Success message with collection details
    """
    client = await get_qdrant_client()
    logfire.info(
        "Creating collection {name} with size {size} and {distance} distance",
        name=name,
        size=vector_size,
        distance=distance
    )
    
    # Map string distance to Qdrant Distance enum
    distance_map = {
        "Cosine": models.Distance.COSINE,
        "Euclid": models.Distance.EUCLID,
        "Dot": models.Distance.DOT,
        "Manhattan": models.Distance.MANHATTAN,
    }
    
    await client.create_collection(
        collection_name=name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=distance_map[distance]
        ),
    )
    
    logfire.info("Collection {name} created successfully", name=name)
    return f"Collection '{name}' created successfully with vector size {vector_size} and {distance} distance metric"
