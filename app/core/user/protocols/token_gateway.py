import uuid
from typing import Protocol, Optional, NewType

SessionId = NewType("SessionId", uuid.UUID)


class TokenGateway(Protocol):
    async def save(self, session_id: SessionId, token: str) -> None:
        ...

    async def delete_token(self, session_id: SessionId) -> None:
        ...

    async def get_token(self, session_id: SessionId) -> Optional[str]:
        ...
