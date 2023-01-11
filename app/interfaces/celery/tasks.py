from app.core.common.mediator import Mediator
from app.core.workout.usecases.nearest_grounds import (
    CalculateNearestGroundCommand,
)
from app.core.workout.usecases.search_grounds import (
    CalculateSearchGroundsCommand,
)


def get_nearest_grounds(
    latitude: float, longitude: float, count: int, mediator: Mediator
):
    return mediator.send_sync(
        CalculateNearestGroundCommand(latitude, longitude, count)
    )


def search_grounds(search_query: str, count: int, mediator: Mediator):
    return mediator.send_sync(
        CalculateSearchGroundsCommand(search_query, count)
    )