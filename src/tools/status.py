"""Status tool for checking Qdrant availability and latency"""

import time
from typing import Any

import logfire

from src.tools.collection.client import get_qdrant_client


async def status() -> dict[str, Any]:
    """Check Qdrant availability and measure latency

    Always use this tool at the beginning of the session to verify that the Qdrant instance is reachable and responsive.

    Returns:
        Dictionary with status information including:
        - status: "healthy" or "unhealthy"
        - qdrant_available: boolean
        - latency_ms: response time in milliseconds
        - collections_count: number of collections (if available)
        - error: error message if unhealthy
    """
    with logfire.span("Health check") as span:
        status_info = {
            "status": "unhealthy",
            "qdrant_available": False,
            "latency_ms": None,
            "collections_count": None,
            "error": None,
        }

        try:
            client = await get_qdrant_client()

            # Measure latency
            start_time = time.perf_counter()
            collections = await client.get_collections()
            end_time = time.perf_counter()

            latency_ms = (end_time - start_time) * 1000

            status_info.update(
                {
                    "status": "healthy",
                    "qdrant_available": True,
                    "latency_ms": round(latency_ms, 2),
                    "collections_count": len(collections.collections),
                }
            )

            span.set_attribute("status", "healthy")
            span.set_attribute("latency_ms", status_info["latency_ms"])
            span.set_attribute("collections_count", status_info["collections_count"])

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            status_info["error"] = error_msg

            span.set_attribute("status", "unhealthy")
            span.set_attribute("error", error_msg)
            logfire.error("Health check failed", error=error_msg, _exc_info=True)

        return status_info
