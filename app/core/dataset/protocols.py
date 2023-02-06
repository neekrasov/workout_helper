from typing import Protocol, Generic, TypeVar
from abc import ABC, abstractmethod
from pandas import DataFrame

T = TypeVar("T")


class DatasetLoader(Protocol):
    def load(self, url: str) -> DataFrame:
        ...


class DatasetToFileSaver(Generic[T], ABC):
    @abstractmethod
    def save(self, dataset: T, path: str):
        ...


class DatasetToDBSaver(Protocol):
    def save(self, dataset: DataFrame) -> None:
        ...


class DatasetHandler(Protocol):
    def handle(self, data: DataFrame) -> DataFrame:
        ...
