from app.core.user.entities.user import User
from app.core.common.cqs import Handler
from app.core.common.base.uow import UnitOfWork
from app.core.common.base.exceptions import UniqueConstraintViolation

from .command import CreateUserCommand
from ...usecases.auth_service import AuthUserService
from ...protocols.user_dao import UserDAOWriter
from ...exceptions.users import UserAlreadyExistsException


class CreateUserHandler(Handler[CreateUserCommand, None]):
    def __init__(
        self,
        auth_service: AuthUserService,
        user_dao_writer: UserDAOWriter,
        uow: UnitOfWork,
    ) -> None:
        self._auth_service = auth_service
        self._uow = uow
        self._user_dao_writer = user_dao_writer

    async def handle(self, event: CreateUserCommand) -> None:
        async with self._uow.pipeline:
            hashed_password = self._auth_service.hash_pass(event.password)
            user = User(  # type: ignore
                username=event.username,
                email=event.email,
                hashed_password=hashed_password,
            )
            self._user_dao_writer.create_user(user)

            try:
                await self._uow.commit()
            except UniqueConstraintViolation:
                raise UserAlreadyExistsException
