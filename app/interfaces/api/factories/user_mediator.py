from rodi import GetServiceContext
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.cqs import MediatorImpl
from app.infrastructure.user.user_dao import (
    UserDAOWriterImpl,
    UserDAOReaderImpl,
)
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl
from app.infrastructure.user.tokens_storage_dao import TokensStorageDAOImpl
from app.core.user.usecases.auth_service import AuthUserService
from app.core.user.services.create_user import (
    CreateUserCommand,
    CreateUserHandler,
)
from app.core.user.services.create_token import (
    CreateTokenCommand,
    CreateTokenHandler,
)
from app.core.user.services.delete_token import (
    DeleteTokenCommand,
    DeleteTokenHandler,
)
from app.core.user.services.get_token import (
    GetTokenQuery,
    GetTokenHandler,
)
from app.core.user.services.get_user_by_email import (
    GetUserByEmailQuery,
    GetUserByEmailHandler,
)
from app.core.user.services.get_user_by_id import (
    GetUserByIDQuery,
    GetUserByIDHandler,
)


def user_mediator_bind(
    mediator: MediatorImpl,
    session: AsyncSession,
    uow: UnitOfWorkImpl,
    redis: Redis,
    services: GetServiceContext,
):
    tokens_dao = TokensStorageDAOImpl(redis)
    user_dao_writer = UserDAOWriterImpl(session)
    user_dao_reader = UserDAOReaderImpl(session)
    auth_service = services.provider.get(AuthUserService)

    mediator.bind(
        CreateUserCommand,
        CreateUserHandler(auth_service, user_dao_writer, uow),
    )
    mediator.bind(
        CreateTokenCommand, CreateTokenHandler(auth_service, tokens_dao)
    )
    mediator.bind(
        GetUserByEmailQuery, GetUserByEmailHandler(user_dao_reader, uow)
    )
    mediator.bind(DeleteTokenCommand, DeleteTokenHandler(tokens_dao))
    mediator.bind(GetTokenQuery, GetTokenHandler(auth_service, tokens_dao))
    mediator.bind(GetUserByIDQuery, GetUserByIDHandler(user_dao_reader, uow))
    return mediator
