"""Backward compatible import wrapper for embedding helpers."""
from app.services.embeddings import generate_embedding

__all__ = ["generate_embedding"]
