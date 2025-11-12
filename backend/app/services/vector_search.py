"""Vector search helpers for selecting relevant context."""
from __future__ import annotations

from typing import Iterable, Optional, Sequence

import numpy as np

from .embeddings import generate_embedding
from ..data import StoredChunk


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    a_vec = np.array(a)
    b_vec = np.array(b)
    denominator = np.linalg.norm(a_vec) * np.linalg.norm(b_vec)
    if denominator == 0:
        return 0.0
    return float(np.dot(a_vec, b_vec) / denominator)


def find_most_relevant_chunk(
    user_input: str, stored_chunks: Iterable[StoredChunk]
) -> Optional[str]:
    """Return the chunk text that best matches the provided *user_input*."""
    input_vector = generate_embedding(user_input)
    best_score = -1.0
    best_chunk: Optional[str] = None
    for chunk in stored_chunks:
        score = cosine_similarity(input_vector, chunk.embedding)
        if score > best_score:
            best_score = score
            best_chunk = chunk.text
    return best_chunk
