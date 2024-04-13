from uvicorn import run
from uvicorn.config import LOGGING_CONFIG

from src.core.misc import settings


def main():
    LOGGING_CONFIG["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    run("src.core.asgi:app", port=8080, reload=settings.reload)


if __name__ == "__main__":
    main()
