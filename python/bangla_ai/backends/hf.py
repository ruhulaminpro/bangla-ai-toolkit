"""HuggingFace Transformers backend — free, works offline after first download."""

from __future__ import annotations
from .base import Backend

# Defaults chosen for Bengali quality vs. size balance
_DEFAULT_SUMMARIZER = "csebuetnlp/mT5_multilingual_XLSum"
_DEFAULT_QA = "deepset/xlm-roberta-base-squad2"
_DEFAULT_SENTIMENT = "nlptown/bert-base-multilingual-uncased-sentiment"

# Map 1–5 star labels from nlptown model to our canonical labels
_STAR_TO_LABEL = {
    "1 star": "negative",
    "2 stars": "negative",
    "3 stars": "neutral",
    "4 stars": "positive",
    "5 stars": "positive",
}


class TransformersBackend(Backend):
    """
    Uses HuggingFace pipelines. Models are downloaded on first use and cached.

    Args:
        summarizer_model: HF model ID for summarization.
        qa_model: HF model ID for question answering.
        sentiment_model: HF model ID for sentiment classification.
        device: "cpu" | "cuda" | "mps" — auto-detected if None.
    """

    def __init__(
        self,
        summarizer_model: str = _DEFAULT_SUMMARIZER,
        qa_model: str = _DEFAULT_QA,
        sentiment_model: str = _DEFAULT_SENTIMENT,
        device: str | None = None,
    ):
        try:
            from transformers import pipeline
        except ImportError as e:
            raise ImportError(
                "transformers backend requires: pip install bangla-ai[transformers]"
            ) from e

        self._pipeline = pipeline
        self._summarizer_model = summarizer_model
        self._qa_model = qa_model
        self._sentiment_model = sentiment_model
        self._device = device

        # Pipelines are lazy-loaded on first use
        self._sum_pipe = None
        self._qa_pipe = None
        self._sent_pipe = None

    def _get_sum_pipe(self):
        if self._sum_pipe is None:
            kw = {} if self._device is None else {"device": self._device}
            self._sum_pipe = self._pipeline("summarization", model=self._summarizer_model, **kw)
        return self._sum_pipe

    def _get_qa_pipe(self):
        if self._qa_pipe is None:
            kw = {} if self._device is None else {"device": self._device}
            self._qa_pipe = self._pipeline("question-answering", model=self._qa_model, **kw)
        return self._qa_pipe

    def _get_sent_pipe(self):
        if self._sent_pipe is None:
            kw = {} if self._device is None else {"device": self._device}
            self._sent_pipe = self._pipeline("text-classification", model=self._sentiment_model, **kw)
        return self._sent_pipe

    def summarize(self, text: str, *, max_sentences: int = 3, language: str = "bengali") -> str:
        # mT5_multilingual_XLSum expects a language prefix
        prefix = "bengali: " if language == "bengali" else "english: "
        result = self._get_sum_pipe()(
            prefix + text,
            max_new_tokens=200,
            min_new_tokens=20,
            truncation=True,
        )
        return result[0]["summary_text"].strip()

    def qa(self, context: str, question: str, *, language: str = "bengali") -> str:
        result = self._get_qa_pipe()(question=question, context=context)
        return result["answer"].strip()

    def sentiment(self, text: str) -> dict[str, str | float]:
        result = self._get_sent_pipe()(text, truncation=True)[0]
        raw_label: str = result["label"].lower()
        label = _STAR_TO_LABEL.get(raw_label, raw_label)
        return {
            "label": label,
            "score": round(float(result["score"]), 4),
            "explanation": "",  # model doesn't produce explanations
        }
