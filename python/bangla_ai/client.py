"""Main client that bundles all NLP modules."""

from openai import OpenAI
from .summarizer import Summarizer
from .qa import QA
from .sentiment import Sentiment


class BanglaAI:
    """Unified client for Bengali NLP tasks."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        client = OpenAI(api_key=api_key)
        self.summarize = Summarizer(client, model)
        self.qa = QA(client, model)
        self.sentiment = Sentiment(client, model)
