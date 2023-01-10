from rodi import GetServiceContext

from app.core.common.mediator import MediatorImpl
from app.core.workout.protocols.analysis import AnalysisSportsGround
from app.core.workout.usecases.get_nearest_grounds import (
    GetNearestGroundCommand,
    GetNearestGroundHandler,
)
from app.core.workout.usecases.get_updates import (
    GetUpdatesCommand,
    GetUpdatesHandler,
)


def grounds_mediator_bind(
    mediator: MediatorImpl,
    services: GetServiceContext,
):
    analysis = services.provider.get(AnalysisSportsGround)
    mediator.bind(GetNearestGroundCommand, GetNearestGroundHandler(analysis))
    mediator.bind(GetUpdatesCommand, GetUpdatesHandler(analysis))
