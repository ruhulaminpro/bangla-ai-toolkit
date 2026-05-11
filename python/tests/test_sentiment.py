"""Sentiment tests — require OPENAI_API_KEY for openai backend."""

import os
import pytest
from bangla_ai import BanglaAI


@pytest.fixture
def openai_ai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return BanglaAI(backend="openai", api_key=key)


def test_positive(openai_ai):
    r = openai_ai.sentiment("আজকের দিনটি অসাধারণ ছিল! আমি খুব খুশি।")
    assert r["label"] == "positive"
    assert 0.0 <= r["score"] <= 1.0


def test_negative(openai_ai):
    r = openai_ai.sentiment("আজকে সব কিছু খুব খারাপ হয়েছে।")
    assert r["label"] == "negative"


def test_result_shape(openai_ai):
    r = openai_ai.sentiment("আজকে সকাল দশটায় মিটিং আছে।")
    assert {"label", "score", "explanation"} <= r.keys()
