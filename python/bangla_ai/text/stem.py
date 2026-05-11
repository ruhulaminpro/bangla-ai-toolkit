"""Bengali suffix-stripping stemmer.

Lightweight rule-based stemmer — NOT a full morphological analyzer.
Strips common inflectional suffixes to reduce surface forms to approximate roots.
Suitable for bag-of-words tasks (search, classification).

Limitations:
- Does not handle compound words (সমাস)
- Does not distinguish homographic stems
- No POS-aware stripping

Unicode note: Bengali vowel signs (মাত্রা) are combining characters, e.g.:
  া = U+09BE,  ি = U+09BF,  ী = U+09C0,  ু = U+09C1
  ূ = U+09C2,  ে = U+09CB,  ো = U+09CB U+09BE,  ্ = U+09CD (hasanta/virama)
These differ from standalone vowel letters — suffixes must use the correct form.
"""

from __future__ import annotations

# Ordered longest → shortest so we strip the most specific suffix first.
# (suffix_string, minimum_stem_length_in_chars)
_SUFFIXES: list[tuple[str, int]] = [
    # ── Verbal — perfect (must precede simple present — longer suffix first) ──
    # করেছেন = কর + েছেন  (ে = U+09CB vowel sign, not standalone এ letter)
    ("েছিলেন", 2), ("েছিলাম", 2), ("েছিলে", 2), ("েছিলো", 2),
    ("েছেন", 2), ("েছে", 2), ("েছি", 2), ("েছো", 2),

    # ── Verbal — past imperfect / habitual ───────────────────────────────────
    # যাচ্ছিলেন = যা + চ্ছিলেন
    ("চ্ছিলেন", 2), ("চ্ছিলাম", 2), ("চ্ছিলে", 2), ("চ্ছিলো", 2), ("চ্ছিল", 2),
    # করছিলেন = কর + ছিলেন
    ("ছিলেন", 2), ("ছিলাম", 2), ("ছিলে", 2), ("ছিলো", 2), ("ছিল", 2),
    # যাচ্ছেন = যা + চ্ছেন
    ("চ্ছেন", 2), ("চ্ছে", 2), ("চ্ছি", 2), ("চ্ছো", 2),
    # করছেন = কর + ছেন
    ("ছেন", 2), ("ছে", 2), ("ছি", 2), ("ছো", 2),

    # ── Verbal — simple past ─────────────────────────────────────────────────
    ("লেন", 2), ("লাম", 2), ("লাে", 2), ("লো", 2), ("লে", 2), ("ল", 2),

    # ── Verbal — future ──────────────────────────────────────────────────────
    ("বেন", 2), ("বেছি", 2), ("বো", 2), ("বে", 2), ("বি", 2),

    # ── Verbal — imperative / present ────────────────────────────────────────
    ("উন", 2), ("ুন", 2), ("েন", 2),

    # ── Nominal — plural ──────────────────────────────────────────────────────
    ("গুলোকে", 2), ("গুলোর", 2), ("গুলো", 2),
    ("েরকে", 2), ("েরও", 2), ("েরা", 2),
    ("দেরকে", 2), ("দেরও", 2), ("দের", 2),
    ("রাকে", 2), ("রারও", 2), ("রা", 2),

    # ── Nominal — case markers ────────────────────────────────────────────────
    # Genitive:  বাংলাদেশ + ের = বাংলাদেশের  (ে = U+09CB)
    ("ের", 2),
    # Locative:  ঘরে = ঘর + ে
    ("তেও", 2), ("তে", 2),
    # Accusative/dative
    ("কেও", 2), ("কে", 2),
    # Simple genitive after vowel-final stems: তার + র already handled above
    ("র", 2),

    # ── Derivational ──────────────────────────────────────────────────────────
    ("আনো", 2), ("ওয়া", 2), ("িত", 2),
]


def stem(word: str) -> str:
    """Strip inflectional suffixes from a Bengali word.

    Args:
        word: A single Bengali word token.

    Returns:
        Approximate stem (may not be a real dictionary root).
    """
    for suffix, min_len in _SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= min_len:
            return word[: -len(suffix)]
    return word


def stem_tokens(tokens: list[str]) -> list[str]:
    """Stem a list of tokens."""
    return [stem(t) for t in tokens]
