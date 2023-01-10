from dataclasses import dataclass

from app.core.common.mediator import Command


@dataclass
class GetNearestGroundCommand(Command):
    latitude: float
    longitude: float
