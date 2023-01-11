from rodi import GetServiceContext

from app.core.common.mediator import MediatorImpl
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


def grounds_mediator_bind(
    mediator: MediatorImpl,
    services: GetServiceContext,
):
    analysis = services.provider.get(AnalysisSportsGround)
    mediator.bind(GetNearestGroundCommand, GetNearestGroundUseCase(analysis))
    mediator.bind(GetUpdatesCommand, GetUpdatesUseCase(analysis))
    mediator.bind(SearchGroundsCommand, SearchGroundsUseCase(analysis))
