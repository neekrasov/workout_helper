from typing import Protocol

from app.core.common.base.types import UserId
from ..entities.user import User


class UserWriteGateway(Protocol):
    def create_user(self, user: User) -> None:
        ...


class UserReadGateway(Protocol):
    async def get_user_by_id(self, user_id: UserId) -> User:
        ...

    async def get_user_by_email(self, email: str) -> User:
        ...
