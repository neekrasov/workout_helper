from dataclasses import dataclass

from app.core.common.base.types import UserId, GroundId


@dataclass
class LikedGround:
    user_id: UserId
    ground_id: GroundId
