"""Tests for QA — require OPENAI_API_KEY env var."""

import os
import pytest
from bangla_ai import BanglaAI

CONTEXT = (
    "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন। "
    "তিনি একজন বিখ্যাত বাংলা কবি, ঔপন্যাসিক এবং দার্শনিক। "
    "১৯১৩ সালে তিনি সাহিত্যে নোবেল পুরস্কার লাভ করেন। "
    "গীতাঞ্জলি তাঁর সবচেয়ে বিখ্যাত কাব্যগ্রন্থ।"
)


@pytest.fixture
def ai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return BanglaAI(api_key=api_key)


def test_qa_bengali(ai):
    answer = ai.qa(CONTEXT, "রবীন্দ্রনাথ ঠাকুর কোন পুরস্কার পেয়েছিলেন?")
    assert isinstance(answer, str)
    assert len(answer) > 0


def test_qa_english_output(ai):
    answer = ai.qa(CONTEXT, "When was Rabindranath Tagore born?", language="english")
    assert isinstance(answer, str)
    assert "1861" in answer
