import uuid

from app.core.common.mediator import UseCase
from app.core.common.base.uow import UnitOfWork
from ...protocols.user_gateway import UserReadGateway
from ...protocols.token_gateway import TokenGateway
from ...services.auth_service import AuthUserService
from ...exceptions.auth import (
    InvalidCredentialsException,
)
from .command import LoginUserCommand


class LoginUserUseCase(UseCase[LoginUserCommand, uuid.UUID]):
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

    async def handle(self, command: LoginUserCommand) -> uuid.UUID:
        async with self._uow.pipeline:
            user = await self._user_read_gateway.get_user_by_email(
                command.email
            )

            if not user:
                raise InvalidCredentialsException

            verify = self._auth_service.verify_pass(
                command.raw_password, user.hashed_password
            )

            if not verify:
                raise InvalidCredentialsException

            session_id = self._auth_service.generate_session_id()
            token = self._auth_service.create_token(user.id)  # type: ignore
            await self._token_gateway.save(session_id, token)
            return session_id
