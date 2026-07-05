import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

logger = logging.getLogger(__name__)

# Validate that database URL is present in settings
if not settings.db.url:
    raise ValueError(
        "CRITICAL: Database URL is not configured. "
        "Provide a valid PostgreSQL connection string under 'DB__URL'."
    )

try:
    # Setup PostgreSQL engine using asyncpg driver
    engine = create_async_engine(
        settings.db.url,
        echo=False,
        future=True,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_timeout=settings.db.pool_timeout,
        pool_recycle=settings.db.pool_recycle,
    )
    logger.info("SQLAlchemy PostgreSQL engine initialized.")
except Exception as e:
    logger.critical(f"Failed to initialize PostgreSQL engine: {e}")
    raise e

# Setup session factory for dependency injections
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for all relational database models in Sentinel AI."""

    pass
