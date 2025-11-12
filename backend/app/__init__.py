"""Ava AI Assistant FastAPI application factory."""

from .factory import create_app

# Instantiate the FastAPI application at import time for ASGI servers.
app = create_app()

__all__ = ["app", "create_app"]
