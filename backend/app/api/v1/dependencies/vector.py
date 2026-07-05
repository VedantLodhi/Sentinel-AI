import logging
from typing import AsyncGenerator
from qdrant_client import AsyncQdrantClient
from app.core.config import settings

logger = logging.getLogger(__name__)

# Enforce no in-memory fallbacks for vector store
if settings.vector.url == ":memory:":
    raise ValueError(
        "CRITICAL: In-memory Qdrant fallback is disabled. "
        "Provide a valid vector URL under 'VECTOR__URL'."
    )

try:
    client = AsyncQdrantClient(
        url=settings.vector.url, api_key=settings.vector.api_key, timeout=5
    )
    logger.info("Qdrant AsyncClient initialized.")
except Exception as e:
    logger.critical(f"Failed to create Qdrant client: {e}")
    raise e


async def get_vector_store() -> AsyncGenerator[AsyncQdrantClient, None]:
    """Dependency provider yielding the active Qdrant vector client connection."""
    yield client
