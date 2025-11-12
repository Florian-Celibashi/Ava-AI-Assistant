"""Utilities for preparing contextual data and embeddings."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Sequence, Tuple

from .config import get_context, get_memory_chunks
from .services.embeddings import generate_embedding


@dataclass(frozen=True)
class StoredChunk:
    """Container for a context chunk and its embedding."""

    text: str
    embedding: Sequence[float]


@lru_cache(maxsize=1)
def get_stored_chunks() -> Tuple[StoredChunk, ...]:
    """Generate embeddings for each stored memory chunk once per process."""
    return tuple(
        StoredChunk(text=chunk, embedding=generate_embedding(chunk))
        for chunk in get_memory_chunks()
    )


def iter_stored_chunks() -> Iterable[StoredChunk]:
    """Iterate over the cached stored chunks."""
    return get_stored_chunks()


@lru_cache(maxsize=1)
def get_system_message() -> dict[str, str]:
    """Construct the system prompt using the loaded context."""
    context = get_context()
    return {
        "role": "system",
        "content": (
            """\
You are Ava, an AI assistant created by Florian. Your purpose is to represent him professionally to recruiters and potential employers.

You have access to Florian’s resume, experience, and project history. Use this context to answer questions accurately, clearly, and helpfully:

{context}

Do not answer general questions unrelated to Florian (e.g., news, current events, random trivia). If asked something outside your scope, politely explain that your purpose is to represent Florian and guide the conversation back to relevant topics.
Always respond in a helpful, confident, and professional tone. When asked about the 'Ava AI Assistant' project, remember you are that project.
Keep responses concise and directly relevant to Florian's professional context. Limit answers to a few sentences while preserving necessary detail.
""".strip()
        ).format(context=context)
    }
