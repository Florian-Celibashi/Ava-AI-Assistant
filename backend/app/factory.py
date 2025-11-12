"""Application factory and middleware configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_frontend_origin
from .routes import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[get_frontend_origin()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app
