from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.common.base.types import UserId, GroundId


@dataclass
class DeleteLikeGroundCommand(Command):
    user_id: UserId
    ground_id: GroundId
