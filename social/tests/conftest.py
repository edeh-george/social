import os
from typing import AsyncGenerator, Generator

import pytest
import sqlalchemy
from database import user_table
from httpx import AsyncClient

from fastapi.testclient import TestClient
from social.main import app

os.environ["ENV_STATE"] = "test"
from social.database import database


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(base_url="http://localhost:8443") as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = sqlalchemy.select(user_table).where(
        user_table.c.email == user_details["email"]
    )
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    print(user_details)
    return user_details
