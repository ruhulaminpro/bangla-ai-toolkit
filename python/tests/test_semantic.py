"""Tests for embeddings, semantic search, and NER plumbing.

These use a fake backend so no API key or model download is needed — they
verify the client wiring and the pure-Python similarity math.
"""

import math
import pytest

from bangla_ai import BanglaAI
from bangla_ai.backends.base import Backend
from bangla_ai.semantic import cosine_similarity, rank_by_similarity


class FakeBackend(Backend):
    """Backend that returns canned vectors/entities for testing."""

    def __init__(self, vectors):
        self._vectors = vectors

    def summarize(self, text, *, max_sentences=3, language="bengali"):
        return ""

    def qa(self, context, question, *, language="bengali"):
        return ""

    def sentiment(self, text):
        return {"label": "neutral", "score": 0.0, "explanation": ""}

    def embed(self, texts):
        return [self._vectors[t] for t in texts]

    def ner(self, text):
        return [{"text": "ঢাকা", "type": "LOC", "score": 0.99}]


class MinimalBackend(Backend):
    """Implements only the three required tasks — no ner/embed."""

    def summarize(self, text, *, max_sentences=3, language="bengali"):
        return ""

    def qa(self, context, question, *, language="bengali"):
        return ""

    def sentiment(self, text):
        return {}


# ── cosine ────────────────────────────────────────────────────────────────────

def test_cosine_identical():
    assert cosine_similarity([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_cosine_orthogonal():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_zero_vector():
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_rank_orders_by_similarity():
    q = [1.0, 0.0]
    docs = [[0.0, 1.0], [1.0, 0.1], [-1.0, 0.0]]
    ranked = rank_by_similarity(q, docs)
    assert ranked[0][0] == 1          # the [1.0, 0.1] doc is closest
    assert ranked[-1][0] == 2         # the opposite vector is last


# ── client wiring ───────────────────────────────────────────────────────────

def test_semantic_search_ranks_documents():
    vectors = {
        "রাজধানী": [1.0, 0.0],
        "ঢাকা বাংলাদেশের রাজধানী": [1.0, 0.1],
        "আমি ভাত খাই": [0.0, 1.0],
    }
    ai = BanglaAI(backend=FakeBackend(vectors))
    results = ai.semantic_search(
        "রাজধানী", ["ঢাকা বাংলাদেশের রাজধানী", "আমি ভাত খাই"], top_k=2
    )
    assert results[0]["document"] == "ঢাকা বাংলাদেশের রাজধানী"
    assert results[0]["index"] == 0
    assert results[0]["score"] >= results[1]["score"]


def test_embed_accepts_single_string():
    ai = BanglaAI(backend=FakeBackend({"x": [0.1, 0.2]}))
    assert ai.embed("x") == [[0.1, 0.2]]


def test_ner_passthrough():
    ai = BanglaAI(backend=FakeBackend({}))
    entities = ai.ner("ঢাকা একটি শহর")
    assert entities[0]["type"] == "LOC"


def test_unsupported_capability_raises():
    ai = BanglaAI(backend=MinimalBackend())
    with pytest.raises(NotImplementedError):
        ai.ner("ঢাকা")
    with pytest.raises(NotImplementedError):
        ai.embed("ঢাকা")
