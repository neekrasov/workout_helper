import pytest
from typing import List, Tuple
from blacksheep.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from app.settings import Settings
from tests.json_converter import json_content


@pytest.mark.asyncio
async def test_create_user(
    test_client: TestClient,
    engine: AsyncEngine,
):
    email = "email@test.ru"
    response = await test_client.post(
        "/api/v1/users",
        content=json_content(
            {
                "email": email,
                "username": "testtest",
                "password": "testtest12345678",
            }
        ),
    )

    assert response.status == 201

    async with engine.begin() as connection:
        result = await connection.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {
                "email": email,
            },
        )

        row = result.first()

        assert row is not None
        assert row["username"] == "testtest"
        assert row["email"] == email

    async with engine.begin() as connection:
        await connection.execute(
            text("DELETE FROM users WHERE email = :email"),
            {
                "email": email,
            },
        )


@pytest.mark.asyncio
async def test_get_current_user(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
    settings: Settings,
):
    response = await test_client.get(
        "/api/v1/users/me",
        headers=first_user_token_headers,
    )

    assert response.status == 200

    data = await response.json()

    assert data["id"] == settings.test_user.id


@pytest.mark.asyncio
async def test_create_user_errors(
    test_client: TestClient,
    settings: Settings,
):
    response = await test_client.post(
        "/api/v1/users",
        content=json_content(
            {
                "email": settings.test_user.email,
                "username": settings.test_user.username,
                "password": settings.test_user.password,
            }
        ),
    )

    assert response.status == 400


@pytest.mark.asyncio
async def test_get_current_user_errors(
    test_client: TestClient,
):
    response = await test_client.get(
        "/api/v1/users/me",
        headers=[(b"Authorization", b"invalid_token")],
    )

    assert response.status == 401
