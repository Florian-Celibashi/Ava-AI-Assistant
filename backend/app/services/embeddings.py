"""Embedding helpers that wrap the OpenAI client."""
from __future__ import annotations

from functools import lru_cache
from typing import Sequence

from openai import OpenAI

from ..config import get_openai_api_key


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    """Instantiate a single OpenAI client per process."""
    return OpenAI(api_key=get_openai_api_key())


def generate_embedding(text: str, model: str = "text-embedding-3-small") -> Sequence[float]:
    """Return an embedding vector for *text* using the configured model."""
    response = _get_client().embeddings.create(input=[text], model=model)
    return response.data[0].embedding
