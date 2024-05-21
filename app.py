from typing import Any
import uvicorn
from litestar import Litestar

from controllers import create_router
from lib import settings

def create_app(**kwargs: Any) -> Litestar:
    return Litestar(
        debug=settings.DEBUG,
        route_handlers=create_router(),
        **kwargs,
    )

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
