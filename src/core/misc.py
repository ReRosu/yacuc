from clickhouse_connect import get_client

from src.core.settings import Settings

settings = Settings()

ch_client = get_client(
    host=settings.clickhouse_host,
    port=settings.clickhouse_port,
    username=settings.clickhouse_user,
    password=settings.clickhouse_password,
    database=settings.clickhouse_database,
)
