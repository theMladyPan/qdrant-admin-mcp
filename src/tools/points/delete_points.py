from typing import Any, List, Union

import logfire
from qdrant_client.http.models import PointIdsList

from src.tools.collection.client import get_qdrant_client


async def delete_points(collection_name: str, ids: List[Union[int, str]]) -> dict[str, Any]:
    """Delete specific points by their IDs

    Args:
        collection_name: Name of the collection
        ids: List of point IDs to delete

    Returns:
        Operation status
    """
    with logfire.span("Delete Qdrant points", collection_name=collection_name, point_ids=ids) as span:
        client = await get_qdrant_client()
        result = await client.delete(collection_name=collection_name, points_selector=PointIdsList(points=ids))

        return {"operation_id": result.operation_id, "status": result.status.value}
