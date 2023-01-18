import os.path
from sqlalchemy import create_engine

from app.presentation.cli.update_dataset import main
from app.settings import Settings


def test_update_dataset(settings: Settings):
    main()

    engine = create_engine(
        settings.postgres.postgres_url.replace("+asyncpg", "")
    )

    with engine.begin() as conn:
        result = conn.execute("SELECT COUNT(*) FROM sports_grounds")
        count = result.fetchone()[0]
        assert count > 3000

    assert os.path.exists(settings.dataset.dataset_path)
