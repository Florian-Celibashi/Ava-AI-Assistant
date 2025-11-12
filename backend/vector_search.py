"""Backward compatible import wrapper for vector search helpers."""
from app.services.vector_search import cosine_similarity, find_most_relevant_chunk

__all__ = ["cosine_similarity", "find_most_relevant_chunk"]
