import pytest
import asyncio
from typing import List, Tuple
from blacksheep.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from app.settings import Settings
from tests.json_converter import json_content


async def assert_updates(
    test_client: TestClient,
    task_id: str,
    count: int,
) -> dict:
    updates = await test_client.get(f"/api/v1/grounds/get-updates/{task_id}")
    updates_result = await updates.json()

    assert updates.status == 200
    assert len(updates_result["data"]) == count
    return updates_result


def assert_task_response(
    test_client: TestClient,
    response,
    data: dict,
):
    assert response.status == 200
    assert data["type"] == "ID"


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_get_nearest_grounds(test_client: TestClient):
    items_count = 1
    response = await test_client.get(
        "/api/v1/grounds/nearest",
        query={"latitude": 55, "longitude": 37, "count": items_count},
    )
    data = await response.json()
    assert_task_response(test_client, response, data)

    await asyncio.sleep(5)

    updates_result = await assert_updates(
        test_client, data["data"], items_count
    )
    assert (
        updates_result["data"][0]["contact"]["email"] == "DDS-Voronovo@mail.ru"
    )


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_search_grounds(test_client: TestClient):
    items_count = 5
    prepared_request_body = json_content(
        {
            "adm_area": "Центральный административный округ",
            "district": "Басманный район",
        }
    )

    search_response = await test_client.post(
        "/api/v1/grounds/search",
        query={"count": items_count},
        content=prepared_request_body,
    )
    search_data = await search_response.json()
    assert_task_response(test_client, search_response, search_data)

    await asyncio.sleep(5)

    updates_result = await assert_updates(
        test_client, search_data["data"], items_count
    )
    assert (
        updates_result["data"][0]["location"]["adm_area"]
        == "Центральный административный округ"
    )


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_get_recommendations(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
):
    items_count = 3

    response = await test_client.get(
        "/api/v1/grounds/recommendations",
        query={"count": items_count, "ground_id": 281867778},
        headers=first_user_token_headers,
    )

    assert response.status == 200

    rec_data = await response.json()

    assert_task_response(test_client, response, rec_data)

    await asyncio.sleep(delay=5)

    updates_result = await assert_updates(
        test_client, rec_data["data"], items_count
    )

    assert updates_result["data"][0]["contact"]["email"] == "info@parkfili.com"


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_get_user_grounds(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
):
    response = await test_client.get(
        "/api/v1/grounds/my",
        headers=first_user_token_headers,
    )

    assert response.status == 200

    data = await response.json()

    assert len(data) == 1
    assert data[0]["id"] == 281867778


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_like_ground(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
    engine: AsyncEngine,
    settings: Settings,
):
    ground_id = 406671453

    response = await test_client.post(
        "/api/v1/grounds/like",
        query={"ground_id": ground_id},
        headers=first_user_token_headers,
    )

    assert response.status == 200

    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                " SELECT EXISTS (SELECT 1 FROM liked_grounds WHERE user_id = :user_id AND ground_id = :ground_id)"  # noqa
            ),
            {
                "user_id": settings.test_user.id,
                "ground_id": ground_id,
            },
        )
        assert result.scalar() is True


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_delete_like_ground(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
    engine: AsyncEngine,
    settings: Settings,
):
    user_id = settings.test_user.id
    ground_id = 406671453

    response = await test_client.delete(
        "/api/v1/grounds/like",
        query={"ground_id": ground_id},
        headers=first_user_token_headers,
    )

    assert response.status == 200

    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                "SELECT * FROM liked_grounds WHERE user_id = :user_id AND ground_id = :ground_id"  # noqa
            ),
            {
                "user_id": user_id,
                "ground_id": ground_id,
            },
        )
        assert result.rowcount == -1


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_like_ground_errors(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
):
    response = await test_client.post(
        "/api/v1/grounds/like",
        query={"ground_id": 1},
        headers=first_user_token_headers,
    )

    assert response.status == 404

    response = await test_client.post(
        "/api/v1/grounds/like",
        query={"ground_id": 281867778},
        headers=first_user_token_headers,
    )

    assert response.status == 400


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_delete_like_errors(
    test_client: TestClient,
    first_user_token_headers: List[Tuple[bytes, bytes]],
):
    response = await test_client.delete(
        "/api/v1/grounds/like",
        query={"ground_id": 1},
        headers=first_user_token_headers,
    )

    assert response.status == 404
