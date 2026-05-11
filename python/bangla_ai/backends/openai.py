"""OpenAI backend — higher quality, requires API key."""

from __future__ import annotations
import json
from .base import Backend

_SUM_SYSTEM = (
    "You are an expert Bengali language summarizer. "
    "Output only the summary — no preamble."
)
_QA_SYSTEM = (
    "You are a Bengali question answering assistant. "
    "Answer strictly from the provided context. "
    "If the answer is not in the context, say so."
)
_SENT_SYSTEM = (
    "Bengali sentiment analysis expert. "
    "Return JSON: {\"label\": \"positive|negative|neutral\", "
    "\"score\": 0.0-1.0, \"explanation\": \"one sentence in Bengali\"}. "
    "Only JSON, no markdown."
)


class OpenAIBackend(Backend):
    """
    Uses OpenAI chat completions API.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: Chat model to use (default: gpt-4o-mini).
    """

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "openai backend requires: pip install bangla-ai[openai]"
            ) from e
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def _chat(self, system: str, user: str, temperature: float = 0.3, json_mode: bool = False) -> str:
        kwargs: dict = dict(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=temperature,
        )
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        return self._client.chat.completions.create(**kwargs).choices[0].message.content.strip()

    def summarize(self, text: str, *, max_sentences: int = 3, language: str = "bengali") -> str:
        lang = "Bengali (বাংলা)" if language == "bengali" else "English"
        prompt = f"Summarize in {max_sentences} sentences. Respond in {lang}.\n\n{text}"
        return self._chat(_SUM_SYSTEM, prompt, temperature=0.3)

    def qa(self, context: str, question: str, *, language: str = "bengali") -> str:
        lang = "Bengali (বাংলা)" if language == "bengali" else "English"
        prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer in {lang}."
        return self._chat(_QA_SYSTEM, prompt, temperature=0.1)

    def sentiment(self, text: str) -> dict[str, str | float]:
        raw = self._chat(_SENT_SYSTEM, text, temperature=0.0, json_mode=True)
        return json.loads(raw)
