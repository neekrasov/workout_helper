from typing import Protocol, Optional

from app.core.common.base.types import GroundId
from ..entities import SportsGround, LikedGround


class GroundWriteGateway(Protocol):
    async def like_ground(self, ground: LikedGround) -> None:
        ...


class GroundReadGateway(Protocol):
    async def check_user_like(
        self, liked_ground: LikedGround
    ) -> bool:
        ...

    async def get_ground(self, ground_id: GroundId) -> Optional[SportsGround]:
        ...
