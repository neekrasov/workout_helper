from typing import List
from app.core.common.mediator import UseCase
from app.core.common.base.uow import UnitOfWork
from ...entities import SportsGround
from ...exceptions.grounds import GroundsNotFoundException
from ...protocols.grounds_gateway import GroundReadGateway
from .command import GetUserGroundsCommand


class GetUserGroundsUseCase(
    UseCase[GetUserGroundsCommand, List[SportsGround]]
):
    def __init__(
        self, uow: UnitOfWork, ground_read_gateway: GroundReadGateway
    ):
        self._uow = uow
        self._ground_read_gateway = ground_read_gateway

    async def handle(self, command: GetUserGroundsCommand):
        async with self._uow.pipeline:
            grounds = await self._ground_read_gateway.get_user_grounds(
                command.user_id
            )
            if not grounds:
                raise GroundsNotFoundException
            return grounds
