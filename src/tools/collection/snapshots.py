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
    client = await get_qdrant_client()
    logfire.info("Creating snapshot for collection {collection}", collection=collection_name)
    
    result = await client.create_snapshot(collection_name=collection_name)
    snapshot_name = result.name
    
    logfire.info(
        "Snapshot created for collection {collection}: {snapshot}",
        collection=collection_name,
        snapshot=snapshot_name
    )
    return f"Snapshot '{snapshot_name}' created successfully for collection '{collection_name}'"


async def list_snapshots(
    collection_name: Annotated[str, Field(description="Name of the collection")],
) -> list[str]:
    """List all snapshots for a collection
    
    Args:
        collection_name: Name of the collection
    
    Returns:
        List of snapshot names
    """
    client = await get_qdrant_client()
    logfire.info("Listing snapshots for collection {collection}", collection=collection_name)
    
    snapshots = await client.list_snapshots(collection_name=collection_name)
    snapshot_names = [snap.name for snap in snapshots]
    
    logfire.info(
        "Found {count} snapshots for collection {collection}",
        count=len(snapshot_names),
        collection=collection_name
    )
    return snapshot_names


async def delete_snapshot(
    collection_name: Annotated[str, Field(description="Name of the collection")],
    snapshot_name: Annotated[str, Field(description="Name of the snapshot to delete")],
    confirm: Annotated[
        bool,
        Field(description="Confirmation flag - must be set to true to proceed with deletion")
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
    if not confirm:
        return (
            f"Deletion of snapshot '{snapshot_name}' not confirmed. "
            "Set confirm=true to proceed with this destructive operation."
        )
    
    client = await get_qdrant_client()
    logfire.warn(
        "Deleting snapshot {snapshot} from collection {collection}",
        snapshot=snapshot_name,
        collection=collection_name
    )
    
    await client.delete_snapshot(
        collection_name=collection_name,
        snapshot_name=snapshot_name
    )
    
    logfire.info(
        "Snapshot {snapshot} deleted from collection {collection}",
        snapshot=snapshot_name,
        collection=collection_name
    )
    return f"Snapshot '{snapshot_name}' deleted successfully from collection '{collection_name}'"


async def recover_from_snapshot(
    collection_name: Annotated[str, Field(description="Name of the collection to recover")],
    snapshot_name: Annotated[str, Field(description="Name of the snapshot to restore from")],
    confirm: Annotated[
        bool,
        Field(description="Confirmation flag - must be set to true to proceed with recovery")
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
    if not confirm:
        return (
            f"Recovery of collection '{collection_name}' from snapshot '{snapshot_name}' not confirmed. "
            "Set confirm=true to proceed with this destructive operation."
        )
    
    client = await get_qdrant_client()
    logfire.warn(
        "Recovering collection {collection} from snapshot {snapshot}",
        collection=collection_name,
        snapshot=snapshot_name
    )
    
    await client.recover_snapshot(
        collection_name=collection_name,
        snapshot_name=snapshot_name
    )
    
    logfire.info(
        "Collection {collection} recovered from snapshot {snapshot}",
        collection=collection_name,
        snapshot=snapshot_name
    )
    return f"Collection '{collection_name}' successfully recovered from snapshot '{snapshot_name}'"
