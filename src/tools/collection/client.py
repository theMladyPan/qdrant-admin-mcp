"""Helper to get Qdrant client instance"""

from qdrant_client import AsyncQdrantClient
from src.settings import settings

_client = None


async def get_qdrant_client() -> AsyncQdrantClient:
    """Get or create async Qdrant client instance"""
    global _client
    if _client is None:
        _client = AsyncQdrantClient(
            url=settings.qdrant.url,
            api_key=settings.qdrant.api_key,
        )
    return _client
