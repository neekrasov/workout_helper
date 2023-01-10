from typing import Protocol, Union, Any

from app.core.common.base.result import (
    TaskId,
    CalculationResult
)

UpdatesResult = CalculationResult[Union[TaskId, Any]]


class AnalysisSportsGround(Protocol):  # Celery absctract class
    def get_nearest_sports_grounds(
        self, latitude: float, longitude: float
    ) -> CalculationResult[TaskId]:
        ...

    def get_updates(self, task_id: TaskId) -> UpdatesResult:
        ...
