from dataclasses import dataclass

from app.core.common.mediator import Command
from ...entities.liked_grounds import UserId, GroundId


@dataclass
class LikeGroundCommand(Command):
    ground_id: GroundId
    user_id: UserId
