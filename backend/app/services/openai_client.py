"""Thin wrappers around OpenAI's chat completion API."""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

from openai import OpenAI

from ..config import get_openai_api_key


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    """Instantiate the OpenAI client once per process."""
    return OpenAI(api_key=get_openai_api_key())


def create_chat_completion(messages: List[Dict[str, str]], model: str) -> str:
    """Request a chat completion and return the assistant's reply text."""
    response = _get_client().chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content
