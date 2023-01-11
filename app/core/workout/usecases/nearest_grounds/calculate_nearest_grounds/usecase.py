import pandas as pd
from sklearn.neighbors import BallTree
from math import radians

from app.core.common.mediator import UseCase
from .command import CalculateNearestGroundCommand


class CalculateNearestGroundUseCase(
    UseCase[CalculateNearestGroundCommand, dict]
):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def handle(self, command: CalculateNearestGroundCommand):
        tree = BallTree(
            self._data[["latitude_radians", "longitude_radians"]],
            metric="haversine",
        )
        query = tree.query(
            [[radians(command.longitude), radians(command.latitude)]],
            k=command.count,
            return_distance=False,
        )
        nearest = self._data.iloc[query[0]]
        return nearest.swapaxes(1, 0).to_dict()

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
