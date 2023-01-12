from typing import Optional
from sqlalchemy import select, exists

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

    async def check_user_like(self, liked_ground: LikedGround) -> bool:
        result = await self._session.execute(
            select(exists().where(
                LikedGround.user_id == liked_ground.user_id,
                LikedGround.ground_id == liked_ground.ground_id,
            ))
        )
        return result.scalar()


class GroundWriteGatewayImpl(BaseGateway, GroundWriteGateway):
    async def like_ground(self, ground: LikedGround) -> None:
        self._session.add(ground)
