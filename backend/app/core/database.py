from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import get_settings

settings = get_settings()

# Gerado pelo Gemini
# Para o Supavisor em modo Transaction, desativamos o prepared statement cache do asyncpg
# passando o parâmetro 'prepared_statement_cache_size=0' na query string ou via connect_args.
engine = create_async_engine(
    settings.DATABASE_URL.get_secret_value(),
    pool_pre_ping=True,
    connect_args={
        "prepared_statement_cache_size": 0  # Crucial para o Supavisor não quebrar!
    }
)

async_sessionmaker_factory = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False
)

Base = declarative_base()

# Dependência assíncrona pythônica para o Depends do FastAPI
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker_factory() as session:
        yield session

