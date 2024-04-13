from typing import TypedDict
from datetime import datetime


class PlotFromDB(TypedDict):
    x: list[datetime]
    y: list[float]
