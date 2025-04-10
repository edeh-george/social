import pytest
from httpx import AsyncClient


async def create_post(async_client: AsyncClient, body: str) -> dict:
    response = await async_client.post("/post", json={"body": body})
    print(response.json())
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


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() == created_post