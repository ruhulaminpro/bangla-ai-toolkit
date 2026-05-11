"""bangla-ai-toolkit: AI-powered NLP library for the Bengali language."""

from .summarizer import Summarizer
from .qa import QA
from .sentiment import Sentiment
from .client import BanglaAI

__version__ = "0.1.0"
__all__ = ["BanglaAI", "Summarizer", "QA", "Sentiment"]
