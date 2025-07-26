import pytest
from httpx import AsyncClient

from social import security


async def create_post(async_client: AsyncClient, body: str, logged_in_token) -> dict:
    response = await async_client.post(
        "/",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response


async def create_comment(
    async_client: AsyncClient, post_id: int, body: str, logged_in_token
) -> dict:
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient, logged_in_token: str):
    return await create_post(async_client, "Test Post", logged_in_token)


@pytest.fixture()
async def created_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    return await create_comment(
        async_client, created_post["id"], "Test Comment", logged_in_token
    )


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"

    response = await async_client.post("/post", json={"body": body})

    assert response.status_code == 201
    assert {"id": 1, "body": body} == response.json().items()


@pytest.mark.anyio
async def test_create_post_expired_token(
    async_client: AsyncClient, registered_user: dict, mocker
):
    mocker.patch("social.security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(registered_user["email"])
    response = await async_client.post(
        "/post",
        json={"body": "Test Post"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.jsong()["detail"]


@pytest.mark.anyio
async def test_create_post_missing_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/post", jsong={}, headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 422
