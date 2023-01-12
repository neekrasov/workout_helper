from typing import Protocol, Union, Any

from app.core.common.base.result import TaskId, CalculationResult
from app.core.common.base.types import GroundId

UpdatesResult = CalculationResult[Union[TaskId, Any]]


class AnalysisSportsGround(Protocol):
    def get_nearest_sports_grounds(
        self, latitude: float, longitude: float, count: int
    ) -> CalculationResult[TaskId]:
        ...

    def get_updates(self, task_id: TaskId) -> UpdatesResult:
        ...

    def search_grounds(
        self, search_query: str, count: int
    ) -> CalculationResult[TaskId]:
        ...

    def get_recommendations(
        self, ground_id: GroundId, count: int
    ) -> CalculationResult[TaskId]:
        ...
