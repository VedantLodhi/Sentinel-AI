import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from qdrant_client import AsyncQdrantClient
from redis.asyncio import Redis
from sqlalchemy.sql import text

from app.core.config import settings
from app.infrastructure.database.database import async_session_maker, engine
from app.core.exceptions import register_exception_handlers
from app.core.telemetry import setup_logging, setup_telemetry
from app.middleware.correlation import CorrelationIdMiddleware
from app.api.v1.router import api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Controls server lifecycle. Validates database, cache, and vector store at startup."""
    logger.info("Sentinel AI: Verifying system connection readiness...")

    # 1. Validate PostgreSQL connection
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        logger.info("System Check: PostgreSQL database connection verified.")
    except Exception as e:
        logger.critical(f"System Check FAILURE: PostgreSQL is unreachable: {e}")
        raise RuntimeError(f"Database readiness validation failed: {e}") from e

    # 2. Validate Redis connection
    if not settings.cache.url:
        logger.critical("System Check FAILURE: Redis URL is not configured.")
        raise RuntimeError("Redis URL is not configured in settings.")
    try:
        redis_client = Redis.from_url(settings.cache.url, socket_timeout=2.0)
        await redis_client.ping()
        await redis_client.close()
        logger.info("System Check: Redis cache connection verified.")
    except Exception as e:
        logger.critical(f"System Check FAILURE: Redis is unreachable: {e}")
        raise RuntimeError(f"Redis readiness validation failed: {e}") from e

    # 3. Validate Qdrant connection
    if settings.vector.url == ":memory:":
        logger.critical(
            "System Check FAILURE: Qdrant in-memory mode is prohibited in this profile."
        )
        raise RuntimeError("Vector database URL cannot be ':memory:'.")
    try:
        qdrant_client = AsyncQdrantClient(
            url=settings.vector.url, api_key=settings.vector.api_key, timeout=2
        )
        await qdrant_client.get_collections()
        await qdrant_client.close()
        logger.info("System Check: Qdrant vector database connection verified.")
    except Exception as e:
        logger.critical(f"System Check FAILURE: Qdrant is unreachable: {e}")
        raise RuntimeError(f"Vector store readiness validation failed: {e}") from e

    logger.info("Sentinel AI Backend started successfully.")

    yield

    logger.info("Sentinel AI: Flushing background resources on shutdown...")
    await engine.dispose()
    logger.info("PostgreSQL connection pools successfully disposed.")


# Initialize logging structure before app creation
setup_logging()

# Setup FastAPI App
app = FastAPI(
    title=settings.project_name,
    description="The AI Incident Response Engineer for Modern Cloud Applications",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# Register Correlation Tracing ID Middleware
app.add_middleware(CorrelationIdMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Adjust origin configurations for production deployment profiles
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Map exceptions filters
register_exception_handlers(app)

# OpenTelemetry configuration hooks
setup_telemetry(app)

# Include core router
app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect roots requests to API interactive Swagger docs."""
    return RedirectResponse(url="/docs")
