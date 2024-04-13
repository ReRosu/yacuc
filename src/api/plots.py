from time import time
from datetime import timedelta
from fastapi import APIRouter, WebSocket

from src.schemas.plot import RequestPlots, Plots, Plot
from src.services.get_plots import get_plot


router = APIRouter(prefix="/plots")


@router.websocket(path="/ws")
async def plot(ws: WebSocket):
    await ws.accept()
    while True:
        from_ws_json = await ws.receive_json()
        from_ws: RequestPlots = RequestPlots.model_validate(from_ws_json)
        left_border = from_ws.left_border
        if not left_border is None:
            left_border = left_border.replace(tzinfo=None)
        right_border = from_ws.right_border
        if not right_border is None:
            right_border = right_border.replace(tzinfo=None)
        if not right_border is None and not left_border is None:
            delta_seconds: float = (right_border - left_border).total_seconds() / 3
            left_border -= timedelta(seconds=delta_seconds)
            right_border += timedelta(seconds=delta_seconds)
        start = time()
        data = get_plot(
            entity_id=1,
            metric_type=1,
            left_border=left_border,
            right_border=right_border,
            downsample_to=from_ws.downsample_to,
            db=from_ws.from_db
        )
        ttg = time() - start
        await ws.send_text(
            data=Plots(
                plots=[Plot(x=data["x"], y=data["y"])],
                time_to_get_data=ttg,
                from_db=from_ws.from_db,
            ).model_dump_json()
        )
