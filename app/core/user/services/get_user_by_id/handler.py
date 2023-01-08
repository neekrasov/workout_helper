from typing import Optional
from app.core.common.cqs import Handler
from app.core.common.base.uow import UnitOfWork
from app.core.user.entities import User
from app.core.user.protocols.user_dao import UserDAOReader

from .query import GetUserByIDQuery


class GetUserByIDHandler(Handler[GetUserByIDQuery, Optional[User]]):
    def __init__(
        self,
        user_dao_reader: UserDAOReader,
        uow: UnitOfWork,
    ):
        self._user_dao_reader = user_dao_reader
        self._uow = uow

    async def handle(self, query: GetUserByIDQuery) -> Optional[User]:
        async with self._uow.pipeline:
            user = await self._user_dao_reader.get_user_by_id(
                str(query.user_id)
            )
        return user
