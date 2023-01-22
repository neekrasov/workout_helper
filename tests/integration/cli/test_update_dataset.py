import os.path
from sqlalchemy import create_engine

from app.presentation.cli.update_dataset import main
from app.settings import Settings


def test_update_dataset(settings: Settings):
    main(
        settings.dataset.parse_url,
        settings.dataset.dataset_path,
        settings.postgres.postgres_url.replace("+asyncpg", ""),
        settings.dataset.recomm_cosine_sim_path,
    )

    engine = create_engine(
        settings.postgres.postgres_url.replace("+asyncpg", "")
    )

    with engine.begin() as conn:
        result = conn.execute("SELECT COUNT(*) FROM sports_grounds")
        count = result.fetchone()[0]
        assert count > 3000

    assert os.path.exists(settings.dataset.dataset_path)
