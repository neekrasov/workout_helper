from typing import Optional
from redis.asyncio import Redis
from app.core.user.protocols.tokens_storage_dao import TokensStorageDAO


class TokensStorageDAOImpl(TokensStorageDAO):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def save(self, session_id: str, token: str) -> None:
        await self._redis.set(session_id, token)

    async def delete_token(self, session_id: str) -> None:
        await self._redis.delete(session_id)

    async def get_token(self, session_id: str) -> Optional[str]:
        return await self._redis.get(session_id)
