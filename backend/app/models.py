"""Pydantic models for request and response payloads."""
from __future__ import annotations

from pydantic import BaseModel


class Message(BaseModel):
    """Inbound chat request body."""

    question: str
