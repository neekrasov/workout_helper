from typing import Optional
from app.core.common.uow import UnitOfWork
from ..protocols.user_dao import UserDAOReader, UserDAOWriter
from ..entities.user import User


class UserService:
    def __init__(
        self,
        user_dao_reader: UserDAOReader,
        user_dao_writer: UserDAOWriter,
        uow: UnitOfWork,
    ):
        self._user_dao_reader = user_dao_reader
        self._user_dao_writer = user_dao_writer
        self._uow = uow

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        async with self._uow.pipeline:
            user = await self._user_dao_reader.get_user_by_id(user_id)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self._uow.pipeline:
            user = await self._user_dao_reader.get_user_by_email(email)
        return user

    async def create_user(self, user: User) -> None:
        await self._user_dao_writer.create_user(user)
        await self._user_dao_writer.commit()
