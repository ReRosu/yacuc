from datetime import datetime
from typing import Optional
from clickhouse_connect.driver.client import Client
import pandas as pd
import numpy as np


def get_plot_from_clickhouse(
    ch_client: Client,
    entity_id: Optional[int],
    metric_type: Optional[int],
    left_border: Optional[datetime],
    right_border: Optional[datetime],
    downsample_to: Optional[int] = 10000,
):
    left_border_check = (
        f"dt >= toDateTime64('{left_border.isoformat()}', 3) and "
        if left_border
        else ""
    )
    right_border_check = (
        f"dt <= toDateTime64('{right_border.isoformat()}', 3) and "
        if right_border
        else ""
    )
    entity_id_check = f"entity_id = {entity_id} and " if entity_id else ""
    metric_type_check = f"metric_type = {metric_type} " if metric_type else ""

    count_query = (
        "select count(dt) as cnt from metrics_data where "
        + f"{left_border_check}{right_border_check}{entity_id_check}{metric_type_check}"
    )

    count_: int = ch_client.query(count_query).first_item["cnt"]

    if count_ == 0:
        return {"x": np.array([]), "y": np.array([])}

    sample_k: float = 1

    if count_ > downsample_to:
        sample_k = downsample_to / count_

    get_data_q = (
        f"select dt, metric_value from metrics_data sample {sample_k} where "
        + f"{left_border_check}{right_border_check}{entity_id_check}{metric_type_check}"
        + "order by dt"
    )

    data: pd.DataFrame = ch_client.query_df(get_data_q)
    return {"x": data["dt"].to_numpy(), "y": data["metric_value"].to_numpy()}


def setup_clickhouse(ch_client: Client):
    query = """
        create table if not exists metrics_data(
            entity_id UInt32,
            dt DateTime64(3),
            metric_type UInt32,
            metric_value Float64
        ) ENGINE = MergeTree()
        partition by metric_type
        order by (entity_id, cityHash64(dt), metric_type)
        sample by cityHash64(dt)
    """
    ch_client.command(query)
