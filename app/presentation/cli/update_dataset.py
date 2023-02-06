import pandas as pd
from celery import Celery
from sqlalchemy.engine import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.settings import Settings

from app.core.dataset.exceptions import ParsingSiteNotAvailable
from app.core.dataset.handlers import (
    BaseProcessingDatasetHandler,
    CalculateCosineSimilatiryDatasetHandler,
    DatasetToDBHandler,
)
from app.infrastructure.worker.dataset import (
    DatasetLoaderImpl,
    CosineSimilaritySaver,
    BaseDatasetSaver,
    DatasetToDBSaverImpl,
)

pd.options.mode.chained_assignment = None


def get_options() -> webdriver.ChromeOptions:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    return chrome_options


def main(
    parse_url: str, dataset_path: str, postgres_url: str, cosine_sim_path: str
):
    browser = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"), options=get_options()
    )
    engine = create_engine(postgres_url)
    dataset_loader = DatasetLoaderImpl(browser)
    similarity_saver = CosineSimilaritySaver()
    base_saver = BaseDatasetSaver()
    db_saver = DatasetToDBSaverImpl(engine)

    base_processing_handler = BaseProcessingDatasetHandler(
        base_saver, dataset_path
    )
    similarity_handler = CalculateCosineSimilatiryDatasetHandler(
        similarity_saver, cosine_sim_path
    )
    db_handler = DatasetToDBHandler(db_saver)

    print("Getting data from URL...")
    try:
        data = dataset_loader.load(parse_url)
    except ParsingSiteNotAvailable:
        print("The service is not available")
        return
    print("Processing data...")
    base_processing_handler.handle(data)
    print("Calculating cosine similarity...")
    similarity_handler.handle(data)
    print("Inserting data to DB...")
    db_handler.handle(data)
    print("Done")


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
