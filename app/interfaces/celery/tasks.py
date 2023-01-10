from app.core.common.mediator import MediatorImpl
from app.core.workout.usecases.calculate_nearest_grounds import (
    CalculateNearestGroundCommand,
)


def get_nearest_grounds(
    latitude: float, longitude: float, mediator: MediatorImpl
):
    return mediator.send_sync(
        CalculateNearestGroundCommand(latitude=latitude, longitude=longitude)
    )
