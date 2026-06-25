"""Bengali numeral conversion.

Bengali uses its own digit glyphs (০-৯, U+09E6–U+09EF). These utilities
convert between Bengali and ASCII (Western Arabic) digits in both directions,
leaving all non-digit characters untouched.
"""

from __future__ import annotations

_BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
_ASCII_DIGITS = "0123456789"

_BN_TO_EN = str.maketrans(_BENGALI_DIGITS, _ASCII_DIGITS)
_EN_TO_BN = str.maketrans(_ASCII_DIGITS, _BENGALI_DIGITS)


def to_english_digits(text: str) -> str:
    """Convert Bengali digits (০-৯) to ASCII digits (0-9).

    >>> to_english_digits("২০২৪ সালে")
    '2024 সালে'
    """
    return text.translate(_BN_TO_EN)


def to_bengali_digits(text: str) -> str:
    """Convert ASCII digits (0-9) to Bengali digits (০-৯).

    >>> to_bengali_digits("2024 সালে")
    '২০২৪ সালে'
    """
    return text.translate(_EN_TO_BN)
