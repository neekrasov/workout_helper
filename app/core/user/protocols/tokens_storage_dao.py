from typing import Protocol, Optional


class TokensStorageDAO(Protocol):
    async def save(self, session_id: str, token: str) -> None:
        ...

    async def delete_token(self, session_id: str) -> None:
        ...

    async def get_token(self, session_id: str) -> Optional[str]:
        ...
