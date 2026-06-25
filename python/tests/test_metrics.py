"""Tests for the benchmark metric functions (zero-dep, no models needed)."""

import json
from pathlib import Path

import pytest

from benchmarks import metrics


def test_token_f1_identical():
    assert metrics.token_f1("ঢাকা শহর", "ঢাকা শহর") == pytest.approx(1.0)


def test_token_f1_no_overlap():
    assert metrics.token_f1("ঢাকা", "চট্টগ্রাম") == 0.0


def test_token_f1_partial():
    # 1 shared token ("রাজধানী") out of pred=2, ref=3 → P=.5, R=.333, F1≈0.4
    score = metrics.token_f1("রাজধানী ঢাকা", "বাংলাদেশের রাজধানী শহর")
    assert score == pytest.approx(0.4, abs=1e-3)


def test_token_f1_empty():
    assert metrics.token_f1("", "ঢাকা") == 0.0


def test_exact_match_normalizes():
    # Extra spaces are collapsed by normalize() before comparison.
    assert metrics.exact_match("ঢাকা   শহর", "ঢাকা শহর") == 1.0
    assert metrics.exact_match("ঢাকা", "চট্টগ্রাম") == 0.0


def test_accuracy():
    assert metrics.accuracy(["positive", "negative", "neutral"],
                            ["positive", "positive", "neutral"]) == pytest.approx(2 / 3)
    assert metrics.accuracy([], []) == 0.0


def test_bundled_dataset_is_valid():
    data = json.loads((Path(__file__).parent.parent / "benchmarks" / "data" / "bn_eval.json").read_text(encoding="utf-8"))
    assert set(data) == {"summarize", "qa", "sentiment"}
    assert all("reference" in x for x in data["summarize"])
    assert all({"context", "question", "answer"} <= set(x) for x in data["qa"])
    assert all(x["label"] in {"positive", "negative", "neutral"} for x in data["sentiment"])
