"""BanglaAI — unified NLP client with pluggable backends."""

from __future__ import annotations
from .backends.base import Backend


class BanglaAI:
    """AI-powered Bengali NLP with swappable backends.

    Args:
        backend: "transformers" (free, default) or "openai" (paid, higher quality).
        **kwargs: Passed to the selected backend constructor.

    Examples::

        # Free — downloads HuggingFace models on first use
        ai = BanglaAI()

        # Paid — OpenAI API
        ai = BanglaAI(backend="openai", api_key="sk-...")

        # Bring your own backend
        ai = BanglaAI(backend=MyCustomBackend())
    """

    def __init__(self, backend: str | Backend = "transformers", **kwargs):
        if isinstance(backend, Backend):
            self._backend = backend
        elif backend == "transformers":
            from .backends.hf import TransformersBackend
            self._backend = TransformersBackend(**kwargs)
        elif backend == "openai":
            from .backends.openai import OpenAIBackend
            self._backend = OpenAIBackend(**kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend!r}. Use 'transformers' or 'openai'.")

    def summarize(self, text: str, *, max_sentences: int = 3, language: str = "bengali") -> str:
        """Summarize Bengali text.

        Args:
            text: Bengali input text.
            max_sentences: Target summary length in sentences.
            language: Output language — "bengali" (default) or "english".
        """
        return self._backend.summarize(text, max_sentences=max_sentences, language=language)

    def qa(self, context: str, question: str, *, language: str = "bengali") -> str:
        """Answer a question from a Bengali context passage.

        Args:
            context: Bengali passage containing the answer.
            question: Question in Bengali or English.
            language: Response language — "bengali" (default) or "english".
        """
        return self._backend.qa(context, question, language=language)

    def sentiment(self, text: str) -> dict[str, str | float]:
        """Classify sentiment of Bengali text.

        Returns:
            Dict with keys "label" (positive/negative/neutral),
            "score" (0.0–1.0), and "explanation".
        """
        return self._backend.sentiment(text)
