from typing import Protocol, Optional, List

from app.core.common.base.types import GroundId, UserId
from ..entities import SportsGround, LikedGround


class GroundWriteGateway(Protocol):
    async def like_ground(self, ground: LikedGround) -> None:
        ...

    async def delete_like(self, ground: LikedGround) -> None:
        ...


class GroundReadGateway(Protocol):
    async def check_user_like(self, liked_ground: LikedGround) -> bool:
        ...

    async def get_ground(self, ground_id: GroundId) -> Optional[SportsGround]:
        ...

    async def get_user_grounds(
        self, user_id: UserId
    ) -> Optional[List[SportsGround]]:
        ...
