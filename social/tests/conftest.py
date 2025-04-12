import os
from typing import AsyncGenerator, Generator

import pytest
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
