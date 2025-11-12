"""Chat orchestration helpers for the Ava backend."""
from __future__ import annotations

import logging
from typing import Dict, List

from ..config import get_openai_model
from ..data import get_system_message, iter_stored_chunks
from .openai_client import create_chat_completion
from .vector_search import find_most_relevant_chunk

logger = logging.getLogger(__name__)


def build_chat_messages(question: str) -> List[Dict[str, str]]:
    """Construct the OpenAI chat payload for the provided *question*."""
    messages: List[Dict[str, str]] = [get_system_message()]
    relevant_chunk = find_most_relevant_chunk(question, iter_stored_chunks())
    if relevant_chunk:
        messages.append({"role": "system", "content": f"Relevant fact: {relevant_chunk}"})
    messages.append({"role": "user", "content": question})
    return messages


def fetch_answer(question: str) -> Dict[str, str]:
    """Return the assistant's response payload for the given question."""
    try:
        messages = build_chat_messages(question)
        response_text = create_chat_completion(messages, get_openai_model())
        return {"answer": response_text}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("OpenAI API Error: %s", exc)
        return {"error": str(exc)}
