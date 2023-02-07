import io
import bs4
import time
import requests
import zipfile
import pandas as pd
import numpy as np
from selenium import webdriver
from sqlalchemy.engine import Engine

from app.core.dataset.exceptions import ParsingSiteNotAvailable
from app.core.dataset.protocols import (
    DatasetLoader,
    DatasetToFileSaver,
    DatasetToDBSaver,
)


class DatasetLoaderImpl(DatasetLoader):
    def __init__(self, browser: webdriver.Chrome):
        self._browser = browser

    def load(self, url: str) -> pd.DataFrame:
        self._find_zip(url)
        time.sleep(10)

        bytes = self._download_zip()
        file, file_list = self._unpack_zip(bytes)
        return self._get_dataframe_from_bytes(file)

    def _find_zip(self, url: str):
        self._browser.get(url)
        button = self._browser.find_element(
            "xpath", "//a[contains(., 'Скачать')]"
        )
        button.click()

    def _download_zip(self) -> io.BytesIO:
        soup = bs4.BeautifulSoup(self._browser.page_source, "html.parser")
        try:
            link = (
                soup.find("div", id="dropDownloads")
                .find_all("a")[0]
                .get("href")
            )
        except IndexError:
            raise ParsingSiteNotAvailable
        https_link = "https:" + link
        response = requests.get(https_link)

        if response.status_code != 200:
            raise ParsingSiteNotAvailable

        bytes = io.BytesIO(response.content)
        return bytes

    def _unpack_zip(self, bytes: io.BytesIO) -> tuple[bytes, zipfile.ZipInfo]:
        fzip = zipfile.ZipFile(bytes)
        file_list = fzip.infolist()
        file = fzip.open(file_list[0].filename)
        return (file, file_list)  # type: ignore

    def _get_dataframe_from_bytes(
        self, file: bytes, encoding="Windows-1251"
    ) -> pd.DataFrame:
        data = pd.read_json(file, encoding=encoding)
        return data


class CosineSimilaritySaver(DatasetToFileSaver[np.ndarray]):
    def save(self, dataset: np.ndarray, path: str) -> None:
        np.savetxt(path, dataset, delimiter=",")


class BaseDatasetSaver(DatasetToFileSaver[pd.DataFrame]):
    def save(self, dataset: pd.DataFrame, path: str) -> None:
        dataset.to_csv(path)


class DatasetToDBSaverImpl(DatasetToDBSaver):
    def __init__(self, engine: Engine):
        self._engine = engine

    def save(self, dataset: pd.DataFrame):
        dataset.to_sql(
            "sports_grounds",
            self._engine,
            if_exists="append",
            index=True,
            method=self._insert_do_nothing_on_conflicts,
        )

    def _insert_do_nothing_on_conflicts(self, sqltable, conn, keys, data_iter):
        """
        Execute SQL statement inserting data

        Parameters
        ----------
        sqltable : pandas.io.sql.SQLTable
        conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
        keys : list of str
            Column names
        data_iter : Iterable that iterates the values to be inserted
        """
        from sqlalchemy.dialects.postgresql import insert
        from sqlalchemy import table, column

        columns = []
        for c in keys:
            columns.append(column(c))

        if sqltable.schema:
            table_name = "{}.{}".format(sqltable.schema, sqltable.name)
        else:
            table_name = sqltable.name

        mytable = table(table_name, *columns)

        insert_stmt = insert(mytable).values(list(data_iter))
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
            index_elements=["id"]
        )

        conn.execute(do_nothing_stmt)
