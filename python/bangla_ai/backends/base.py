"""Abstract backend interface.

The three core tasks (summarize, qa, sentiment) are abstract — every backend
must implement them. ``ner`` and ``embed`` are optional capabilities with a
default that raises ``NotImplementedError``, so a custom backend can implement
only what it supports without breaking.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    def summarize(self, text: str, *, max_sentences: int = 3, language: str = "bengali") -> str: ...

    @abstractmethod
    def qa(self, context: str, question: str, *, language: str = "bengali") -> str: ...

    @abstractmethod
    def sentiment(self, text: str) -> dict[str, str | float]: ...

    def ner(self, text: str) -> list[dict[str, str | float]]:
        """Extract named entities. Returns a list of
        ``{"text": ..., "type": ..., "score": ...}`` dicts.
        """
        raise NotImplementedError(f"{type(self).__name__} does not support ner()")

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return an embedding vector for each input string."""
        raise NotImplementedError(f"{type(self).__name__} does not support embed()")
