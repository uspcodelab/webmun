from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings


class RepositoryError(Exception):
    """Base exception for all repository issues"""

    pass


def create_db(
    settings: Settings,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    database_url = settings.DATABASE_URL.get_secret_value()
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"prepared_statement_cache_size": 0},
    )

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine, session_factory


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """Dependency Injection for DB session. Uses app state for storing db setup"""
    session_factory = request.app.state.db_session_factory

    async with session_factory() as session:
        yield session
