from __future__ import annotations

from collections import OrderedDict
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
import time
from typing import Dict, Literal, Optional, Sequence, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import APIConnectionError, APIError, APITimeoutError, AsyncOpenAI, RateLimitError
from pydantic import BaseModel, Field, field_validator

try:
    from .context_index import build_context_index
    from .settings import Settings, get_settings
except ImportError:  # pragma: no cover - supports direct module execution
    from context_index import build_context_index
    from settings import Settings, get_settings


SYSTEM_PROMPT = """
You are Ava, Florian Celibashi's professional AI assistant.

Your job:
- Represent Florian clearly and professionally.
- Answer using only provided context snippets and conversation history.
- If a question is outside Florian-related scope, say that Ava is focused on Florian's background and guide back.
- Keep answers concise and concrete (2-5 short paragraphs max).
- Prefer factual statements over generic marketing language.
""".strip()


@dataclass
class CachedAnswer:
    answer: str
    sources: list[str]
    expires_at: float


class AnswerCache:
    def __init__(self, max_items: int, ttl_seconds: int):
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self._items: OrderedDict[str, CachedAnswer] = OrderedDict()

    def get(self, key: str) -> Optional[CachedAnswer]:
        now = time.monotonic()
        item = self._items.get(key)
        if item is None:
            return None
        if item.expires_at <= now:
            self._items.pop(key, None)
            return None
        self._items.move_to_end(key)
        return item

    def set(self, key: str, answer: str, sources: list[str]) -> None:
        expires_at = time.monotonic() + self.ttl_seconds
        self._items[key] = CachedAnswer(answer=answer, sources=sources, expires_at=expires_at)
        self._items.move_to_end(key)
        while len(self._items) > self.max_items:
            self._items.popitem(last=False)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2_000)

    @field_validator("content")
    @classmethod
    def trim_content(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Message content cannot be empty.")
        return stripped


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2_000)
    history: list[ChatMessage] = Field(default_factory=list)

    @field_validator("question")
    @classmethod
    def trim_question(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Question cannot be empty.")
        return stripped


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    cached: bool = False
    latency_ms: int


def _history_to_messages(history: Sequence[ChatMessage], max_messages: int) -> list[dict[str, str]]:
    if max_messages <= 0:
        return []
    trimmed = history[-max_messages:]
    return [{"role": msg.role, "content": msg.content} for msg in trimmed]


def _normalize_cache_key(req: AskRequest, max_history_messages: int) -> str:
    history = _history_to_messages(req.history, max_history_messages)
    return f"{req.question.lower().strip()}::{history}"


def _extract_answer(response: object) -> str:
    try:
        content = response.choices[0].message.content  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover - defensive guard
        raise RuntimeError("OpenAI returned an unexpected response format.") from exc

    if isinstance(content, str):
        answer = content.strip()
        if answer:
            return answer
        return "I do not have enough context to answer that yet."

    if isinstance(content, list):
        text_parts: list[str] = []
        for part in content:
            if isinstance(part, dict):
                maybe_text = part.get("text")
                if isinstance(maybe_text, str):
                    text_parts.append(maybe_text)
            else:
                maybe_text = getattr(part, "text", None)
                if isinstance(maybe_text, str):
                    text_parts.append(maybe_text)
        joined = "\n".join(part.strip() for part in text_parts if part and part.strip()).strip()
        if joined:
            return joined
        return "I do not have enough context to answer that yet."

    return str(content).strip() or "I do not have enough context to answer that yet."


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    context_index = build_context_index(Path(__file__).resolve().parent / "context.json")
    openai_client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout_seconds)
    response_cache = AnswerCache(
        max_items=settings.response_cache_max_items,
        ttl_seconds=settings.response_cache_ttl_seconds,
    )

    app.state.settings = settings
    app.state.context_index = context_index
    app.state.openai_client = openai_client
    app.state.response_cache = response_cache
    yield


app = FastAPI(lifespan=lifespan)


def _cors_origins(settings: Settings) -> list[str]:
    return list(settings.frontend_origins)


try:
    _settings_for_cors = get_settings()
except RuntimeError:
    # Keep local startup debuggable: CORS falls back to localhost while env gets fixed.
    _settings_for_cors = Settings(
        openai_api_key="",
        openai_model="gpt-4o-mini",
        frontend_origins=("http://localhost:5173",),
        max_context_chunks=4,
        max_history_messages=8,
        response_cache_ttl_seconds=600,
        response_cache_max_items=256,
        openai_timeout_seconds=45,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(_settings_for_cors),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Ava AI Assistant backend is live."}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> Dict[str, Union[str, int]]:
    chunk_count = len(app.state.context_index.chunks)
    return {"status": "ready", "context_chunks": chunk_count}


@app.post("/ask", response_model=AskResponse)
async def ask_ava(msg: AskRequest) -> AskResponse:
    settings: Settings = app.state.settings
    context_index = app.state.context_index
    openai_client: AsyncOpenAI = app.state.openai_client
    response_cache: AnswerCache = app.state.response_cache

    started_at = time.perf_counter()
    cache_key = _normalize_cache_key(msg, settings.max_history_messages)
    cached = response_cache.get(cache_key)
    if cached:
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        return AskResponse(
            answer=cached.answer,
            sources=cached.sources,
            cached=True,
            latency_ms=elapsed_ms,
        )

    hits = context_index.search(msg.question, top_k=settings.max_context_chunks)
    source_chunks = [hit.text for hit in hits]
    context_block = "\n\n---\n\n".join(source_chunks) if source_chunks else "No context snippets matched."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Context snippets:\n{context_block}"},
        *_history_to_messages(msg.history, settings.max_history_messages),
        {"role": "user", "content": msg.question},
    ]

    try:
        completion = await openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
        )
    except (RateLimitError, APITimeoutError, APIConnectionError) as exc:
        raise HTTPException(status_code=503, detail=f"OpenAI service unavailable: {exc}") from exc
    except APIError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected backend error: {exc}") from exc

    answer = _extract_answer(completion)
    response_cache.set(cache_key, answer=answer, sources=source_chunks)
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)

    return AskResponse(
        answer=answer,
        sources=source_chunks,
        cached=False,
        latency_ms=elapsed_ms,
    )
