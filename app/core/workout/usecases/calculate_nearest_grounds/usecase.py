import pandas as pd
from sklearn.neighbors import BallTree
from math import radians

from app.core.common.mediator import UseCase
from .command import CalculateNearestGroundCommand


class CalculateNearestGroundUseCase(
    UseCase[CalculateNearestGroundCommand, dict]
):
    def handle(self, command: CalculateNearestGroundCommand):
        data = pd.read_csv("source/processed_data.csv")
        tree = BallTree(
            data[["latitude_radians", "longitude_radians"]],
            metric="haversine",
        )
        query = tree.query(
            [[radians(command.longitude), radians(command.latitude)]],
            k=15,
            return_distance=False,
        )
        nearest = data.iloc[query[0]]
        return nearest.swapaxes(1, 0).to_dict()

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
