# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0]

### Added
- **Transliteration**: `to_latin` (Bengali→Latin romanization with schwa
  deletion) and `to_bengali` (Latin "Banglish"→Bengali phonetic input).
- **Numerals**: `to_english_digits` / `to_bengali_digits` (০-৯ ↔ 0-9).
- **NER**: `BanglaAI.ner` on both backends (OpenAI structured output;
  HuggingFace token-classification).
- **Embeddings & semantic search**: `BanglaAI.embed` and
  `BanglaAI.semantic_search`, plus zero-dependency `cosine_similarity` /
  `rank_by_similarity` helpers.
- **CLI**: `bangla-ai` command (text utilities + ML tasks) in both Python and
  JavaScript.
- **Types**: `py.typed` marker (Python) and `index.d.ts` (TypeScript).
- **Benchmarks**: evaluation harness (`python -m benchmarks.run`) with
  token-F1 / accuracy metrics and a bundled Bengali dataset.

### Fixed
- `pyproject.toml` build backend corrected to `setuptools.build_meta` so the
  package builds and publishes to PyPI.

### Packaging
- Per-package READMEs (`python/`, `javascript/`) so PyPI and npm render full
  descriptions.
- GitHub Actions CI running the Python and JavaScript test suites plus a
  Python build + `twine check`.
- npm `files` allowlist (ships only `src/` + `bin/`); added `engines`,
  `homepage`, `bugs`, `bin`, `types`.
- Status badges, `CHANGELOG.md`, and `ROADMAP.md`.

## [0.2.0]

### Added
- Model-agnostic architecture with pluggable backends (`transformers`, `openai`,
  or any custom `Backend`).
- Zero-dependency Bengali text utilities: `normalize`, `tokenize`,
  `sent_tokenize`, `remove_stopwords`, `stem`.
- ML tasks: `summarize`, `qa`, `sentiment`.
- Python and JavaScript implementations with matching APIs.
