from enum import Enum


class DBEnum(str, Enum):
    clickhouse = "clickhouse"
    postgresql = "postgresql"
    timescaledb = "timescaledb"
