from typing import Protocol
from app.core.common.base.dao import DAO
from ..entities.user import User


class UserDAOWriter(DAO, Protocol):
    def create_user(self, user: User) -> None:
        ...


class UserDAOReader(DAO, Protocol):
    async def get_user_by_id(self, user_id: str) -> User:
        ...

    async def get_user_by_email(self, email: str) -> User:
        ...
