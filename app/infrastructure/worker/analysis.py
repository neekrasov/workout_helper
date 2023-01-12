from celery import Celery, states
from celery.result import AsyncResult

from app.core.common.base.result import TaskId, ResultStatus, CalculationResult
from app.core.common.base.types import GroundId
from app.core.workout.protocols.analysis import (
    AnalysisSportsGround,
    UpdatesResult,
)


class AnalysisSportsGroundImpl(AnalysisSportsGround):
    def __init__(self, celery: Celery):
        self._celery = celery

    def get_nearest_sports_grounds(
        self, latitude: float, longitude: float, count: int
    ) -> CalculationResult[TaskId]:
        task: AsyncResult = self._celery.send_task(
            name="get_nearest_grounds", args=(latitude, longitude, count)
        )
        return CalculationResult(status=ResultStatus.PENDING, data=task.id)

    def get_updates(self, task_id: TaskId) -> UpdatesResult:
        task: AsyncResult = self._celery.AsyncResult(task_id)
        if task.state == states.SUCCESS:
            return CalculationResult(
                status=ResultStatus.SUCCESS, data=task.result
            )
        elif task.state == states.PENDING:
            return CalculationResult(status=ResultStatus.PENDING, data=task.id)
        else:
            return CalculationResult(status=ResultStatus.FAILURE, data=None)

    def search_grounds(
        self, search_query: str, count: int
    ) -> CalculationResult[TaskId]:
        task: AsyncResult = self._celery.send_task(
            name="search_grounds", args=(search_query, count)
        )
        return CalculationResult(status=ResultStatus.PENDING, data=task.id)

    def get_recommendations(
        self, ground_id: GroundId, count: int
    ) -> CalculationResult[TaskId]:
        task: AsyncResult = self._celery.send_task(
            name="get_recommendations", args=(int(ground_id), count)
        )
        return CalculationResult(status=ResultStatus.PENDING, data=task.id)
