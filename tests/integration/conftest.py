import os

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.repos import RepController


@pytest.fixture(scope="session")
def integration_db_url():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set")
    return url


@pytest_asyncio.fixture
async def pg_rep_controller(integration_db_url):
    engine = create_async_engine(integration_db_url)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.execute(
            text("TRUNCATE TABLE user_rep_history, user_reps RESTART IDENTITY CASCADE")
        )

    try:
        yield RepController(session_factory=session_factory)
    finally:
        async with engine.begin() as connection:
            await connection.execute(
                text("TRUNCATE TABLE user_rep_history, user_reps RESTART IDENTITY CASCADE")
            )
        await engine.dispose()
