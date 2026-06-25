"""Bengali transliteration (romanization and phonetic input).

Two directions:

- ``to_latin``  — Bengali script → Latin (romanization). Deterministic.
- ``to_bengali`` — Latin "Banglish" → Bengali script (phonetic typing).

Both are **approximate**. Bengali↔Latin has no lossless standard mapping:
romanization drops vowel-length distinctions, and phonetic input is inherently
ambiguous (e.g. "t" could be ত or ট). These functions aim to be correct on the
common cases used in chat, search, and casual writing — not to be a reversible
codec. See the test suite for the cases that are guaranteed.
"""

from __future__ import annotations

# ── Bengali → Latin tables ────────────────────────────────────────────────────

_INDEP_VOWELS = {
    "অ": "o", "আ": "a", "ই": "i", "ঈ": "i", "উ": "u", "ঊ": "u",
    "ঋ": "ri", "এ": "e", "ঐ": "oi", "ও": "o", "ঔ": "ou",
}

# Vowel signs (matras) — combine with the preceding consonant
_MATRAS = {
    "া": "a", "ি": "i", "ী": "i", "ু": "u", "ূ": "u", "ৃ": "ri",
    "ে": "e", "ৈ": "oi", "ো": "o", "ৌ": "ou",
}

_CONSONANTS = {
    "ক": "k", "খ": "kh", "গ": "g", "ঘ": "gh", "ঙ": "ng",
    "চ": "ch", "ছ": "chh", "জ": "j", "ঝ": "jh", "ঞ": "n",
    "ট": "t", "ঠ": "th", "ড": "d", "ঢ": "dh", "ণ": "n",
    "ত": "t", "থ": "th", "দ": "d", "ধ": "dh", "ন": "n",
    "প": "p", "ফ": "ph", "ব": "b", "ভ": "bh", "ম": "m",
    "য": "j", "র": "r", "ল": "l", "শ": "sh", "ষ": "sh",
    "স": "s", "হ": "h", "ড়": "r", "ঢ়": "rh", "য়": "y",
    "ৎ": "t",
}

# Standalone signs
_SIGNS = {"ং": "ng", "ঃ": "h", "ঁ": "n"}

_HASANTA = "্"          # virama — suppresses the inherent vowel
_INHERENT = "o"         # inherent vowel carried by a bare consonant


def to_latin(text: str) -> str:
    """Romanize Bengali script to Latin (approximate).

    Bare consonants receive the inherent vowel ``o`` unless followed by a
    matra, a hasanta (conjunct), or an explicit vowel.

    >>> to_latin("বাংলা")
    'bangla'
    >>> to_latin("ঢাকা")
    'dhaka'
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in _CONSONANTS:
            out.append(_CONSONANTS[ch])
            nxt = text[i + 1] if i + 1 < n else ""
            if nxt == _HASANTA:
                i += 2          # conjunct: no inherent vowel, drop the hasanta
                continue
            if nxt in _MATRAS:
                out.append(_MATRAS[nxt])
                i += 2
                continue
            # Inherent vowel — but drop it word-finally (Bengali schwa deletion):
            # only keep it if another Bengali letter continues the word.
            if nxt in _CONSONANTS or nxt in _INDEP_VOWELS or nxt in _SIGNS:
                out.append(_INHERENT)
            i += 1
            continue
        if ch in _INDEP_VOWELS:
            out.append(_INDEP_VOWELS[ch])
        elif ch in _SIGNS:
            out.append(_SIGNS[ch])
        elif ch in _MATRAS:
            out.append(_MATRAS[ch])     # stray matra (no preceding consonant)
        else:
            out.append(ch)              # whitespace, punctuation, ASCII
        i += 1
    return "".join(out)


# ── Latin → Bengali tables ────────────────────────────────────────────────────
# Multi-character keys are matched greedily (longest first).

_LATIN_INDEP = {
    "ou": "ঔ", "oi": "ঐ", "oo": "ঊ", "ee": "ঈ", "aa": "আ",
    "a": "আ", "i": "ই", "u": "উ", "e": "এ", "o": "অ", "O": "ও",
}

_LATIN_MATRA = {
    "ou": "ৌ", "oi": "ৈ", "oo": "ূ", "ee": "ী", "aa": "া",
    "a": "া", "i": "ি", "u": "ু", "e": "ে", "O": "ো",
    # "o" after a consonant is the inherent vowel → no matra emitted
}

_LATIN_CONSONANTS = {
    "chh": "ছ", "kh": "খ", "gh": "ঘ", "ng": "ং", "ch": "চ",
    "jh": "ঝ", "th": "থ", "dh": "ধ", "ph": "ফ", "bh": "ভ",
    "sh": "শ", "rh": "ঢ়",
    "k": "ক", "g": "গ", "j": "জ", "t": "ত", "d": "দ", "n": "ন",
    "p": "প", "b": "ব", "m": "ম", "r": "র", "l": "ল", "s": "স",
    "h": "হ", "y": "য়", "w": "ও", "v": "ভ", "f": "ফ", "z": "জ",
}

_HASANTA_CHAR = "্"

# Longest keys first so "chh" beats "ch" beats "h", etc.
_VOWEL_KEYS = sorted(set(_LATIN_INDEP) | set(_LATIN_MATRA) | {"o"}, key=len, reverse=True)
_CONS_KEYS = sorted(_LATIN_CONSONANTS, key=len, reverse=True)


def to_bengali(text: str) -> str:
    """Convert Latin "Banglish" to Bengali script (approximate, phonetic).

    A vowel after a consonant becomes a matra; at a word start it becomes an
    independent vowel. Two consonants in a row form a conjunct (joined with a
    hasanta). The vowel ``o`` after a consonant is treated as the inherent
    vowel and adds nothing.

    >>> to_bengali("bangla")
    'বাংলা'
    >>> to_bengali("ami")
    'আমি'
    """
    out: list[str] = []
    prev_consonant = False
    i = 0
    n = len(text)
    while i < n:
        # Try a consonant first.
        matched = None
        for key in _CONS_KEYS:
            if text.startswith(key, i):
                matched = key
                break
        if matched is not None:
            if prev_consonant:
                out.append(_HASANTA_CHAR)   # join into a conjunct
            out.append(_LATIN_CONSONANTS[matched])
            # "ng" is anusvara (a sign), not a true consonant base
            prev_consonant = matched != "ng"
            i += len(matched)
            continue

        # Then a vowel.
        matched = None
        for key in _VOWEL_KEYS:
            if text.startswith(key, i):
                matched = key
                break
        if matched is not None:
            if prev_consonant:
                if matched != "o":          # "o" = inherent vowel → nothing
                    out.append(_LATIN_MATRA.get(matched, ""))
            else:
                out.append(_LATIN_INDEP.get(matched, ""))
            prev_consonant = False
            i += len(matched)
            continue

        # Pass through anything we don't recognize.
        out.append(text[i])
        prev_consonant = False
        i += 1
    return "".join(out)
