import uuid

from app.core.common.mediator import UseCase
from ...entities.user import UserId
from ...protocols.user_gateway import UserReadGateway
from ...protocols.token_gateway import TokenGateway
from ...services.auth_service import AuthUserService
from ...exceptions.auth import (
    SessionNotFoundException,
)
from .command import LogoutUserCommand


class LogoutUserUseCase(UseCase[LogoutUserCommand, uuid.UUID]):
    def __init__(
        self,
        auth_service: AuthUserService,
        user_read_gateway: UserReadGateway,
        token_gateway: TokenGateway,
    ):
        self._auth_service = auth_service
        self._user_read_gateway = user_read_gateway
        self._token_gateway = token_gateway

    async def handle(self, command: LogoutUserCommand) -> UserId:
        token = await self._token_gateway.get_token(command.session_id)

        if not token:
            raise SessionNotFoundException

        user_id = self._auth_service.decode_token(token)
        await self._token_gateway.delete_token(command.session_id)
        return UserId(uuid.UUID(user_id))
