from typing import Optional
from sqlalchemy import select

from app.core.common.base.types import GroundId
from app.core.workout.protocols.grounds_gateway import (
    GroundWriteGateway,
    GroundReadGateway,
)
from app.core.workout.entities import SportsGround, LikedGround
from ..gateway import BaseGateway


class GroundReadGatewayImpl(BaseGateway, GroundReadGateway):
    async def get_ground(self, ground_id: GroundId) -> Optional[SportsGround]:
        ground = await self._session.execute(
            select(SportsGround).where(SportsGround.id == ground_id)
        )
        return ground.scalar_one_or_none()


class GroundWriteGatewayImpl(BaseGateway, GroundWriteGateway):
    async def like_ground(self, ground: LikedGround) -> None:
        self._session.add(ground)
