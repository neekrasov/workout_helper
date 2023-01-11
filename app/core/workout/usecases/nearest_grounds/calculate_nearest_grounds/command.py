from dataclasses import dataclass

from app.core.common.mediator import Command


@dataclass
class CalculateNearestGroundCommand(Command):
    latitude: float
    longitude: float
    count: int
