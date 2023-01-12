from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.common.base.types import GroundId, UserId


@dataclass
class GetRecommendationsCommand(Command):
    ground_id: GroundId
    user_id: UserId
    count: int
