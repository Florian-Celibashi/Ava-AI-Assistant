from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Tuple

from dotenv import load_dotenv


def _parse_int(name: str, default: int, *, minimum: int = 1, maximum: int = 100_000) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        parsed = int(raw)
    except ValueError:
        return default
    return max(minimum, min(parsed, maximum))


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    frontend_origins: Tuple[str, ...]
    max_context_chunks: int
    max_history_messages: int
    response_cache_ttl_seconds: int
    response_cache_max_items: int
    openai_timeout_seconds: int


def get_settings() -> Settings:
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").strip()
    extra_origins = os.getenv("FRONTEND_URLS", "")
    parsed_extra_origins = [origin.strip() for origin in extra_origins.split(",") if origin.strip()]
    frontend_origins = tuple(dict.fromkeys([frontend_url, *parsed_extra_origins]))

    return Settings(
        openai_api_key=openai_api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
        frontend_origins=frontend_origins,
        max_context_chunks=_parse_int("MAX_CONTEXT_CHUNKS", 4, minimum=1, maximum=12),
        max_history_messages=_parse_int("MAX_HISTORY_MESSAGES", 8, minimum=0, maximum=20),
        response_cache_ttl_seconds=_parse_int("RESPONSE_CACHE_TTL_SECONDS", 600, minimum=0, maximum=86_400),
        response_cache_max_items=_parse_int("RESPONSE_CACHE_MAX_ITEMS", 256, minimum=1, maximum=10_000),
        openai_timeout_seconds=_parse_int("OPENAI_TIMEOUT_SECONDS", 45, minimum=5, maximum=300),
    )
