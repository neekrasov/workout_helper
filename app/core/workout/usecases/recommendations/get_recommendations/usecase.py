from app.core.common.mediator import UseCase
from app.core.common.base.result import TaskId, CalculationResult
from app.core.common.base.uow import UnitOfWork
from .command import GetRecommendationsCommand
from ....entities import LikedGround
from ....exceptions.grounds import UserDoesNotLikeGroundException
from ....protocols.analysis import AnalysisSportsGround
from ....protocols.grounds_gateway import GroundReadGateway


class GetRecommendationsUseCase(
    UseCase[GetRecommendationsCommand, CalculationResult[TaskId]]
):
    def __init__(
        self,
        analysis: AnalysisSportsGround,
        grounds_read_gateway: GroundReadGateway,
        uow: UnitOfWork,
    ) -> None:
        self._analysis = analysis
        self._grounds_read_gateway = grounds_read_gateway
        self._uow = uow

    async def handle(
        self, command: GetRecommendationsCommand
    ) -> CalculationResult[TaskId]:
        async with self._uow.pipeline:
            user_like_existed = (
                await self._grounds_read_gateway.check_user_like(
                    LikedGround(command.user_id, command.ground_id)
                )
            )

            if not user_like_existed:
                raise UserDoesNotLikeGroundException

            recommendations = self._analysis.get_recommendations(
                command.ground_id, command.count
            )
            return recommendations
