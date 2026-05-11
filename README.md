# bangla-ai-toolkit

AI-powered NLP toolkit for the Bengali language — **summarization, question answering, and sentiment analysis** in both Python and JavaScript.

Bengali (বাংলা) is spoken by 230+ million people yet remains severely underrepresented in AI tooling. This toolkit bridges that gap using OpenAI models with prompts optimized for Bengali text.

---

## Features

| Feature | Description |
|---|---|
| **Summarization** | Condense long Bengali passages into key points |
| **Question Answering** | Extract answers from Bengali context passages |
| **Sentiment Analysis** | Classify text as positive / negative / neutral with confidence score |
| **Bilingual output** | Respond in Bengali or English |
| **Python + JavaScript** | Use in any stack |

---

## Python

### Install

```bash
pip install bangla-ai
```

### Usage

```python
import os
from bangla_ai import BanglaAI

ai = BanglaAI(api_key=os.environ["OPENAI_API_KEY"])

# Summarization
text = "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে।"
print(ai.summarize(text, max_sentences=2))

# Question Answering
context = "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন। তিনি ১৯১৩ সালে নোবেল পুরস্কার পান।"
print(ai.qa(context, "রবীন্দ্রনাথ কোথায় জন্মগ্রহণ করেন?"))

# Sentiment Analysis
result = ai.sentiment("আজকের দিনটি অসাধারণ ছিল!")
print(result["label"])   # "positive"
print(result["score"])   # 0.97
```

### Run tests

```bash
cd python
OPENAI_API_KEY=sk-... pytest tests/
```

---

## JavaScript

### Install

```bash
npm install bangla-ai
```

### Usage

```js
import { BanglaAI } from "bangla-ai";

const ai = new BanglaAI({ apiKey: process.env.OPENAI_API_KEY });

// Summarization
const text = "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা।";
console.log(await ai.summarize.call(text, { maxSentences: 1 }));

// Question Answering
const context = "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন।";
console.log(await ai.qa.call(context, "Tagore was born where?", { language: "english" }));

// Sentiment
const result = await ai.sentiment.call("আজকের দিনটি অসাধারণ ছিল!");
console.log(result.label);  // "positive"
```

### Run tests

```bash
cd javascript
npm install
OPENAI_API_KEY=sk-... npm test
```

---

## Models

Default model: `gpt-4o-mini` (fast, cheap).  
Swap to `gpt-4o` for higher accuracy:

```python
ai = BanglaAI(model="gpt-4o")
```

---

## Project Structure

```
bangla-ai-toolkit/
├── python/
│   ├── bangla_ai/        # Python package
│   ├── tests/            # pytest test suite
│   ├── examples/         # Usage examples
│   └── pyproject.toml
├── javascript/
│   ├── src/              # ES module package
│   ├── tests/            # Jest test suite
│   ├── examples/         # Usage examples
│   └── package.json
├── docs/
│   └── API.md            # Full API reference
└── LICENSE               # MIT
```

---

## Contributing

Pull requests welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE).

---

Built with ♥ by [LXNotes](https://lxnotes.com) to support Bengali language AI.
