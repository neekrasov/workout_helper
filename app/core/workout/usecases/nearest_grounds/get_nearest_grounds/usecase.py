from app.core.common.mediator import UseCase
from app.core.common.base.result import (
    TaskId,
    CalculationResult
)
from .command import GetNearestGroundCommand
from ....protocols.analysis import AnalysisSportsGround


class GetNearestGroundUseCase(
    UseCase[
        GetNearestGroundCommand,
        CalculationResult[TaskId]
    ]
):
    def __init__(self, analysis: AnalysisSportsGround) -> None:
        self._analysis = analysis

    async def handle(
        self, command: GetNearestGroundCommand
    ) -> CalculationResult[TaskId]:
        grounds = self._analysis.get_nearest_sports_grounds(
            command.latitude, command.longitude, command.count
        )
        return grounds
