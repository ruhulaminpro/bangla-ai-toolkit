"""Vector similarity helpers — pure Python, zero dependencies.

Used by ``BanglaAI.semantic_search`` to rank documents against a query once a
backend has produced embeddings, but usable standalone with any vectors.
"""

from __future__ import annotations
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors. Returns 0.0 if either
    vector is all zeros."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def rank_by_similarity(
    query_vec: list[float], doc_vecs: list[list[float]]
) -> list[tuple[int, float]]:
    """Rank documents by cosine similarity to the query.

    Returns ``(index, score)`` pairs sorted by score, highest first.
    """
    sims = [cosine_similarity(query_vec, d) for d in doc_vecs]
    order = sorted(range(len(doc_vecs)), key=lambda i: sims[i], reverse=True)
    return [(i, sims[i]) for i in order]
