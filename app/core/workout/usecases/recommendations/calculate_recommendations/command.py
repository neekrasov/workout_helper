from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.common.base.types import GroundId


@dataclass
class CalculateRecommendationsCommand(Command):
    ground_id: GroundId
    count: int
