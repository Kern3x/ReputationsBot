from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core import settings
from app.db.base import Base


engine = create_async_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)
SessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_database() -> None:
    import app.models  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def dispose_database() -> None:
    await engine.dispose()
