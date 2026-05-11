"""Tests for Sentiment — require OPENAI_API_KEY env var."""

import os
import pytest
from bangla_ai import BanglaAI


@pytest.fixture
def ai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return BanglaAI(api_key=api_key)


def test_positive_sentiment(ai):
    result = ai.sentiment("আজকের দিনটি অসাধারণ ছিল! আমি খুব খুশি।")
    assert result["label"] == "positive"
    assert 0.0 <= result["score"] <= 1.0
    assert "explanation" in result


def test_negative_sentiment(ai):
    result = ai.sentiment("আজকে সব কিছু খুব খারাপ হয়েছে। আমি মোটেও খুশি নই।")
    assert result["label"] == "negative"
    assert 0.0 <= result["score"] <= 1.0


def test_neutral_sentiment(ai):
    result = ai.sentiment("আজকে সকাল দশটায় মিটিং আছে।")
    assert result["label"] in ("positive", "negative", "neutral")
    assert isinstance(result["score"], float)
