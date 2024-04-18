import pandas as pd
from datetime import datetime, timedelta
from time import time
from math import sin


def generate_and_save_data(
    entity_id: int,
    left_border: datetime,
    right_border: datetime,
    time_step: timedelta,
    metric_type: int,
):
    if entity_id <= 0 or metric_type <= 0 or time_step.total_seconds() < 0:
        raise Exception("entity_id, metric_type, time_step  must be > 0")

    to_df: dict[str, list] = {
        "entity_id": entity_id,
        "dt": [],
        "metric_type": metric_type,
        "metric_value": [],
    }
    wdf = pd.read_csv("./csv_for_dbs/weather.csv")
    mean_temp = wdf["meantemp"].to_numpy()
    del wdf
    ct = 0
    dt = left_border
    idx = 0
    while dt <= right_border:
        to_df["dt"].append(dt)
        to_df["metric_value"].append(mean_temp[idx] + sin(time()))
        ct += 1
        dt += time_step
        idx += 1
        if idx == len(mean_temp):
            idx = 0
    print(f"Generated {ct} rows")

    filename = f"./csv_for_dbs/{entity_id}_{left_border}_{right_border}_{metric_type}_{datetime.utcnow()}.csv"
    print(filename)
    pd.DataFrame(to_df).to_csv(filename, index=False)


def main():
    generate_and_save_data(
        entity_id=1,
        left_border=datetime.utcnow() - timedelta(days=365 * 50),
        right_border=datetime.utcnow(),
        time_step=timedelta(hours=1),
        metric_type=1,
    )


if __name__ == "__main__":
    main()
