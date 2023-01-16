import pytest
from typing import List, Tuple
from redis.asyncio import Redis
from blacksheep.testing import TestClient
from blacksheep.contents import FormContent


@pytest.mark.asyncio
async def test_login(
    test_client: TestClient,
    redis_client: Redis,
    first_user_token_headers: List[Tuple[bytes, bytes]],
) -> None:

    assert first_user_token_headers is not None
    assert len(first_user_token_headers[0]) == 2
    assert first_user_token_headers[0][0] == b"Authorization"
    assert first_user_token_headers[0][1] is not None

    token = await redis_client.get(first_user_token_headers[0][1])

    assert token is not None


@pytest.mark.asyncio
async def test_login_errors(
    test_client: TestClient,
):
    response = await test_client.post(
        "/api/v1/auth/login",
        content=FormContent(
            [
                ("username", "123456789"),
                ("password", "123456789"),
            ],
        ),
    )

    assert response.status == 401


@pytest.mark.asyncio
async def test_logout(
    test_client: TestClient,
    redis_client: Redis,
    first_user_token_headers: List[Tuple[bytes, bytes]],
):
    response = await test_client.post(
        "/api/v1/auth/logout",
        query={"session_id": first_user_token_headers[0][1]},
    )

    assert response.status == 202

    token = await redis_client.get(first_user_token_headers[0][1])

    assert token is None


@pytest.mark.asyncio
async def test_logout_errors(
    test_client: TestClient,
):
    response = await test_client.post(
        "/api/v1/auth/logout",
        query={"session_id": "123456789"},
    )

    assert response.status == 400

    response = await test_client.post(
        "/api/v1/auth/logout",
        query={"session_id": "b3dab05d-d9ad-49f4-a25d-c12b4a9b0b05"},
    )

    assert response.status == 404
