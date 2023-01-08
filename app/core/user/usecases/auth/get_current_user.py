import uuid
from app.core.common.cqs import MediatorProtocol

from ...entities.user import User
from ..auth_service import AuthUserService
from ...exceptions.auth import (
    SessionNotFoundException,
)

from ...services.get_token import GetTokenQuery
from ...services.get_user_by_id import GetUserByIDQuery


class GetCurrentUserUseCase:
    def __init__(
        self,
        auth_user_service: AuthUserService,
        mediator: MediatorProtocol,
    ):
        self._auth_user_service = auth_user_service
        self._mediator = mediator

    async def execute(self, session_id: str) -> User:
        session_id_: uuid.UUID = uuid.UUID(session_id)
        token: str = await self._mediator.send(GetTokenQuery(session_id_))

        if not token:
            raise SessionNotFoundException

        user_id = self._auth_user_service.decode_token(token)

        return await self._mediator.send(GetUserByIDQuery(uuid.UUID(user_id)))
