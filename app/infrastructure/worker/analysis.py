from celery import Celery, states
from celery.result import AsyncResult

from app.core.common.base.result import (
    TaskId,
    ResultStatus,
    CalculationResult
)
from app.core.workout.protocols.analysis import (
    AnalysisSportsGround,
    UpdatesResult,
)


class AnalysisSportsGroundImpl(AnalysisSportsGround):
    def __init__(self, celery: Celery):
        self._celery = celery

    def get_nearest_sports_grounds(
        self, latitude: float, longitude: float
    ) -> CalculationResult[TaskId]:
        task: AsyncResult = self._celery.send_task(
            name="get_nearest_grounds", args=(latitude, longitude)
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
