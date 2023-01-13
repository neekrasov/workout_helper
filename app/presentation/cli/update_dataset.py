import re
import bs4
import zipfile
import io
import requests
import math
import time
import pandas as pd
from functools import partial
from sqlalchemy.engine import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.settings import Settings


pd.options.mode.chained_assignment = None

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.3",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "se-ch-ua": 'Google Chrome";v="105", "Not)A;Brand";v="8", \
    "Chromium";v="105',
    "cache-control": "max-age=0",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/ \
    avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3; \
    q=0.9",
}
URL = "https://data.mos.ru/opendata/7708308010-trenajernye-gorodki-vorkauty"


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


def insert_data_to_db(data: pd.DataFrame):
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/workout"
    )
    data.to_sql(
        "sports_grounds",
        engine,
        if_exists="append",
        index=True,
        method=insert_do_nothing_on_conflicts,
    )


def find_zip(url: str, browser: webdriver.Chrome):
    browser.get(URL)
    browser.find_element("xpath", "//a[contains(., 'Скачать')]").click()


def download_zip(browser: webdriver.Chrome) -> io.BytesIO:
    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    link = soup.find("div", id="dropDownloads").find_all("a")[0].get("href")
    https_link = "https:" + link
    zip = requests.get(https_link)
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


def save_data_to_csv(data: pd.DataFrame, path: str):
    data.to_csv(path)


def main():
    browser = webdriver.Chrome(service=Service("/usr/bin/chromedriver"))
    settings = Settings()
    dataset_path = settings.dataset.dataset_path
    print(dataset_path)
    print("Chrome driver is started")
    print("Getting data from URL...")
    find_zip(URL, browser)
    print("Downloading zip file...")
    time.sleep(5)
    bytes = download_zip(browser)
    print("Unpacking zip file...")
    file, file_list = unpack_zip(bytes)
    print("File name: " + file_list[0].filename)
    print("Getting data from file...")
    data = get_dataframe_from_bytes(file)
    print("Processing data...")
    data = base_process_data(data)
    print("Saving data to CSV...")
    save_data_to_csv(data, dataset_path)
    data = adapt_dataset_to_db_schema(data)
    print("Inserting data to DB...")
    insert_data_to_db(data)
    print("Done!")

    browser.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
