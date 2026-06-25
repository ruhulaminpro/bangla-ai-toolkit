# bangla-ai (JavaScript)

[![npm](https://img.shields.io/npm/v/bangla-ai.svg)](https://www.npmjs.com/package/bangla-ai)
[![CI](https://github.com/ruhulaminpro/bangla-ai-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ruhulaminpro/bangla-ai-toolkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ruhulaminpro/bangla-ai-toolkit/blob/main/LICENSE)

AI-powered NLP toolkit for the Bengali language — **model-agnostic, zero-dependency text utilities, and pluggable ML backends**.

Bengali (বাংলা) is spoken by 230+ million people yet remains severely underrepresented in AI tooling. The text utilities have **zero dependencies**; ML tasks run on either a **free HuggingFace backend** or a **paid OpenAI backend**.

## Install

```bash
npm install bangla-ai

# Optional backends
npm install @huggingface/inference   # free
npm install openai                   # paid
```

ESM-only. Node.js 18+.

## Text utilities (no ML, no API key)

```js
import { text } from "bangla-ai";

const tokens   = text.tokenize("আমি বাংলায় কথা বলি।");
const filtered = text.removeStopwords(tokens);
const stems    = text.stemTokens(filtered);
```

| Function | Description |
|---|---|
| `text.normalize` | Unicode NFC, zero-width removal, punctuation normalization |
| `text.tokenize` / `text.sentTokenize` | Word & sentence tokenizer |
| `text.removeStopwords` | 150+ curated Bengali stopwords |
| `text.stemTokens` | Suffix-stripping stemmer (verbal + nominal) |

## ML tasks

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

## Tests

```bash
cd javascript && npm install && npm test
```

## License

MIT. Built by [LXNotes](https://lxnotes.com) to support Bengali language AI.
Full project: https://github.com/ruhulaminpro/bangla-ai-toolkit
