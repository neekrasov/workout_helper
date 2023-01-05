from dataclasses import dataclass, asdict, field
import os


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

    def get_dict(self):
        return asdict(self)
