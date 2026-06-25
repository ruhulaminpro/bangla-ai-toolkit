"""Run the evaluation harness against a backend.

Usage (from the ``python/`` directory)::

    python -m benchmarks.run --backend transformers
    python -m benchmarks.run --backend openai --api-key sk-... --task sentiment

Summaries and QA answers are scored with token-overlap F1 (QA also reports
exact match); sentiment is scored with label accuracy. The bundled dataset is
small and meant for smoke-testing and relative backend comparison, not as an
authoritative benchmark — see ROADMAP.md for the plan to grow it.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

from bangla_ai import BanglaAI
from . import metrics

_DATA = Path(__file__).parent / "data" / "bn_eval.json"


def _load() -> dict:
    return json.loads(_DATA.read_text(encoding="utf-8"))


def eval_summarize(ai: BanglaAI, items: list[dict]) -> dict:
    scores = []
    for it in items:
        pred = ai.summarize(it["text"], max_sentences=1)
        scores.append(metrics.token_f1(pred, it["reference"]))
    return {"task": "summarize", "n": len(items), "token_f1": round(metrics.mean(scores), 4)}


def eval_qa(ai: BanglaAI, items: list[dict]) -> dict:
    f1s, ems = [], []
    for it in items:
        pred = ai.qa(it["context"], it["question"])
        f1s.append(metrics.token_f1(pred, it["answer"]))
        ems.append(metrics.exact_match(pred, it["answer"]))
    return {
        "task": "qa", "n": len(items),
        "token_f1": round(metrics.mean(f1s), 4),
        "exact_match": round(metrics.mean(ems), 4),
    }


def eval_sentiment(ai: BanglaAI, items: list[dict]) -> dict:
    preds = [ai.sentiment(it["text"])["label"] for it in items]
    refs = [it["label"] for it in items]
    return {"task": "sentiment", "n": len(items), "accuracy": round(metrics.accuracy(preds, refs), 4)}


_EVALUATORS = {"summarize": eval_summarize, "qa": eval_qa, "sentiment": eval_sentiment}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="benchmarks.run", description="Evaluate a bangla-ai backend")
    parser.add_argument("--backend", default="transformers")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--task", choices=["all", *_EVALUATORS], default="all")
    args = parser.parse_args(argv)

    kwargs = {}
    if args.api_key:
        kwargs["api_key"] = args.api_key
    if args.model:
        kwargs["model"] = args.model
    ai = BanglaAI(backend=args.backend, **kwargs)

    data = _load()
    tasks = list(_EVALUATORS) if args.task == "all" else [args.task]
    results = [_EVALUATORS[t](ai, data[t]) for t in tasks]

    print(f"\nBackend: {args.backend}")
    print("-" * 48)
    for r in results:
        line = " | ".join(f"{k}={v}" for k, v in r.items() if k != "task")
        print(f"{r['task']:<10} {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
