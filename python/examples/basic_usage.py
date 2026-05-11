"""Basic usage examples for bangla-ai."""

import os
from bangla_ai import BanglaAI

ai = BanglaAI(api_key=os.environ["OPENAI_API_KEY"])

# ── Summarization ──────────────────────────────────────────────────────────────
text = (
    "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। "
    "বাংলাদেশের মোট জনসংখ্যা প্রায় ১৭ কোটি। "
    "দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে।"
)
print("=== Summarization ===")
print(ai.summarize(text, max_sentences=2))
print()

# ── Question Answering ─────────────────────────────────────────────────────────
context = (
    "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন। "
    "তিনি ১৯১৩ সালে সাহিত্যে নোবেল পুরস্কার লাভ করেন।"
)
print("=== Question Answering ===")
print(ai.qa(context, "রবীন্দ্রনাথ কোথায় জন্মগ্রহণ করেন?"))
print()

# ── Sentiment Analysis ─────────────────────────────────────────────────────────
print("=== Sentiment Analysis ===")
result = ai.sentiment("আজকের দিনটি অসাধারণ ছিল! সব কিছু ভালো হয়েছে।")
print(f"Label: {result['label']}")
print(f"Score: {result['score']:.2f}")
print(f"Explanation: {result['explanation']}")
