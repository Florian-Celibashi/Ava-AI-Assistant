from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
from typing import Any, Iterable, List


TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9+#\-.]*")


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _tokenize(value: str) -> List[str]:
    return TOKEN_PATTERN.findall(value.lower())


def _flatten_context(data: Any, prefix: str = "") -> Iterable[str]:
    if isinstance(data, dict):
        for key, value in data.items():
            nested_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from _flatten_context(value, nested_prefix)
        return
    if isinstance(data, list):
        for idx, value in enumerate(data):
            nested_prefix = f"{prefix}[{idx}]"
            yield from _flatten_context(value, nested_prefix)
        return
    if data is None:
        return
    scalar = str(data).strip()
    if not scalar:
        return
    yield _normalize_text(f"{prefix}: {scalar}" if prefix else scalar)


def _build_chunks(lines: List[str], *, target_chars: int = 650, overlap_lines: int = 1) -> List[str]:
    if not lines:
        return []

    chunks: List[str] = []
    current: List[str] = []

    for line in lines:
        candidate = current + [line]
        if current and len("\n".join(candidate)) > target_chars:
            chunks.append("\n".join(current))
            current = current[-overlap_lines:] if overlap_lines else []
        current.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks


@dataclass(frozen=True)
class SearchHit:
    text: str
    score: float


class ContextIndex:
    def __init__(self, chunks: List[str]):
        self.chunks = chunks
        self._doc_terms = [Counter(_tokenize(chunk)) for chunk in chunks]
        self._doc_lengths = [sum(counter.values()) for counter in self._doc_terms]
        self._avg_doc_length = (
            sum(self._doc_lengths) / len(self._doc_lengths)
            if self._doc_lengths
            else 1.0
        )
        self._idf = self._compute_idf()

    def _compute_idf(self) -> dict[str, float]:
        doc_count = max(len(self._doc_terms), 1)
        term_document_frequency: Counter[str] = Counter()

        for terms in self._doc_terms:
            for term in terms:
                term_document_frequency[term] += 1

        idf: dict[str, float] = {}
        for term, df in term_document_frequency.items():
            idf[term] = math.log1p((doc_count - df + 0.5) / (df + 0.5))

        return idf

    def search(self, query: str, *, top_k: int = 4) -> List[SearchHit]:
        query = _normalize_text(query)
        if not query or not self.chunks:
            return []

        terms = _tokenize(query)
        if not terms:
            return []

        scores: List[tuple[int, float]] = []
        k1 = 1.4
        b = 0.75
        query_lower = query.lower()

        for idx, doc_terms in enumerate(self._doc_terms):
            doc_len = self._doc_lengths[idx] or 1
            score = 0.0

            for term in terms:
                term_frequency = doc_terms.get(term, 0)
                if term_frequency == 0:
                    continue

                idf = self._idf.get(term, 0.0)
                denominator = term_frequency + k1 * (1 - b + b * (doc_len / self._avg_doc_length))
                score += idf * ((term_frequency * (k1 + 1)) / denominator)

            if query_lower in self.chunks[idx].lower():
                score += 0.8

            if score > 0:
                scores.append((idx, score))

        scores.sort(key=lambda item: item[1], reverse=True)
        top_scores = scores[:top_k]
        return [SearchHit(text=self.chunks[idx], score=score) for idx, score in top_scores]

    def fallback(self, *, top_k: int = 4) -> List[SearchHit]:
        if not self.chunks or top_k <= 0:
            return []
        # Keep deterministic and pull early profile chunks in source order.
        selected = self.chunks[:top_k]
        return [SearchHit(text=chunk, score=0.01) for chunk in selected]


def build_context_index(context_path: Path) -> ContextIndex:
    with context_path.open("r", encoding="utf-8") as handle:
        context_obj = json.load(handle)

    lines = list(_flatten_context(context_obj))
    chunks = _build_chunks(lines)
    return ContextIndex(chunks)
