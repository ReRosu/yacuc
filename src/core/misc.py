from clickhouse_connect import get_client
from clickhouse_connect.driver.client import Client
from psycopg import connect, Connection

from src.core.settings import Settings

settings = Settings()

ch_client: Client = get_client(
    host=settings.clickhouse_host,
    port=settings.clickhouse_port,
    username=settings.clickhouse_user,
    password=settings.clickhouse_password,
    database=settings.clickhouse_database,
)
pg_connect: Connection = connect(
        f"host={settings.postgres_host} port={settings.postgres_port} dbname={settings.postgres_db} user={settings.postgres_user} password={settings.postgres_password}"
    )