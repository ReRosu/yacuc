from psycopg import connect
from datetime import datetime
from typing import Optional

from src.core.misc import settings


def get_plot_from_pg(
    entity_id: Optional[int],
    metric_type: Optional[int],
    left_border: Optional[datetime],
    right_border: Optional[datetime],
    downsample_to: Optional[int] = 10000,
):
    result = {
        'x': [],
        'y': []
    }
    if left_border is None:
        left_border = datetime.min
    if right_border is None:
        right_border = datetime.max
    with connect(
        f"host={settings.postgres_host} port={settings.postgres_port} dbname={settings.postgres_db} user={settings.postgres_user} password={settings.postgres_password}"
    ) as conn:
        with conn.cursor() as curr:
            curr.execute(
                f"select * from lttb('{left_border.isoformat()}'::timestamp, '{right_border.isoformat()}'::timestamp, {entity_id}, {metric_type}, {downsample_to})"
            )
            for record in curr:
                result['x'].append(record[0])
                result['y'].append(record[1])

    
    return result
