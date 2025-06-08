from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.db_url, echo=False, pool_size=10, max_overflow=20)
async_sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    """FastAPI dependency that yields an async SQLAlchemy session."""
    async with async_sessionmaker() as session:
        yield session
