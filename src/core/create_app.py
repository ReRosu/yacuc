from fastapi import APIRouter, FastAPI
from src.api import pages, plots


def create_app() -> FastAPI:
    app = FastAPI()

    api_router = APIRouter(prefix="/api")
    api_router.include_router(plots.router)
    app.include_router(api_router)
    app.include_router(pages.router)

    return app
