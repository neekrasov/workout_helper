from app.core.common.mediator import UseCase
from app.core.common.base.uow import UnitOfWork
from .command import DeleteLikeGroundCommand
from ...entities import LikedGround
from ...exceptions.grounds import UserDoesNotLikeGroundException
from ...protocols.grounds_gateway import (
    GroundWriteGateway,
    GroundReadGateway,
)


class DeleteLikeGroundUseCase(UseCase[DeleteLikeGroundCommand, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        grounds_write_gateway: GroundWriteGateway,
        grounds_read_gateway: GroundReadGateway,
    ):
        self._uow = uow
        self._grounds_write_gateway = grounds_write_gateway
        self._grounds_read_gateway = grounds_read_gateway

    async def handle(self, command: DeleteLikeGroundCommand) -> None:
        async with self._uow.pipeline:
            liked_ground = LikedGround(
                command.user_id,
                command.ground_id,
            )
            like = await self._grounds_read_gateway.check_user_like(
                liked_ground
            )
            if not like:
                raise UserDoesNotLikeGroundException()

            await self._grounds_write_gateway.delete_like(liked_ground)
            await self._uow.commit()
