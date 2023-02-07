import re
import math
from functools import partial
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .protocols import DatasetHandler, DatasetToFileSaver, DatasetToDBSaver


class BaseProcessingDatasetHandler(DatasetHandler):
    def __init__(self, saver: DatasetToFileSaver, path: str):
        self._saver = saver
        self._path = path

    def handle(self, data: DataFrame) -> DataFrame:
        # Парсинг данных геолокации
        data["latitude"] = data.geoData.apply(lambda x: x["coordinates"][0])
        data["longitude"] = data.geoData.apply(lambda x: x["coordinates"][1])
        # Удаление ненужных столбцов
        data.drop("geoData", axis=1, inplace=True)
        data.drop("HelpPhoneExtension", axis=1, inplace=True)
        data.drop("PaidComments", axis=1, inplace=True)
        data.drop("EquipmentRentalComments", axis=1, inplace=True)
        data.drop("TechServiceComments", axis=1, inplace=True)
        # Удаление нулевых столбцов
        data = data.loc[:, data.notna().all(axis=0)]

        data["latitude_radians"] = data.latitude.apply(
            lambda x: math.radians(x)
        )
        data["longitude_radians"] = data.longitude.apply(
            lambda x: math.radians(x)
        )

        features = list(data)[2:23]
        data["combined_features"] = data.apply(
            partial(self._combine_features, features=features), axis=1
        )
        data.rename(columns={"global_id": "id"}, inplace=True)
        data.set_index("id", inplace=True)

        new_names = []
        for column in list(data):
            new_names.append(re.sub(r"(?<!^)(?=[A-Z])", "_", column).lower())

        data = data.replace("да", True)
        data = data.replace("нет", False)
        data.columns = new_names
        data.astype(
            {
                "seats": int,
                "has_equipment_rental": bool,
                "has_tech_service": bool,
                "has_dressing_room": bool,
                "has_eatery": bool,
                "has_toilet": bool,
                "has_wifi": bool,
                "has_cash_machine": bool,
                "has_first_aid_post": bool,
                "has_music": bool,
                "paid": str,
            }
        )
        data.rename(
            columns={"web_site": "website", "help_phone": "phone"},
            inplace=True,
        )

        self._saver.save(data, self._path)
        return data

    def _combine_features(self, row, features):
        data = [f"{str(feature)}:{str(row[feature])} " for feature in features]
        return " ".join(data)


class CalculateCosineSimilatiryDatasetHandler(DatasetHandler):
    def __init__(self, saver: DatasetToFileSaver, path: str):
        self._saver = saver
        self._path = path

    def handle(self, data: DataFrame) -> None:
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(data["combined_features"])
        cosine_sim = cosine_similarity(
            count_matrix
        )

        self._saver.save(cosine_sim, self._path)


class DatasetToDBHandler(DatasetHandler):
    def __init__(self, saver: DatasetToDBSaver):
        self._saver = saver

    def handle(self, dataset: DataFrame):
        for column in list(dataset)[-3:]:
            dataset.drop(column, axis=1, inplace=True)

        self._saver.save(dataset)
