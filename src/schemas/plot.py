from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.core.enums import DBEnum


class Plot(BaseModel):
    x: list[datetime] = []
    y: list[float] = []


class Plots(BaseModel):
    plots: list[Plot] = []
    time_to_get_data: float
    from_db: DBEnum


class RequestPlots(BaseModel):
    left_border: Optional[datetime]
    right_border: Optional[datetime]
    from_db: DBEnum
    downsample_to: int = 3000
