"""Tests for text utilities — no API key, no network required."""

from bangla_ai.text import normalize, tokenize, sent_tokenize, remove_stopwords, stem, stem_tokens, STOPWORDS


def test_normalize_nfc():
    # ড (U+09A1) + ় nukta (U+09BC) should compose to ড় (U+09DC)
    decomposed = "ড়"
    result = normalize(decomposed)
    assert result == "ড়"


def test_normalize_strips_zero_width():
    text = "বাংলা​টেক্সট"  # zero-width space in middle
    assert "​" not in normalize(text)


def test_normalize_collapses_spaces():
    assert normalize("বাংলা  টেক্সট") == "বাংলা টেক্সট"


def test_tokenize_basic():
    tokens = tokenize("আমি বাংলায় কথা বলি।")
    assert "আমি" in tokens
    assert "বাংলায়" in tokens
    assert "।" not in tokens  # punctuation dropped


def test_tokenize_mixed():
    tokens = tokenize("LXNotes ২০২৪ সালে শুরু হয়।")
    assert "LXNotes" in tokens
    assert "২০২৪" in tokens


def test_sent_tokenize():
    text = "আমি বাংলায় কথা বলি। তুমি কেমন আছ? আমি ভালো আছি।"
    sents = sent_tokenize(text)
    assert len(sents) == 3


def test_remove_stopwords():
    tokens = tokenize("আমি বাংলাদেশে যাই।")
    filtered = remove_stopwords(tokens)
    assert "আমি" not in filtered
    assert "বাংলাদেশে" in filtered


def test_stopwords_nonempty():
    assert len(STOPWORDS) > 50


def test_stem_verbal_suffix():
    assert stem("করেছেন") == "কর"


def test_stem_nominal_suffix():
    assert stem("বাংলাদেশের") == "বাংলাদেশ"


def test_stem_no_change():
    assert stem("বই") == "বই"


def test_stem_tokens():
    result = stem_tokens(["করেছেন", "বই", "দেশের"])
    assert result == ["কর", "বই", "দেশ"]
