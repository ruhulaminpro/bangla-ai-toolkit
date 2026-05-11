# API Reference

## Python

### `BanglaAI(api_key=None, model="gpt-4o-mini")`

Main client. Falls back to `OPENAI_API_KEY` environment variable.

#### `ai.summarize(text, *, max_sentences=3, language="bengali") → str`

Summarize Bengali text.

| Param | Type | Description |
|---|---|---|
| `text` | `str` | Bengali input text |
| `max_sentences` | `int` | Target summary length (default: 3) |
| `language` | `str` | `"bengali"` or `"english"` |

#### `ai.qa(context, question, *, language="bengali") → str`

Answer a question based on a Bengali context passage.

| Param | Type | Description |
|---|---|---|
| `context` | `str` | Bengali passage containing the answer |
| `question` | `str` | Question in Bengali or English |
| `language` | `str` | `"bengali"` or `"english"` |

#### `ai.sentiment(text) → dict`

Classify sentiment of Bengali text.

Returns:
```json
{
  "label": "positive | negative | neutral",
  "score": 0.95,
  "explanation": "..."
}
```

---

## JavaScript

Same API surface, but:
- Constructor uses `{ apiKey, model }` options object
- Methods are called as `ai.summarize.call(text, options)` etc.
- All methods are `async` and return `Promise`

### `new BanglaAI({ apiKey, model = "gpt-4o-mini" })`

#### `await ai.summarize.call(text, { maxSentences, language })`
#### `await ai.qa.call(context, question, { language })`
#### `await ai.sentiment.call(text)`
