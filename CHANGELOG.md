# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- `pyproject.toml` build backend corrected to `setuptools.build_meta` so the
  package builds and publishes to PyPI.

### Added
- Per-package READMEs (`python/`, `javascript/`) so PyPI and npm render full
  descriptions.
- GitHub Actions CI running the Python and JavaScript test suites.
- `CHANGELOG.md` and `ROADMAP.md`.
- npm `files` allowlist so published tarball ships only `src/`.

## [0.2.0]

### Added
- Model-agnostic architecture with pluggable backends (`transformers`, `openai`,
  or any custom `Backend`).
- Zero-dependency Bengali text utilities: `normalize`, `tokenize`,
  `sent_tokenize`, `remove_stopwords`, `stem`.
- ML tasks: `summarize`, `qa`, `sentiment`.
- Python and JavaScript implementations with matching APIs.
