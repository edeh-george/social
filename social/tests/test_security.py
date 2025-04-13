import pytest
import security


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    """
    Test the get_user function
    """
    user = await security.get_user(registered_user["email"])
    assert user is not None
    assert user["email"] == registered_user["email"]
    assert user["id"] == registered_user["id"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("test@example.com")
    assert user is None
