import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from app.settings import Settings
from app.core.common.mediator import MediatorImpl
from app.core.workout.usecases.nearest_grounds import (
    CalculateNearestGroundCommand,
    CalculateNearestGroundUseCase,
)
from app.core.workout.usecases.search_grounds import (
    CalculateSearchGroundsCommand,
    CalculateSearchGroundsUseCase,
)


def build_mediator(settings: Settings) -> MediatorImpl:

    data = pd.read_csv(settings.dataset_path)
    cv = CountVectorizer()

    mediator = MediatorImpl()
    mediator.bind(
        CalculateNearestGroundCommand, CalculateNearestGroundUseCase(data),
    )
    mediator.bind(
        CalculateSearchGroundsCommand, CalculateSearchGroundsUseCase(data, cv),
    )
    return mediator
