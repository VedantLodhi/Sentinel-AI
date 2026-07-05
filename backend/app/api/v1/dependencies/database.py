from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.database import async_session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide an asynchronous database session dependency.

    Ensures rollback on request exception and clean session closing.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
