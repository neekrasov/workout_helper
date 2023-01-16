import asyncio
import pytest_asyncio
from redis.asyncio import Redis
from typing import List, Tuple
from rodi import Services
from blacksheep import Application
from blacksheep.testing import TestClient
from blacksheep.contents import FormContent
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text
from passlib.context import CryptContext

from app.presentation.api.main import app as api_app
from app.settings import Settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest_asyncio.fixture(scope="session")
async def api():
    await api_app.start()
    yield api_app
    await api_app.stop()


@pytest_asyncio.fixture(scope="session")
async def test_client(api: Application) -> TestClient:
    return TestClient(api)


@pytest_asyncio.fixture(scope="session")
def provider(api: Application) -> Services:
    return api.services.build_provider()


@pytest_asyncio.fixture(scope="session")
async def engine(provider: Services):
    return provider.get(AsyncEngine)


@pytest_asyncio.fixture(scope="session")
async def redis_client(provider: Services):
    return provider.get(Redis)


@pytest_asyncio.fixture(scope="session")
async def crypt_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest_asyncio.fixture(scope="session")
async def create_test_user(
    request,
    event_loop,
    engine: AsyncEngine,
    settings: Settings,
    crypt_context: CryptContext,
):
    id_ = settings.test_user.id
    username = settings.test_user.username
    email = settings.test_user.email
    hashed_password = crypt_context.hash(settings.test_user.password)
    async with engine.begin() as connection:
        await connection.execute(
            text(
                "INSERT INTO users(id, username, email, hashed_password) VALUES (:id, :username, :email, :hashed_password)"  # noqa
            ),
            {
                "id": id_,
                "username": username,
                "email": email,
                "hashed_password": hashed_password,
            },
        )

    async def delete_user():
        async with engine.begin() as connection:
            await connection.execute(
                text("DELETE FROM users WHERE email = :email"),
                {
                    "email": email,
                },
            )

    request.addfinalizer(lambda: event_loop.run_until_complete(delete_user()))


@pytest_asyncio.fixture(scope="session")
async def create_test_like(
    request,
    event_loop,
    engine: AsyncEngine,
    settings: Settings,
):
    id_ = settings.test_user.id
    async with engine.begin() as connection:
        await connection.execute(
            text(
                "INSERT INTO liked_grounds(user_id, ground_id) VALUES (:user_id, :ground_id)"  # noqa
            ),
            {
                "user_id": id_,
                "ground_id": 281867778,
            },
        )


@pytest_asyncio.fixture()
async def first_user_token_headers(
    test_client: TestClient,
    settings: Settings,
    create_test_user,
    create_test_like,
) -> List[Tuple[bytes, bytes]]:
    response = await test_client.post(
        "/api/v1/auth/login",
        content=FormContent(
            [
                ("username", settings.test_user.email),
                ("password", settings.test_user.password),
            ],
        ),
    )
    data = await response.json()
    token = data["session_id"]
    return [
        (b"Authorization", token.encode("utf8")),
    ]
