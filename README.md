# bangla-ai-toolkit

AI-powered NLP toolkit for the Bengali language — **model-agnostic, zero-dependency text utilities, and pluggable ML backends**.

Bengali (বাংলা) is spoken by 230+ million people yet remains severely underrepresented in AI tooling. This toolkit fills real gaps:

- **Bengali text utilities** that work with zero ML dependencies (normalize, tokenize, stopwords, stemmer)
- **Free ML backend** via HuggingFace Transformers / Inference API
- **OpenAI backend** as a paid, higher-quality upgrade
- **Python + JavaScript** — works in any stack

---

## Features

| | Description | Requires |
|---|---|---|
| `text.normalize` | Unicode NFC, zero-width char removal, punctuation normalization | nothing |
| `text.tokenize` | Word & sentence tokenizer for Bengali text | nothing |
| `text.stopwords` | 150+ curated Bengali stopwords + `remove_stopwords()` | nothing |
| `text.stem` | Suffix-stripping stemmer (verbal + nominal inflections) | nothing |
| `BanglaAI.summarize` | Summarize Bengali passages | HF or OpenAI |
| `BanglaAI.qa` | Question answering from Bengali context | HF or OpenAI |
| `BanglaAI.sentiment` | Positive / negative / neutral classification | HF or OpenAI |

---

## Python

### Install

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

### Text utilities

```python
from bangla_ai import text

raw = "বাংলাদেশ   দক্ষিণ এশিয়ার একটি দেশ।  এর রাজধানী ঢাকা।"

normalized = text.normalize(raw)
# "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা।"

tokens = text.tokenize(normalized)
# ['বাংলাদেশ', 'দক্ষিণ', 'এশিয়ার', 'একটি', 'দেশ', 'এর', 'রাজধানী', 'ঢাকা']

sents = text.sent_tokenize(normalized)
# ['বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ', 'এর রাজধানী ঢাকা']

filtered = text.remove_stopwords(tokens)
# ['বাংলাদেশ', 'দক্ষিণ', 'এশিয়ার', 'দেশ', 'রাজধানী', 'ঢাকা']

stems = text.stem_tokens(filtered)
# করেছেন -> কর | বাংলাদেশের -> বাংলাদেশ | যাচ্ছে -> যা
```

### ML tasks

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
print(result["label"])   # "positive"
print(result["score"])   # 0.97
```

### Tests

```bash
cd python && pip install -e ".[dev]"

# No API key needed
pytest tests/test_text.py -v

# With OpenAI
OPENAI_API_KEY=sk-... pytest tests/ -v
```

---

## JavaScript

### Install

```bash
npm install bangla-ai

# Optional backends
npm install @huggingface/inference   # free
npm install openai                   # paid
```

### Text utilities

```js
import { text } from "bangla-ai";

const tokens = text.tokenize("আমি বাংলায় কথা বলি।");
const filtered = text.removeStopwords(tokens);
const stems = text.stemTokens(filtered);
```

### ML tasks

```js
import { BanglaAI } from "bangla-ai";

// Free — HuggingFace Inference API
const ai = new BanglaAI({ apiKey: process.env.HF_TOKEN });

// Paid — OpenAI
const ai = new BanglaAI({ backend: "openai", apiKey: process.env.OPENAI_API_KEY });

const passage = "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা।";
console.log(await ai.summarize(passage, { maxSentences: 1 }));

const r = await ai.sentiment("আজকের দিনটি অসাধারণ ছিল!");
console.log(r.label, r.score);
```

---

## HuggingFace models used

| Task | Model |
|---|---|
| Summarization | `csebuetnlp/mT5_multilingual_XLSum` |
| Question Answering | `deepset/xlm-roberta-base-squad2` |
| Sentiment | `nlptown/bert-base-multilingual-uncased-sentiment` |

Swap models at construction time via `summarizerModel`, `qaModel`, `sentimentModel` params.

---

## Project structure

```
bangla-ai-toolkit/
├── python/
│   ├── bangla_ai/
│   │   ├── text/         # normalize, tokenize, stopwords, stem
│   │   ├── backends/     # hf.py, openai.py (lazy-loaded)
│   │   └── core.py
│   ├── tests/
│   └── pyproject.toml
├── javascript/
│   ├── src/
│   │   ├── text/
│   │   ├── backends/
│   │   └── client.js
│   ├── tests/
│   └── package.json
└── docs/API.md
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs especially welcome for:
- More Bengali stopwords / stemmer rules
- New HuggingFace model integrations
- Bengali NER support

---

## License

MIT — see [LICENSE](LICENSE).  
Built by [LXNotes](https://lxnotes.com) to support Bengali language AI.
