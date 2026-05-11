"""Bengali word tokenizer.

Bengali writing uses spaces between words, but punctuation handling requires
care — particularly the daṇḍa (।) which ends sentences like a period.
"""

from __future__ import annotations
import re

# Bengali Unicode block: U+0980–U+09FF
# Bengali digits: ০-৯ (U+09E6–U+09EF)
# Also include ASCII digits and basic Latin for mixed text
_WORD_PATTERN = re.compile(
    r"[ঀ-৿]+"           # Bengali script run
    r"|[0-9০-৯]+"                 # ASCII or Bengali digits
    r"|[a-zA-Z]+"                 # ASCII words (for mixed text)
)

# Sentence-ending punctuation including Bengali daṇḍa
_SENT_SPLIT = re.compile(r"[।॥!?]+|\.{1,3}")


def tokenize(text: str) -> list[str]:
    """Tokenize Bengali text into words.

    Splits on whitespace and punctuation. Preserves Bengali script runs,
    digit sequences, and ASCII word runs. Drops punctuation tokens.

    Args:
        text: Bengali (or mixed) input string.

    Returns:
        List of token strings.
    """
    return _WORD_PATTERN.findall(text)


def sent_tokenize(text: str) -> list[str]:
    """Split text into sentences on Bengali/Latin sentence boundaries.

    Splits on: ।  ॥  .  !  ?  and their combinations.

    Args:
        text: Bengali (or mixed) input string.

    Returns:
        List of non-empty sentence strings.
    """
    parts = _SENT_SPLIT.split(text)
    return [s.strip() for s in parts if s.strip()]
