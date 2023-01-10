import uuid

from app.core.common.mediator import UseCase
from app.core.common.base.uow import UnitOfWork
from ...entities.user import User, UserId
from ...protocols.user_gateway import UserReadGateway
from ...protocols.token_gateway import TokenGateway
from ...services.auth_service import AuthUserService
from ...exceptions.auth import (
    SessionNotFoundException,
)
from .command import GetCurrentUserCommand


class GetCurrentUserUseCase(UseCase[GetCurrentUserCommand, User]):
    def __init__(
        self,
        auth_service: AuthUserService,
        user_read_gateway: UserReadGateway,
        token_gateway: TokenGateway,
        uow: UnitOfWork,
    ):
        self._auth_service = auth_service
        self._user_read_gateway = user_read_gateway
        self._token_gateway = token_gateway
        self._uow = uow

    async def handle(self, command: GetCurrentUserCommand) -> User:
        token = await self._token_gateway.get_token(command.session_id)

        if not token:
            raise SessionNotFoundException

        user_id = uuid.UUID(self._auth_service.decode_token(token))

        async with self._uow.pipeline:
            return await self._user_read_gateway.get_user_by_id(
                UserId(user_id)
            )
