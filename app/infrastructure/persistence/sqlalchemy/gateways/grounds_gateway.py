from typing import Optional, List
from sqlalchemy import select, exists, delete

from app.core.common.base.types import GroundId, UserId
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
            select(
                exists().where(
                    LikedGround.user_id == liked_ground.user_id,
                    LikedGround.ground_id == liked_ground.ground_id,
                )
            )
        )
        return result.scalar()

    async def get_user_grounds(
        self, user_id: UserId
    ) -> Optional[List[SportsGround]]:
        result = await self._session.execute(
            select(SportsGround)
            .join(LikedGround)
            .filter(LikedGround.user_id == user_id)
        )
        grounds = result.scalars().all()
        if not grounds:
            return None
        return grounds


class GroundWriteGatewayImpl(BaseGateway, GroundWriteGateway):
    async def like_ground(self, ground: LikedGround) -> None:
        self._session.add(ground)

    async def delete_like(self, ground: LikedGround) -> None:
        stmt = delete(LikedGround).where(
            LikedGround.user_id == ground.user_id,
            LikedGround.ground_id == ground.ground_id,
        )
        await self._session.execute(stmt)
