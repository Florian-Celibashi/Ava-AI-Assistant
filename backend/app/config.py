"""Configuration helpers for environment variables and static data."""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Resolve paths relative to the backend directory regardless of the runtime cwd.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables eagerly so downstream modules do not need to.
load_dotenv()


def get_env(name: str, default: Any | None = None) -> Any:
    """Return an environment variable, falling back to *default* when unset."""
    return os.getenv(name, default)


def get_openai_api_key() -> str | None:
    """Expose the OpenAI API key without altering variable names."""
    return get_env("OPENAI_API_KEY")


def get_openai_model() -> str:
    """Return the chat completion model to use for responses."""
    return get_env("OPENAI_MODEL", "gpt-5")


def get_frontend_origin() -> str:
    """Return the allowed frontend origin for CORS."""
    return get_env("FRONTEND_URL", "http://localhost:5173")


def _load_json(filename: str) -> Any:
    """Load JSON data stored alongside the backend codebase."""
    file_path = BASE_DIR / filename
    with file_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@lru_cache(maxsize=1)
def get_context() -> Any:
    """Load the assistant context description."""
    return _load_json("context.json")


@lru_cache(maxsize=1)
def get_memory_chunks() -> list[str]:
    """Load the long-term memory chunks used for retrieval."""
    return list(_load_json("memory_chunks.json"))
