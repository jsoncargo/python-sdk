# JSONCargo Python SDK

Python client for the JSONCargo container tracking API. See `AGENTS.md` for full project conventions.

## Commands

```bash
# Run tests
pytest tests/ -v

# Build package
python -m build

# Publish to PyPI
python -m twine upload dist/*
```

## Key facts

- `shipping_line` is **always required** for `track()` and `from_bol()` — never make it optional
- Container numbers must match ISO 6346: 4 uppercase letters + 7 digits (e.g. `MSCU1234567`)
- All HTTP errors map to custom exceptions in `jsoncargo/exceptions.py` — never let raw `requests` exceptions surface
- `__version__` in `jsoncargo/__init__.py` must stay in sync with `pyproject.toml`
- Pushing to `main` auto-deploys to the production server via GitHub Actions

## Structure

```
jsoncargo/client.py       # HTTP transport + error mapping
jsoncargo/containers.py   # track() and from_bol() + input validation
jsoncargo/models.py       # Container and BolResult data classes
jsoncargo/exceptions.py   # JSONCargoError hierarchy
jsoncargo/__init__.py     # Public exports
tests/test_client.py      # 24 tests — always add tests for new behaviour
```
