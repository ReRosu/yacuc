from datetime import datetime
from typing import Optional

from src.core.enums import DBEnum
from src.core.misc import ch_client, pg_connect
from src.entities.plot import PlotFromDB
from src.services.clickhouse import get_plot_from_clickhouse
from src.services.postgresql import get_plot_from_pg


def get_plot(
    left_border: Optional[datetime], right_border: Optional[datetime], entity_id: int, metric_type: int, downsample_to: int, db: DBEnum
) -> PlotFromDB: 
    match db:
        case DBEnum.clickhouse:
            ch_plot = get_plot_from_clickhouse(
                ch_client=ch_client,
                entity_id=entity_id,
                metric_type=metric_type,
                left_border=left_border,
                right_border=right_border,
                downsample_to=downsample_to
            )
            return PlotFromDB(
                x=ch_plot['x'].tolist(),
                y=ch_plot['y'].tolist()
            )
        case DBEnum.postgresql:
            pg_plot = get_plot_from_pg(
                pg_connect=pg_connect,
                entity_id=entity_id,
                metric_type=metric_type,
                left_border=left_border,
                right_border=right_border,
                downsample_to=downsample_to
            )
            return PlotFromDB(
                **pg_plot
            )
        case _:
            return PlotFromDB(
                x=[],
                y=[]
            )
