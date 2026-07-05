import logging
from typing import AsyncGenerator
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# Check settings cache URL
if not settings.cache.url:
    raise ValueError(
        "CRITICAL: Redis cache URL is not configured. Provide 'CACHE__URL'."
    )

# Create a shared connection pool
try:
    client = Redis.from_url(
        settings.cache.url, socket_timeout=settings.cache.timeout, decode_responses=True
    )
    logger.info("Redis cache pool initialized.")
except Exception as e:
    logger.critical(f"Failed to create Redis connection: {e}")
    raise e


async def get_cache() -> AsyncGenerator[Redis, None]:
    """Dependency provider yielding the shared active Redis client connection."""
    yield client
