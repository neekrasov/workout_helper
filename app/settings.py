import os
from dataclasses import dataclass, asdict, field


@dataclass
class PGSettings:
    postgres_user: str = field(init=False)
    postgres_password: str = field(init=False)
    postgres_host: str = field(init=False)
    postgres_db: str = field(init=False)
    postgres_port: str = field(init=False)
    postgres_url: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_host = os.getenv("POSTGRES_HOST")
        self.postgres_db = os.getenv("POSTGRES_DB")
        self.postgres_port = os.getenv("POSTGRES_PORT")
        self.postgres_url = (
            "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
                user=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                db=self.postgres_db,
            )
        )


@dataclass
class RedisSettings:
    redis_host: str = field(init=False)
    redis_port: str = field(init=False)
    redis_url: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = os.getenv("REDIS_PORT")
        self.redis_url = "redis://{host}:{port}".format(
            host=self.redis_host, port=self.redis_port
        )


@dataclass
class DatasetSettings:
    dataset_path: str = field(init=False)
    recomm_cosine_sim_path: str = field(init=False)
    parse_url: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.dataset_path = os.getenv("DATASET_PATH")
        self.recomm_cosine_sim_path = os.getenv("RECOMM_COSINE_SIM_PATH")
        self.parse_url = os.getenv("PARSE_URL")


@dataclass
class TestUserSettings:
    id: str = field(init=False)
    username: str = field(init=False)
    password: str = field(init=False)
    email: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.id = os.getenv("FIRST_USER_ID")
        self.username = os.getenv("FIRST_USER_USERNAME")
        self.password = os.getenv("FIRST_USER_PASSWORD")
        self.email = os.getenv("FIRST_USER_EMAIL")


@dataclass
class Settings:
    title: str = field(init=False)
    description: str = field(init=False)
    version: str = field(init=False)
    logging_level: str = field(init=False)
    secret_key: str = field(init=False)
    show_error_details: bool = field(init=False)
    debug: bool = field(init=False)
    api_version: str = field(init=False, default="v1")
    token_expiration: int = field(init=False, default=3600)

    postgres: PGSettings = field(init=False, default_factory=PGSettings)
    redis: RedisSettings = field(init=False, default_factory=RedisSettings)
    dataset: DatasetSettings = field(
        init=False, default_factory=DatasetSettings
    )
    test_user: TestUserSettings = field(
        init=False, default_factory=TestUserSettings
    )

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.title = os.getenv("APP_TITLE")
        self.description = os.getenv("APP_DESCRIPTION")
        self.secret_key = os.getenv("APP_SECRET_KEY")
        self.logging_level = os.getenv("APP_LOGGING_LEVEL")
        self.show_error_details = os.getenv("APP_SHOW_ERROR_DETAILS")
        self.version = os.getenv("APP_VERSION")
        self.debug = os.getenv("APP_DEBUG")
        self.token_expiration = os.getenv("APP_TOKEN_EXPIRATION")
        self.recomm_cosine_sim_path = os.getenv("APP_RECOMM_COSINE_SIM_PATH")

    def get_dict(self):
        return asdict(self)
