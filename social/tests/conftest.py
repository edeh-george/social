from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from fastapi.testclient import TestClient
from social.main import app
from social.router.posts import comment_table, post_table


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(base_url="http://test") as ac:
        yield ac
