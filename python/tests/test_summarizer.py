"""Summarizer tests — require OPENAI_API_KEY for openai backend."""

import os
import pytest
from bangla_ai import BanglaAI

SAMPLE = (
    "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। "
    "বাংলাদেশের মোট জনসংখ্যা প্রায় ১৭ কোটি। "
    "দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে। "
    "বাংলাদেশের অর্থনীতি মূলত গার্মেন্টস শিল্প ও কৃষির উপর নির্ভরশীল।"
)


@pytest.fixture
def openai_ai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return BanglaAI(backend="openai", api_key=key)


def test_summarize_openai(openai_ai):
    result = openai_ai.summarize(SAMPLE, max_sentences=2)
    assert isinstance(result, str) and len(result) > 0


def test_summarize_english_output(openai_ai):
    result = openai_ai.summarize(SAMPLE, max_sentences=2, language="english")
    assert isinstance(result, str) and len(result) > 0
