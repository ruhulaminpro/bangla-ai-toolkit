"""Abstract backend interface."""

from __future__ import annotations
from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    def summarize(self, text: str, *, max_sentences: int = 3, language: str = "bengali") -> str: ...

    @abstractmethod
    def qa(self, context: str, question: str, *, language: str = "bengali") -> str: ...

    @abstractmethod
    def sentiment(self, text: str) -> dict[str, str | float]: ...
