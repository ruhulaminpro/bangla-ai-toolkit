# Contributing

## Setup

```bash
# Python
cd python
pip install -e ".[dev]"

# JavaScript
cd javascript
npm install
```

## Running tests

```bash
# Python
cd python && OPENAI_API_KEY=sk-... pytest tests/ -v

# JavaScript
cd javascript && OPENAI_API_KEY=sk-... npm test
```

## Adding a new feature

1. Add module in `python/bangla_ai/` and `javascript/src/`
2. Export from `__init__.py` / `index.js`
3. Add tests in `tests/`
4. Update `docs/API.md`

## Code style

- Python: follow PEP 8, type hints on all public signatures
- JavaScript: ES modules, JSDoc on public methods

## Pull requests

- One feature per PR
- Tests required for new functionality
- Update README if public API changes
