import uuid
from app.core.common.cqs import MediatorProtocol

from ..auth_service import AuthUserService
from ...exceptions.auth import (
    InvalidCredentialsException,
)

from ...services.create_token import CreateTokenCommand
from ...services.get_user_by_email import GetUserByEmailQuery


class LoginUserUseCase:
    def __init__(
        self,
        auth_service: AuthUserService,
        mediator: MediatorProtocol,
    ):
        self._auth_service = auth_service
        self._mediator = mediator

    async def execute(self, email: str, raw_password: str) -> uuid.UUID:
        user = await self._mediator.send(GetUserByEmailQuery(email))

        if not user:
            raise InvalidCredentialsException

        verify = self._auth_service.verify_pass(
            raw_password, user.hashed_password
        )

        if not verify:
            raise InvalidCredentialsException

        session_id = self._auth_service.generate_session_id()
        await self._mediator.send(CreateTokenCommand(
            user_id=user.id,
            session_id=session_id,
        ))
        return session_id
