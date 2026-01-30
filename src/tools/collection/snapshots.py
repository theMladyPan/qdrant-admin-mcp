"""Manage Qdrant collection snapshots"""

from typing import Annotated
import logfire
from pydantic import Field
from src.tools.collection.client import get_qdrant_client


async def create_snapshot(
    collection_name: Annotated[str, Field(description="Name of the collection to snapshot")],
) -> str:
    """Create a snapshot of a collection

    Creates a point-in-time snapshot of the collection that can be used for backup
    or restoration purposes.

    Args:
        collection_name: Name of the collection to snapshot

    Returns:
        Success message with snapshot name
    """
    with logfire.span("Create collection snapshot") as span:
        client = await get_qdrant_client()

        result = await client.create_snapshot(collection_name=collection_name)
        snapshot_name = result.name

        span.set_attribute("collection_name", collection_name)
        span.set_attribute("snapshot_name", snapshot_name)

        return f"Snapshot '{snapshot_name}' created successfully for collection '{collection_name}'"


async def list_snapshots(
    collection_name: Annotated[str, Field(description="Name of the collection")],
) -> list[str]:
    """List all snapshots for a collection

    Args:
        collection_name: Name of the collection

    Returns:
        list of snapshot names
    """
    with logfire.span("List collection snapshots") as span:
        client = await get_qdrant_client()

        snapshots = await client.list_snapshots(collection_name=collection_name)
        snapshot_names = [snap.name for snap in snapshots]

        span.set_attribute("collection_name", collection_name)
        span.set_attribute("snapshot_count", len(snapshot_names))
        span.set_attribute("snapshots", snapshot_names)

        return snapshot_names


async def delete_snapshot(
    collection_name: Annotated[str, Field(description="Name of the collection")],
    snapshot_name: Annotated[str, Field(description="Name of the snapshot to delete")],
    confirm: Annotated[
        bool, Field(description="Confirmation flag - must be set to true to proceed with deletion")
    ] = False,
) -> str:
    """Delete a snapshot from a collection (DESTRUCTIVE OPERATION - requires confirmation)

    This operation permanently deletes the snapshot file.
    The confirm parameter must be explicitly set to true.

    Args:
        collection_name: Name of the collection
        snapshot_name: Name of the snapshot to delete
        confirm: Must be true to confirm deletion

    Returns:
        Success message if deleted, or error if not confirmed
    """
    with logfire.span("Delete collection snapshot", _level="warn") as span:
        if not confirm:
            span.set_attribute("confirmed", False)
            span.set_attribute("collection_name", collection_name)
            span.set_attribute("snapshot_name", snapshot_name)
            logfire.warn(
                "Snapshot deletion not confirmed", collection_name=collection_name, snapshot_name=snapshot_name
            )
            return (
                f"Deletion of snapshot '{snapshot_name}' not confirmed. "
                "Set confirm=true to proceed with this destructive operation."
            )

        client = await get_qdrant_client()

        await client.delete_snapshot(collection_name=collection_name, snapshot_name=snapshot_name)

        span.set_attribute("confirmed", True)
        span.set_attribute("collection_name", collection_name)
        span.set_attribute("snapshot_name", snapshot_name)
        span.set_attribute("operation", "deleted")

        return f"Snapshot '{snapshot_name}' deleted successfully from collection '{collection_name}'"


async def recover_from_snapshot(
    collection_name: Annotated[str, Field(description="Name of the collection to recover")],
    snapshot_name: Annotated[str, Field(description="Name of the snapshot to restore from")],
    confirm: Annotated[
        bool, Field(description="Confirmation flag - must be set to true to proceed with recovery")
    ] = False,
) -> str:
    """Recover a collection from a snapshot (DESTRUCTIVE OPERATION - requires confirmation)

    This operation will restore the collection to the state captured in the snapshot.
    Any data added after the snapshot was created will be lost.
    The confirm parameter must be explicitly set to true.

    Args:
        collection_name: Name of the collection to recover
        snapshot_name: Name of the snapshot to restore from
        confirm: Must be true to confirm recovery

    Returns:
        Success message if recovered, or error if not confirmed
    """
    with logfire.span("Recover collection from snapshot", _level="warn") as span:
        if not confirm:
            span.set_attribute("confirmed", False)
            span.set_attribute("collection_name", collection_name)
            span.set_attribute("snapshot_name", snapshot_name)
            logfire.warn(
                "Collection recovery not confirmed", collection_name=collection_name, snapshot_name=snapshot_name
            )
            return (
                f"Recovery of collection '{collection_name}' from snapshot '{snapshot_name}' not confirmed. "
                "Set confirm=true to proceed with this destructive operation."
            )

        client = await get_qdrant_client()

        await client.recover_snapshot(collection_name=collection_name, snapshot_name=snapshot_name)

        span.set_attribute("confirmed", True)
        span.set_attribute("collection_name", collection_name)
        span.set_attribute("snapshot_name", snapshot_name)
        span.set_attribute("operation", "recovered")

        return f"Collection '{collection_name}' successfully recovered from snapshot '{snapshot_name}'"
