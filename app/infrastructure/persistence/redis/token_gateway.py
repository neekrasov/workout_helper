from typing import Optional
from redis.asyncio import Redis

from app.core.common.base.types import SessionId
from app.core.user.protocols.token_gateway import TokenGateway


class TokenGatewayImpl(TokenGateway):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def save(self, session_id: SessionId, token: str) -> None:
        await self._redis.set(str(session_id), token)

    async def delete_token(self, session_id: SessionId) -> None:
        await self._redis.delete(str(session_id))

    async def get_token(self, session_id: SessionId) -> Optional[str]:
        return await self._redis.get(str(session_id))
