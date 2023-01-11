from sqlalchemy.ext.asyncio import AsyncSession
from rodi import GetServiceContext
from redis.asyncio import Redis

from app.core.common.mediator import MediatorImpl, Mediator
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl

from .user_mediator import user_mediator_bind
from .grounds_mediator import grounds_mediator_bind


def mediator_factory(services: GetServiceContext) -> Mediator:
    mediator = MediatorImpl()

    session = services.provider.get(AsyncSession)
    uow = UnitOfWorkImpl(session)
    redis = services.provider.get(Redis)

    user_mediator_bind(mediator, session, uow, redis, services)
    grounds_mediator_bind(mediator, services, uow, session)

    return mediator
