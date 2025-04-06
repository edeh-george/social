import pytest
from httpx import AsyncClient


async def create_post(client: AsyncClient, body: str) -> dict:
    response = await client.post("/post", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post(async_client, "This is a test post.")


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"

    response = await async_client.post("/post", json={"body": body})

    assert response.status_code == 201
    assert {"id": 0, "body": body} <= response.json().items()
