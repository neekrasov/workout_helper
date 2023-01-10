from enum import Enum
from dataclasses import dataclass
from typing import TypeVar, Generic, NewType

T = TypeVar("T")
TaskId = NewType("TaskId", str)


class ResultStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


@dataclass
class CalculationResult(Generic[T]):
    status: ResultStatus
    data: T
