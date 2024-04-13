import os
import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR: str = str(pathlib.Path(__file__).parent.parent.parent)


class Settings(BaseSettings):
    api_prefix: str = "/api"

    reload: bool = False

    clickhouse_host: str
    clickhouse_port: int
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_database: str
    postgres_db: str
    postgres_port: int
    postgres_host: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"))
