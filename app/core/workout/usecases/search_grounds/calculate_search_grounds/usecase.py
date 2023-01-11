import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.common.mediator import UseCase
from .command import CalculateSearchGroundsCommand


class CalculateSearchGroundsUseCase(
    UseCase[CalculateSearchGroundsCommand, dict]
):
    def __init__(self, data: pd.DataFrame, vectorizer: CountVectorizer):
        self._data = data
        self._vectorizer = vectorizer

    def handle(self, command: CalculateSearchGroundsCommand):
        count_matrix = self._vectorizer.fit_transform(
            self._data["combined_features"]
        )
        query = command.search_query
        words = self._vectorizer.get_feature_names_out()
        querycv = self._vectorizer.fit(words)
        querycv = querycv.transform([query])
        related = cosine_similarity(querycv, count_matrix).flatten()
        sorted_related = sorted(
            list(enumerate(related)), key=lambda x: x[1], reverse=True
        )[:command.count]
        objects = self._data.iloc[[i[0] for i in sorted_related]]
        return objects.swapaxes(1, 0).to_dict()

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
