# bangla-ai (Python)

[![PyPI](https://img.shields.io/pypi/v/bangla-ai.svg)](https://pypi.org/project/bangla-ai/)
[![Python](https://img.shields.io/pypi/pyversions/bangla-ai.svg)](https://pypi.org/project/bangla-ai/)
[![CI](https://github.com/ruhulaminpro/bangla-ai-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ruhulaminpro/bangla-ai-toolkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ruhulaminpro/bangla-ai-toolkit/blob/main/LICENSE)

AI-powered NLP toolkit for the Bengali language — **model-agnostic, zero-dependency text utilities, and pluggable ML backends**.

Bengali (বাংলা) is spoken by 230+ million people yet remains severely underrepresented in AI tooling. This package fills real gaps: the text utilities work with **zero dependencies**, and ML tasks run on either a **free HuggingFace backend** or a **paid OpenAI backend**.

## Install

```bash
# Text utilities only — zero dependencies
pip install bangla-ai

# With HuggingFace backend (free, works offline after first download)
pip install "bangla-ai[transformers]"

# With OpenAI backend
pip install "bangla-ai[openai]"

# Everything
pip install "bangla-ai[all]"
```

## Text utilities (no ML, no API key)

```python
from bangla_ai import text

raw = "বাংলাদেশ   দক্ষিণ এশিয়ার একটি দেশ।  এর রাজধানী ঢাকা।"

normalized = text.normalize(raw)        # NFC, zero-width strip, punct, spaces
tokens     = text.tokenize(normalized)  # word tokens, punctuation dropped
sents      = text.sent_tokenize(normalized)
filtered   = text.remove_stopwords(tokens)
stems      = text.stem_tokens(filtered) # বাংলাদেশের -> বাংলাদেশ
```

| Function | Description | Requires |
|---|---|---|
| `text.normalize` | Unicode NFC, zero-width removal, punctuation normalization | nothing |
| `text.tokenize` / `text.sent_tokenize` | Word & sentence tokenizer | nothing |
| `text.remove_stopwords` | 150+ curated Bengali stopwords | nothing |
| `text.stem_tokens` | Suffix-stripping stemmer (verbal + nominal) | nothing |

## ML tasks

```python
from bangla_ai import BanglaAI

# Free — HuggingFace models (downloaded on first use)
ai = BanglaAI()

# Paid — OpenAI API
ai = BanglaAI(backend="openai", api_key="sk-...")

passage = "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে।"

print(ai.summarize(passage, max_sentences=1))
print(ai.qa(passage, "বাংলাদেশের রাজধানী কোথায়?"))

result = ai.sentiment("আজকের দিনটি অসাধারণ ছিল!")
print(result["label"], result["score"])   # "positive" 0.97
```

| Method | Task | Requires |
|---|---|---|
| `BanglaAI.summarize` | Summarize Bengali passages | HF or OpenAI |
| `BanglaAI.qa` | Question answering from context | HF or OpenAI |
| `BanglaAI.sentiment` | Positive / negative / neutral | HF or OpenAI |
| `BanglaAI.ner` | Named entity recognition | HF or OpenAI |
| `BanglaAI.embed` / `BanglaAI.semantic_search` | Embeddings & semantic search | HF or OpenAI |

```python
ai.ner("ড. মুহাম্মদ ইউনূস ঢাকায় জন্মগ্রহণ করেন।")
# [{"text": "মুহাম্মদ ইউনূস", "type": "PER", ...}, {"text": "ঢাকা", "type": "LOC", ...}]

ai.semantic_search("দেশের রাজধানী", ["ঢাকা বাংলাদেশের রাজধানী।", "আমি ভাত খাই।"], top_k=1)
# [{"document": "ঢাকা বাংলাদেশের রাজধানী।", "score": 0.82, "index": 0}]
```

## Transliteration & numerals (no API key)

```python
from bangla_ai import text

text.to_latin("বাংলাদেশ")        # 'bangladesh'
text.to_bengali("bangla")        # 'বাংলা'
text.to_english_digits("২০২৪")   # '2024'
text.to_bengali_digits("2024")   # '২০২৪'
```

## Command line

```bash
bangla-ai translit --to latin "বাংলাদেশ"
bangla-ai digits --to bn "2024"
bangla-ai sentiment "আজকের দিনটি অসাধারণ ছিল!" --backend openai --api-key sk-...
```

## HuggingFace models used

| Task | Model |
|---|---|
| Summarization | `csebuetnlp/mT5_multilingual_XLSum` |
| Question Answering | `deepset/xlm-roberta-base-squad2` |
| Sentiment | `nlptown/bert-base-multilingual-uncased-sentiment` |

Swap models at construction via `summarizer_model`, `qa_model`, `sentiment_model`.

## Tests

```bash
cd python && pip install -e ".[dev]"
pytest tests/test_text.py -v        # no API key needed
OPENAI_API_KEY=sk-... pytest tests/ -v
```

## License

MIT. Built by [LXNotes](https://lxnotes.com) to support Bengali language AI.
Full project: https://github.com/ruhulaminpro/bangla-ai-toolkit
