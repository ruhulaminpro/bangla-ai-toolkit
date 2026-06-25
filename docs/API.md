# API Reference

The Python and JavaScript packages expose the same surface. JavaScript method
names are camelCase and the ML methods are `async` (return `Promise`).

---

## Python

### Text utilities — `bangla_ai.text` (zero dependencies)

| Function | Returns | Description |
|---|---|---|
| `normalize(text, *, strip_zero_width=True, normalize_punct=True)` | `str` | NFC + zero-width strip + punctuation/space normalization |
| `tokenize(text)` | `list[str]` | Word tokens (punctuation dropped) |
| `sent_tokenize(text)` | `list[str]` | Sentences (splits on । ॥ . ! ?) |
| `remove_stopwords(tokens)` | `list[str]` | Drop the 150+ curated stopwords |
| `stem(word)` / `stem_tokens(tokens)` | `str` / `list[str]` | Suffix-stripping stemmer |
| `to_latin(text)` | `str` | Bengali → Latin romanization (approximate) |
| `to_bengali(text)` | `str` | Latin "Banglish" → Bengali (approximate) |
| `to_english_digits(text)` | `str` | ০-৯ → 0-9 |
| `to_bengali_digits(text)` | `str` | 0-9 → ০-৯ |

### `BanglaAI(backend="transformers", **kwargs)`

`backend` is `"transformers"` (free, default), `"openai"`, or any object
implementing the `Backend` interface. Extra `kwargs` are forwarded to the
backend constructor (e.g. `api_key`, `model`, `embedding_model`, model overrides).

```python
ai = BanglaAI()                                   # HuggingFace
ai = BanglaAI(backend="openai", api_key="sk-...") # OpenAI
```

| Method | Returns | Notes |
|---|---|---|
| `summarize(text, *, max_sentences=3, language="bengali")` | `str` | |
| `qa(context, question, *, language="bengali")` | `str` | |
| `sentiment(text)` | `dict` | `{"label", "score", "explanation"}` |
| `ner(text)` | `list[dict]` | `[{"text", "type", "score"}]`; type ∈ PER/LOC/ORG/MISC |
| `embed(texts)` | `list[list[float]]` | Accepts a `str` or `list[str]` |
| `semantic_search(query, documents, *, top_k=5)` | `list[dict]` | `[{"document", "score", "index"}]`, best first |

`ner` and `embed` raise `NotImplementedError` on a custom backend that does not
implement them.

### `bangla_ai.semantic` (zero dependencies)

| Function | Returns |
|---|---|
| `cosine_similarity(a, b)` | `float` |
| `rank_by_similarity(query_vec, doc_vecs)` | `list[(index, score)]` sorted by score |

---

## JavaScript

```js
import { BanglaAI, text, cosineSimilarity, rankBySimilarity } from "bangla-ai";
```

### `text` utilities

`normalize`, `tokenize`, `sentTokenize`, `removeStopwords`, `stem`, `stemTokens`,
`toLatin`, `toBengali`, `toEnglishDigits`, `toBengaliDigits` — same behavior as
Python, camelCase names.

### `new BanglaAI({ backend, apiKey, model })`

`backend` is `"huggingface"` (default), `"openai"`, or a custom object.

```js
const ai = new BanglaAI();                                    // HuggingFace
const ai = new BanglaAI({ backend: "openai", apiKey: "sk-..." });

await ai.summarize(text, { maxSentences, language });
await ai.qa(context, question, { language });
await ai.sentiment(text);                 // { label, score, explanation }
await ai.ner(text);                       // [{ text, type, score }]
await ai.embed(texts);                    // string | string[] -> number[][]
await ai.semanticSearch(query, documents, { topK });  // [{ document, score, index }]
```

TypeScript types ship in `index.d.ts`.

---

## CLI (`bangla-ai`)

Shipped by both packages.

```bash
bangla-ai normalize "বাংলা   টেক্সট"
bangla-ai tokenize "আমি বাংলায় কথা বলি।"
bangla-ai stem "করেছেন বাংলাদেশের"
bangla-ai translit --to latin "বাংলাদেশ"
bangla-ai translit --to bengali "bangla"
bangla-ai digits --to bn "2024"
bangla-ai digits --to en "২০২৪"

# ML tasks — add --backend / --api-key / --model
bangla-ai summarize "…" --max-sentences 2 --backend openai --api-key sk-...
bangla-ai qa "…context…" --question "…?"
bangla-ai sentiment "…"
bangla-ai ner "…"

# Read from stdin with "-"
echo "…" | bangla-ai tokenize -
```
