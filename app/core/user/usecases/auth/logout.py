import uuid
from app.core.common.cqs import MediatorProtocol

from ..auth_service import AuthUserService
from ...exceptions.auth import (
    SessionNotFoundException,
)

from ...services.delete_token import DeleteTokenCommand
from ...services.get_token import GetTokenQuery


class LogoutUserUseCase:
    def __init__(
        self,
        auth_service: AuthUserService,
        mediator: MediatorProtocol,
    ):
        self._auth_service = auth_service
        self._mediator = mediator

    async def execute(self, session_id: uuid.UUID) -> uuid.UUID:
        token = await self._mediator.send(GetTokenQuery(session_id))

        if not token:
            raise SessionNotFoundException

        user_id = self._auth_service.decode_token(token)
        await self._mediator.send(DeleteTokenCommand(session_id))
        return uuid.UUID(user_id)
