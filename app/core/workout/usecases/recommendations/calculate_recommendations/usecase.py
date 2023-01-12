import pandas as pd

from app.core.common.mediator import UseCase
from app.core.common.base.types import GroundId
from .command import CalculateRecommendationsCommand


class CalculateRecommendationsUseCase(
    UseCase[CalculateRecommendationsCommand, dict]
):
    def __init__(self, cosine_sim: pd.DataFrame, data: pd.DataFrame):
        self._cosine_sim = cosine_sim
        self._data = data

    def handle(self, command: CalculateRecommendationsCommand):
        ground_id = command.ground_id
        index = self._get_index_by_id(self._data, ground_id)
        sorted_similar = self._get_sorted_similarity_list(
            index, self._cosine_sim
        )[1:command.count+1]
        objects = self._data.iloc[[i[0] for i in sorted_similar]]
        return objects.swapaxes(1, 0).to_dict()

    def _get_sorted_similarity_list(
        self, index: int, cosine_sim_array: pd.DataFrame
    ) -> list[tuple[int, float]]:
        return sorted(
            list(enumerate(cosine_sim_array[index])),
            key=lambda x: x[1],
            reverse=True,
        )

    def _get_index_by_id(
        self, data: pd.DataFrame, id_: GroundId
    ) -> pd.DataFrame:
        return data[data.global_id == id_].index.values[0]

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
