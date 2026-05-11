"""bangla-ai usage examples."""

import os

# ── 1. Text utilities — zero dependencies ──────────────────────────────────────
from bangla_ai import text

raw = "বাংলাদেশ   দক্ষিণ এশিয়ার একটি দেশ।  এর রাজধানী ঢাকা।"

normalized = text.normalize(raw)
tokens = text.tokenize(normalized)
sentences = text.sent_tokenize(normalized)
filtered = text.remove_stopwords(tokens)
stems = text.stem_tokens(filtered)

print("=== Text Utilities ===")
print("Normalized :", normalized)
print("Tokens     :", tokens)
print("Sentences  :", sentences)
print("Filtered   :", filtered)
print("Stems      :", stems)
print()

# ── 2. HuggingFace backend (free) ──────────────────────────────────────────────
# Uncomment after: pip install bangla-ai[transformers]
#
# from bangla_ai import BanglaAI
# ai = BanglaAI()  # downloads models on first run
# ...

# ── 3. OpenAI backend ──────────────────────────────────────────────────────────
from bangla_ai import BanglaAI

ai = BanglaAI(backend="openai", api_key=os.environ["OPENAI_API_KEY"])

passage = (
    "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। "
    "দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে।"
)

print("=== Summarization ===")
print(ai.summarize(passage, max_sentences=1))
print()

print("=== Question Answering ===")
print(ai.qa(passage, "বাংলাদেশের রাজধানী কোথায়?"))
print()

print("=== Sentiment Analysis ===")
r = ai.sentiment("আজকের দিনটি অসাধারণ ছিল!")
print(f"Label: {r['label']}  Score: {r['score']:.2f}")
print(f"Explanation: {r['explanation']}")
