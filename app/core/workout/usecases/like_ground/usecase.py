from app.core.common.mediator import UseCase
from app.core.common.base.uow import UnitOfWork
from ...entities import LikedGround
from .command import LikeGroundCommand
from ...protocols.grounds_gateway import (
    GroundWriteGateway,
    GroundReadGateway
)
from ...exceptions.grounds import GroundsNotFoundException


class LikeGroundUseCase(UseCase[LikeGroundCommand, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        grounds_write_gateway: GroundWriteGateway,
        grounds_read_gateway: GroundReadGateway,
    ):
        self._uow = uow
        self._grounds_write_gateway = grounds_write_gateway
        self._grounds_read_gateway = grounds_read_gateway

    async def handle(self, command: LikeGroundCommand) -> None:
        async with self._uow.pipeline:
            ground = await self._grounds_read_gateway.get_ground(
                command.ground_id
            )
            if not ground:
                raise GroundsNotFoundException

            await self._grounds_write_gateway.like_ground(
                LikedGround(command.user_id, command.ground_id)
            )
            await self._uow.commit()
