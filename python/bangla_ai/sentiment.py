"""Bengali sentiment analysis."""

from __future__ import annotations
import json
from openai import OpenAI

_SYSTEM = """You are a Bengali sentiment analysis expert.
Analyze the sentiment of Bengali text and return a JSON object with:
  - "label": one of "positive", "negative", or "neutral"
  - "score": confidence float between 0.0 and 1.0
  - "explanation": one-sentence reason in Bengali

Return only valid JSON. No markdown, no extra text."""

SentimentResult = dict[str, str | float]


class Sentiment:
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini"):
        self._client = client
        self._model = model

    def __call__(self, text: str) -> SentimentResult:
        """Classify sentiment of Bengali text.

        Args:
            text: Bengali input text.

        Returns:
            Dict with keys "label", "score", and "explanation".
        """
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": text},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
