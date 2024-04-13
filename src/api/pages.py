from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import aiofiles


router = APIRouter()


@router.get("/plots")
async def plots_page():
    async with aiofiles.open("./site/plots.html") as page:
        return HTMLResponse(await page.read())
