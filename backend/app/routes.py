"""API routes for the Ava backend."""
from __future__ import annotations

from fastapi import APIRouter

from .models import Message
from .services.chat import fetch_answer

router = APIRouter()


@router.get("/")
def read_root() -> dict[str, str]:
    """Health check route used by the frontend ping."""
    return {"message": "Ava AI Assistant backend is live."}


@router.post("/ask")
async def ask_ava(msg: Message) -> dict[str, str]:
    """Proxy chat questions to the OpenAI-backed assistant."""
    return fetch_answer(msg.question)
