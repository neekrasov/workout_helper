import re
import bs4
import zipfile
import io
import requests
import math
import time
import typing as t
import pandas as pd
import numpy as np
from celery import Celery
from functools import partial
from sqlalchemy.engine import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.settings import Settings


pd.options.mode.chained_assignment = None


def combine_features(row, features):
    data = [f"{str(feature)}:{str(row[feature])} " for feature in features]
    return " ".join(data)


def base_process_data(data: pd.DataFrame) -> pd.DataFrame:
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

    data["latitude_radians"] = data.latitude.apply(lambda x: math.radians(x))
    data["longitude_radians"] = data.longitude.apply(lambda x: math.radians(x))

    features = list(data)[2:23]
    data["combined_features"] = data.apply(
        partial(combine_features, features=features), axis=1
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
        columns={"web_site": "website", "help_phone": "phone"}, inplace=True
    )

    return data


def adapt_dataset_to_db_schema(data: pd.DataFrame) -> pd.DataFrame:
    for column in list(data)[-3:]:
        data.drop(column, axis=1, inplace=True)

    return data


def insert_do_nothing_on_conflicts(sqltable, conn, keys, data_iter):
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
    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["id"])

    conn.execute(do_nothing_stmt)


def insert_data_to_db(data: pd.DataFrame, postgres_url: str):
    engine = create_engine(postgres_url)
    data.to_sql(
        "sports_grounds",
        engine,
        if_exists="append",
        index=True,
        method=insert_do_nothing_on_conflicts,
    )


def find_zip(url: str, browser: webdriver.Chrome):
    browser.get(url)
    button = browser.find_element("xpath", "//a[contains(., 'Скачать')]")
    button.click()


def get_options() -> webdriver.ChromeOptions:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    return chrome_options


def download_zip(browser: webdriver.Chrome) -> t.Optional[io.BytesIO]:
    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    try:
        link = (
            soup.find("div", id="dropDownloads").find_all("a")[0].get("href")
        )
    except IndexError:
        return None

    https_link = "https:" + link
    zip = requests.get(https_link)

    if zip.status_code != 200:
        return None

    bytes = io.BytesIO(zip.content)
    return bytes


def unpack_zip(bytes: io.BytesIO):
    fzip = zipfile.ZipFile(bytes)
    file_list = fzip.infolist()
    file = fzip.open(file_list[0].filename)
    return (file, file_list)


def get_dataframe_from_bytes(file, encoding="Windows-1251") -> pd.DataFrame:
    data = pd.read_json(file, encoding=encoding)
    return data


def calculate_cosine_sim(data: pd.DataFrame) -> np.ndarray:
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data["combined_features"])
    cosine_sim = cosine_similarity(
        count_matrix
    )  # бинарная мера сходства объектов
    return cosine_sim


def save_cosine_sim_to_csv(cosine_sim: np.ndarray, path: str):
    np.savetxt(path, cosine_sim, delimiter=",")


def save_data_to_csv(data: pd.DataFrame, path: str):
    data.to_csv(path)


def main(
    parse_url: str, dataset_path: str, postgres_url: str, cosine_sim_path: str
):
    browser = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"), options=get_options()
    )

    print("Chrome driver is started")
    print("Getting data from URL...")
    find_zip(parse_url, browser)
    print("Downloading zip file...")
    time.sleep(10)
    bytes = download_zip(browser)
    if bytes is None:
        print("The service is not available, contact the administrator.")
        return
    print("Unpacking zip file...")
    file, file_list = unpack_zip(bytes)
    print("File name: " + file_list[0].filename)
    print("Getting data from file...")
    data = get_dataframe_from_bytes(file)
    print("Processing data...")
    data = base_process_data(data)
    print("Data preview:", list(data))
    print("Saving base processed data to CSV...")
    save_data_to_csv(data, dataset_path)
    print("Calculating cosine similarity...")
    cosine_sim = calculate_cosine_sim(data)
    print("Saving cosine similarity to CSV...")
    save_cosine_sim_to_csv(cosine_sim, cosine_sim_path)
    data = adapt_dataset_to_db_schema(data)
    print("Inserting data to DB...")
    insert_data_to_db(data, postgres_url)
    print("Done!")

    browser.close()


if __name__ == "__main__":
    settings = Settings()
    celery = Celery(
        "app",
        backend=settings.redis.redis_url,
        broker=settings.redis.redis_url,
    )
    celery.send_task(
        "update_dataset",
        args=(
            settings.dataset.parse_url,
            settings.dataset.dataset_path,
            settings.postgres.postgres_url.replace("+asyncpg", ""),
            settings.dataset.recomm_cosine_sim_path,
        ),
    )
