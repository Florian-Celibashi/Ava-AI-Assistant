"""Service-layer utilities for the Ava backend."""

from .chat import build_chat_messages, fetch_answer
from .embeddings import generate_embedding
from .vector_search import cosine_similarity, find_most_relevant_chunk

__all__ = [
    "build_chat_messages",
    "cosine_similarity",
    "fetch_answer",
    "find_most_relevant_chunk",
    "generate_embedding",
]
