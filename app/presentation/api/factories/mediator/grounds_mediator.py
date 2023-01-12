from rodi import GetServiceContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.mediator import MediatorImpl
from app.core.common.base.uow import UnitOfWork
from app.core.workout.protocols.analysis import AnalysisSportsGround
from app.core.workout.usecases.nearest_grounds import (
    GetNearestGroundCommand,
    GetNearestGroundUseCase,
)
from app.core.workout.usecases.get_updates import (
    GetUpdatesCommand,
    GetUpdatesUseCase,
)
from app.core.workout.usecases.search_grounds import (
    SearchGroundsCommand,
    SearchGroundsUseCase,
)
from app.core.workout.usecases.like_ground import (
    LikeGroundCommand,
    LikeGroundUseCase,
)
from app.infrastructure.persistence.sqlalchemy.gateways import (
    GroundReadGatewayImpl,
    GroundWriteGatewayImpl,
)


def grounds_mediator_bind(
    mediator: MediatorImpl,
    services: GetServiceContext,
    uow: UnitOfWork,
    session: AsyncSession,
):

    grounds_write_gateway = GroundWriteGatewayImpl(session)
    grounds_read_gateway = GroundReadGatewayImpl(session)

    analysis = services.provider.get(AnalysisSportsGround)
    mediator.bind(GetNearestGroundCommand, GetNearestGroundUseCase(analysis))
    mediator.bind(GetUpdatesCommand, GetUpdatesUseCase(analysis))
    mediator.bind(SearchGroundsCommand, SearchGroundsUseCase(analysis))
    mediator.bind(
        LikeGroundCommand,
        LikeGroundUseCase(uow, grounds_write_gateway, grounds_read_gateway),
    )
