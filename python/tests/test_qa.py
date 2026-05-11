"""QA tests — require OPENAI_API_KEY for openai backend."""

import os
import pytest
from bangla_ai import BanglaAI

CONTEXT = (
    "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন। "
    "তিনি একজন বিখ্যাত বাংলা কবি ও ঔপন্যাসিক। "
    "১৯১৩ সালে তিনি সাহিত্যে নোবেল পুরস্কার লাভ করেন।"
)


@pytest.fixture
def openai_ai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return BanglaAI(backend="openai", api_key=key)


def test_qa_bengali(openai_ai):
    answer = openai_ai.qa(CONTEXT, "রবীন্দ্রনাথ ঠাকুর কোন পুরস্কার পেয়েছিলেন?")
    assert isinstance(answer, str) and len(answer) > 0


def test_qa_english_output(openai_ai):
    answer = openai_ai.qa(CONTEXT, "When was Rabindranath Tagore born?", language="english")
    assert "1861" in answer
