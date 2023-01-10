from rodi import GetServiceContext
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.mediator import MediatorImpl
from app.infrastructure.persistence.sqlalchemy.gateways import (
    UserWriteGatewayImpl,
    UserReadGatewayImpl,
)
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl
from app.infrastructure.persistence.redis.token_gateway import TokenGatewayImpl
from app.core.user.services.auth_service import AuthUserService
from app.core.user.usecases.login_user import (
    LoginUserCommand,
    LoginUserUseCase,
)
from app.core.user.usecases.create_user import (
    CreateUserCommand,
    CreateUserUseCase,
)
from app.core.user.usecases.logout_user import (
    LogoutUserCommand,
    LogoutUserUseCase,
)
from app.core.user.usecases.get_current_user import (
    GetCurrentUserCommand,
    GetCurrentUserUseCase,
)


def user_mediator_bind(
    mediator: MediatorImpl,
    session: AsyncSession,
    uow: UnitOfWorkImpl,
    redis: Redis,
    services: GetServiceContext,
):
    token_gateway = TokenGatewayImpl(redis)
    user_write_gateway = UserWriteGatewayImpl(session)
    user_read_gateway = UserReadGatewayImpl(session)
    auth_service = services.provider.get(AuthUserService)

    mediator.bind(
        LoginUserCommand,
        LoginUserUseCase(auth_service, user_read_gateway, token_gateway, uow),
    )
    mediator.bind(
        LogoutUserCommand,
        LogoutUserUseCase(auth_service, user_read_gateway, token_gateway),
    )
    mediator.bind(
        CreateUserCommand,
        CreateUserUseCase(auth_service, user_write_gateway, uow),
    )
    mediator.bind(
        GetCurrentUserCommand,
        GetCurrentUserUseCase(
            auth_service, user_read_gateway, token_gateway, uow
        ),
    )
