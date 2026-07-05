import asyncio
import logging
import time
from typing import Any, Dict
import httpx
from fastapi import APIRouter, Depends, Response, status
from redis.asyncio import Redis
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.api.v1.dependencies.database import get_db
from app.api.v1.dependencies.cache import get_cache
from app.api.v1.dependencies.vector import get_vector_store
from app.api.v1.dependencies.llm import get_llm
from app.infrastructure.llm.router import LLMRouter
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """Liveness check to verify the API process is alive."""
    return {"status": "live", "message": "I'm alive."}


async def check_database(db: AsyncSession) -> Dict[str, Any]:
    start_time = time.perf_counter()
    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {"status": "healthy", "latency_ms": round(latency_ms, 2)}
    except Exception as e:
        logger.error(f"Readiness check: Database failure: {e}")
        return {"status": "unhealthy", "error": str(e)}


async def check_redis(cache: Redis) -> Dict[str, Any]:
    start_time = time.perf_counter()
    try:
        await cache.ping()
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {"status": "healthy", "latency_ms": round(latency_ms, 2)}
    except Exception as e:
        logger.error(f"Readiness check: Redis failure: {e}")
        return {"status": "unhealthy", "error": str(e)}


async def check_qdrant(vector: AsyncQdrantClient) -> Dict[str, Any]:
    start_time = time.perf_counter()
    try:
        await vector.get_collections()
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {"status": "healthy", "latency_ms": round(latency_ms, 2)}
    except Exception as e:
        logger.error(f"Readiness check: Qdrant failure: {e}")
        return {"status": "unhealthy", "error": str(e)}


async def check_ollama(llm: LLMRouter) -> Dict[str, Any]:
    start_time = time.perf_counter()
    try:
        is_ready = await llm.provider.check_ready()
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {
            "status": "healthy" if is_ready else "unhealthy",
            "latency_ms": round(latency_ms, 2),
        }
    except Exception as e:
        logger.error(f"Readiness check: LLM connection failure: {e}")
        return {"status": "unhealthy", "error": str(e)}


async def check_minio() -> Dict[str, Any]:
    start_time = time.perf_counter()
    # Perform HTTP probe on configured MinIO storage endpoint
    url = f"http://{settings.storage.endpoint}/minio/health/live"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url)
            latency_ms = (time.perf_counter() - start_time) * 1000
            if response.status_code == 200:
                return {"status": "healthy", "latency_ms": round(latency_ms, 2)}
            return {
                "status": "unhealthy",
                "error": f"MinIO returned status code {response.status_code}",
            }
    except Exception as e:
        logger.error(f"Readiness check: MinIO connection failure: {e}")
        return {"status": "unhealthy", "error": str(e)}


@router.get("/ready")
async def readiness_check(
    response: Response,
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache),
    vector: AsyncQdrantClient = Depends(get_vector_store),
    llm: LLMRouter = Depends(get_llm),
) -> Dict[str, Any]:
    """Readiness check to verify that all upstream dependencies are healthy."""
    start_time = time.perf_counter()

    # Query all services concurrently
    db_check, redis_check, qdrant_check, ollama_check, minio_check = (
        await asyncio.gather(
            check_database(db),
            check_redis(cache),
            check_qdrant(vector),
            check_ollama(llm),
            check_minio(),
        )
    )

    total_latency_ms = (time.perf_counter() - start_time) * 1000

    # Audit statuses
    is_healthy = (
        db_check["status"] == "healthy"
        and redis_check["status"] == "healthy"
        and qdrant_check["status"] == "healthy"
        and ollama_check["status"] == "healthy"
        and minio_check["status"] == "healthy"
    )

    overall_status = "ready" if is_healthy else "unready"

    if not is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "total_latency_ms": round(total_latency_ms, 2),
        "services": {
            "database": db_check,
            "redis": redis_check,
            "qdrant": qdrant_check,
            "ollama": ollama_check,
            "minio": minio_check,
        },
    }
