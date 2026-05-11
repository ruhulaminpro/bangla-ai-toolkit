"""Tests for Summarizer — require OPENAI_API_KEY env var."""

import os
import pytest
from bangla_ai import BanglaAI

SAMPLE_TEXT = (
    "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। "
    "বাংলাদেশের মোট জনসংখ্যা প্রায় ১৭ কোটি। "
    "দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে। "
    "বাংলাদেশের অর্থনীতি মূলত গার্মেন্টস শিল্প ও কৃষির উপর নির্ভরশীল।"
)


@pytest.fixture
def ai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return BanglaAI(api_key=api_key)


def test_summarize_bengali(ai):
    result = ai.summarize(SAMPLE_TEXT, max_sentences=2)
    assert isinstance(result, str)
    assert len(result) > 0


def test_summarize_english_output(ai):
    result = ai.summarize(SAMPLE_TEXT, max_sentences=2, language="english")
    assert isinstance(result, str)
    assert len(result) > 0
