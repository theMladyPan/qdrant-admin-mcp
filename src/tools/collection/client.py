"""Helper to get Qdrant client instance"""

from fastmcp.server.dependencies import get_http_request
from qdrant_client import AsyncQdrantClient

from src.settings import settings

# Cache of (client, api_key) keyed by URL
# strict requirement: use URL as cache key
_clients: dict[str, tuple[AsyncQdrantClient, str | None]] = {}


async def get_qdrant_client() -> AsyncQdrantClient:
    """Get or create async Qdrant client instance based on request headers"""
    # Default values from settings
    url = settings.qdrant.url
    api_key = settings.qdrant.api_key

    try:
        # Try to extract from request context
        request = get_http_request()
        if request:
            # Check headers (standardize on lowercase)
            if "x-qdrant-url" in request.headers:
                url = request.headers["x-qdrant-url"]

            if "x-qdrant-api-key" in request.headers:
                api_key = request.headers["x-qdrant-api-key"]
    except Exception:
        # Fallback for non-request context (e.g. startup checks)
        pass

    # Logic: Use URL as cache key
    # If the API key for that URL changes, we must recreate the client
    global _clients

    if url in _clients:
        client, cached_key = _clients[url]
        if cached_key != api_key:
            # API Key changed for this URL, recreate client
            await client.close()
            client = AsyncQdrantClient(url=url, api_key=api_key)
            _clients[url] = (client, api_key)
    else:
        client = AsyncQdrantClient(url=url, api_key=api_key)
        _clients[url] = (client, api_key)

    return _clients[url][0]
