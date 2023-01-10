from app.core.user.entities.user import User
from app.core.common.mediator import UseCase
from app.core.common.base.uow import UnitOfWork
from app.core.common.base.exceptions import UniqueConstraintViolation
from .command import CreateUserCommand
from ...services.auth_service import AuthUserService
from ...protocols.user_gateway import UserWriteGateway
from ...exceptions.users import UserAlreadyExistsException


class CreateUserUseCase(UseCase[CreateUserCommand, None]):
    def __init__(
        self,
        auth_service: AuthUserService,
        user_write_gateway: UserWriteGateway,
        uow: UnitOfWork,
    ) -> None:
        self._user_write_gateway = user_write_gateway
        self._auth_service = auth_service
        self._uow = uow

    async def handle(self, command: CreateUserCommand) -> None:
        async with self._uow.pipeline:
            hashed_password = self._auth_service.hash_pass(command.password)
            user = User(
                username=command.username,
                email=command.email,
                hashed_password=hashed_password,
            )
            self._user_write_gateway.create_user(user)

            try:
                await self._uow.commit()
            except UniqueConstraintViolation:
                raise UserAlreadyExistsException
