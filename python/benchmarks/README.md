# Benchmarks

A small evaluation harness for comparing backends on Bengali tasks. Not shipped
in the published package.

```bash
cd python
# Free backend (downloads HuggingFace models on first run)
python -m benchmarks.run --backend transformers

# OpenAI backend
python -m benchmarks.run --backend openai --api-key sk-... --task sentiment
```

## Metrics
- **summarize** — token-overlap F1 against a reference summary
- **qa** — token-overlap F1 + exact match
- **sentiment** — label accuracy

Token F1 uses the toolkit's own Bengali tokenizer, so scores reflect the same
word units the library produces. Metric functions live in
[`metrics.py`](metrics.py) and are unit-tested in `tests/test_metrics.py`.

## Dataset
The bundled dataset (`data/bn_eval.json`) is intentionally tiny — it is for
smoke-testing and relative backend comparison, not an authoritative benchmark.
Growing it into a real open Bengali eval set is part of the
[ROADMAP](../../ROADMAP.md), and one of the things OpenAI API credits would fund.
