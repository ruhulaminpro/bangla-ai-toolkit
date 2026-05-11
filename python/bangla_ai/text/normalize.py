"""Bengali Unicode normalization.

Bengali text appears in multiple encodings and Unicode representations.
This module canonicalizes text to NFC and fixes common encoding artifacts.
"""

from __future__ import annotations
import re
import unicodedata

# Zero-width characters that serve no semantic purpose in plain text
_ZW_STRIP = re.compile(r"[​‌‍﻿]")

# Multiple spaces → single space
_MULTI_SPACE = re.compile(r" {2,}")

# Characters that have canonical precomposed forms in Bengali Unicode block
# (U+09DC = ড়, U+09DD = ঢ়, U+09DF = য়) but are sometimes encoded as
# base + nukta (U+09BC). NFC handles most of these, but we verify explicitly.
_DECOMPOSED_PATTERNS = [
    ("ড়", "ড়"),  # ড + ় → ড়
    ("ঢ়", "ঢ়"),  # ঢ + ় → ঢ়
    ("য়", "য়"),  # য + ় → য়
]

# Punctuation normalization: curly quotes, em-dash, etc. → ASCII equivalents
_PUNCT_MAP = str.maketrans({
    "“": '"', "”": '"',   # " "
    "‘": "'", "’": "'",   # ' '
    "–": "-", "—": "-",   # en-dash, em-dash
    " ": " ",                  # non-breaking space
})


def normalize(text: str, *, strip_zero_width: bool = True, normalize_punct: bool = True) -> str:
    """Normalize Bengali Unicode text.

    Steps applied:
    1. NFC Unicode normalization (composes combining characters).
    2. Fix decomposed Bengali characters (ড+় → ড়, etc.).
    3. Optionally strip zero-width characters (ZWSP, ZWNJ, ZWJ, BOM).
    4. Optionally normalize common punctuation to ASCII equivalents.
    5. Collapse multiple spaces; strip leading/trailing whitespace.

    Args:
        text: Input string.
        strip_zero_width: Remove zero-width invisible characters (default True).
        normalize_punct: Map curly quotes and dashes to ASCII (default True).

    Returns:
        Normalized string.
    """
    text = unicodedata.normalize("NFC", text)

    for decomposed, composed in _DECOMPOSED_PATTERNS:
        text = text.replace(decomposed, composed)

    if strip_zero_width:
        text = _ZW_STRIP.sub("", text)

    if normalize_punct:
        text = text.translate(_PUNCT_MAP)

    text = _MULTI_SPACE.sub(" ", text).strip()
    return text
