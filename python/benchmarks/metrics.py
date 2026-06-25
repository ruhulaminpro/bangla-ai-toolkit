"""Zero-dependency evaluation metrics.

Token-overlap F1 reuses the toolkit's own Bengali tokenizer, so summaries and
answers are scored on the same word units the library produces elsewhere.
"""

from __future__ import annotations
from collections import Counter

from bangla_ai.text import tokenize, normalize


def token_f1(prediction: str, reference: str) -> float:
    """Token-overlap F1 between a prediction and a reference string.

    Bag-of-tokens (multiset) overlap — order-insensitive. Returns 0.0 when
    there is no overlap or either side is empty.
    """
    pred = Counter(tokenize(normalize(prediction)))
    ref = Counter(tokenize(normalize(reference)))
    common = sum((pred & ref).values())
    if common == 0:
        return 0.0
    precision = common / sum(pred.values())
    recall = common / sum(ref.values())
    return 2 * precision * recall / (precision + recall)


def exact_match(prediction: str, reference: str) -> float:
    """1.0 if the normalized strings match exactly, else 0.0."""
    return 1.0 if normalize(prediction) == normalize(reference) else 0.0


def accuracy(predictions: list[str], references: list[str]) -> float:
    """Fraction of predictions equal to their reference label."""
    if not references:
        return 0.0
    hits = sum(1 for p, r in zip(predictions, references) if p == r)
    return hits / len(references)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
