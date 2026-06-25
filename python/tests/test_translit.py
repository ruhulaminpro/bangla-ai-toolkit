"""Tests for numeral conversion and transliteration."""

from bangla_ai import text


# ── Numerals ──────────────────────────────────────────────────────────────────

def test_bengali_to_english_digits():
    assert text.to_english_digits("২০২৪") == "2024"
    assert text.to_english_digits("৫টি আপেল") == "5টি আপেল"


def test_english_to_bengali_digits():
    assert text.to_bengali_digits("2024") == "২০২৪"
    assert text.to_bengali_digits("page 7") == "page ৭"


def test_digit_roundtrip():
    s = "১২৩৪৫৬৭৮৯০"
    assert text.to_bengali_digits(text.to_english_digits(s)) == s


def test_non_digits_untouched():
    assert text.to_english_digits("বাংলা") == "বাংলা"
    assert text.to_bengali_digits("hello") == "hello"


# ── Bengali → Latin ───────────────────────────────────────────────────────────

def test_to_latin_common_words():
    assert text.to_latin("বাংলা") == "bangla"
    assert text.to_latin("ঢাকা") == "dhaka"
    assert text.to_latin("আমি") == "ami"
    assert text.to_latin("কলম") == "kolom"


def test_to_latin_drops_final_schwa():
    # The inherent vowel must not appear on a word-final consonant.
    assert text.to_latin("বাংলাদেশ") == "bangladesh"
    assert text.to_latin("মন") == "mon"


def test_to_latin_keeps_matra():
    assert text.to_latin("ভালো") == "bhalo"


def test_to_latin_passthrough():
    assert text.to_latin("ঢাকা 2024") == "dhaka 2024"


# ── Latin → Bengali ───────────────────────────────────────────────────────────

def test_to_bengali_common_words():
    assert text.to_bengali("bangla") == "বাংলা"
    assert text.to_bengali("ami") == "আমি"
    assert text.to_bengali("kolom") == "কলম"
    assert text.to_bengali("amar") == "আমার"


def test_to_bengali_conjunct():
    # Two consonants in a row join with a hasanta.
    assert "্" in text.to_bengali("dhonnobad")


def test_to_bengali_passthrough():
    assert text.to_bengali("bangla 2024") == "বাংলা 2024"
