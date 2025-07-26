import os
from logging import getLogger
from typing import AsyncGenerator, Generator

import pytest
import sqlalchemy
from database import user_table
from httpx import ASGITransport, AsyncClient

from fastapi.testclient import TestClient
from social.main import app

os.environ["ENV_STATE"] = "test"
from fastapi import HTTPException, status
from social.database import database

logger = getLogger(__name__)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True, scope='session')
async def db() -> AsyncGenerator:
    logger.debug("Setting up database connection for tests")
    await database.connect()
    logger.debug("Database connection established")
    yield
    await database.disconnect()
    logger.debug("Closed database connection for tests")


@pytest.fixture
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8443"
    ) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = sqlalchemy.select(user_table).where(
        user_table.c.email == user_details["email"]
    )
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User not stored in database",
        )
    user_details["id"] = user.id
    return user_details


@pytest.fixture
async def logged_in_token(async_client: AsyncClient, registered_uder: dict) -> str:
    response = await async_client.post("/token", json=registered_user)
    return response.json()["access_token"]


@pytest.fixture(scope="function", autouse=True)
async def clean_database():
    """Clean database before each test"""
    tables_to_clear = ["users", "posts", "comments"] 

    for table in tables_to_clear:
        try:
            query = f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"
            await database.execute(query)
        except Exception as e:
            logger.debug(f"Could not truncate {table}: {e}")

    yield
