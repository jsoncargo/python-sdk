# JSONCargo Python SDK

A lightweight Python client library for the [JSONCargo](https://jsoncargo.com) container tracking API.

## Project Overview

This is a minimal, well-tested Python SDK that wraps the JSONCargo REST API. The library provides:
- Container tracking by number and shipping line
- Bill of lading lookups
- API usage statistics

**Key constraint**: `shipping_line` is a **mandatory parameter** for all container operations.

## Project Structure

```
jsoncargo/
├── __init__.py           # Package exports (Client, Container, BolResult, all exceptions)
├── client.py             # Main Client class, HTTP transport, error handling
├── containers.py         # ContainersResource: track() and from_bol() + input validation
├── models.py             # Container and BolResult data models
└── exceptions.py         # Custom exception hierarchy

tests/
├── __init__.py
└── test_client.py        # 30 tests (no real API key or network required)

.github/
└── workflows/
    └── publish.yml       # Auto-publish to PyPI on version tag (e.g. v0.1.2)

pyproject.toml            # Package metadata and dependencies
README.md                 # User-facing documentation
```

## Important Conventions

### 1. Shipping Line is Mandatory
All container tracking operations require `shipping_line`:
- `track(tracking_number: str, shipping_line: str)` — always required
- `from_bol(bill_of_lading: str, shipping_line: str)` — always required

Valid values: `MAERSK`, `HAPAG_LLOYD`, `HMM`, `ONE`, `EVERGREEN`, `MSC`, `CMA_CGM`, `COSCO`, `ZIM`, `YANG_MING`, `PIL`

If omitted or invalid, a `ValueError` is raised immediately (before any HTTP call).

### 2. Input Validation
Container numbers are validated against ISO 6346 format: 4 uppercase letters + 7 digits (e.g. `MSCU1234567`). BOL numbers are checked for path traversal and URL-special characters (`/`, `\`, `..`, `%`, `#`, `?`, `&`, `+`, null bytes). Both checks happen in `containers.py` before the HTTP request is made.

### 3. Exception Hierarchy
All SDK exceptions live in `jsoncargo/exceptions.py` and are exported from the package root:

```
JSONCargoError          # base class
├── AuthenticationError # 401/403 — bad or missing API key
├── NotFoundError       # 404 — resource not found
├── RateLimitError      # 429 — rate limit exceeded
└── APIError            # everything else (5xx, timeouts, bad JSON)
    └── .status_code    # HTTP status code, if available
```

Callers should catch SDK exceptions, not `requests` exceptions.

### 4. Models Use Simple Data Classes
`Container` and `BolResult` are plain data classes that:
- Accept a `dict` in `__init__()`
- Use `.get()` to safely extract fields (defaults to `None`)
- Store the full raw response in `.raw`
- Implement `__repr__()` for debugging

### 5. Client Pattern
The `Client` class (`client.py`):
- Requires `api_key` at init (raises `ValueError` if empty)
- Accepts optional `timeout` (default 30s, pass `None` to disable)
- Uses `requests.Session` with `x-api-key` header
- All HTTP errors are mapped to custom exceptions in `_get()`
- Exposes `client.containers` and `client.stats()`

## Running Tests

```bash
pytest tests/ -v
```

Tests use `unittest.mock` — no real API key or network access needed.

## Build & Publish

```bash
pip install build twine
python -m build
python -m twine upload dist/*
```

## Release & Publishing

Tagging a release on GitHub automatically publishes the package to PyPI via `.github/workflows/publish.yml`.

1. Bump the version in `pyproject.toml` and `jsoncargo/__init__.py` (keep them in sync)
2. Commit and push
3. Create and push a version tag: `git tag v0.1.2 && git push origin v0.1.2`
4. The workflow builds and uploads to PyPI automatically

## Common Patterns

### Adding a New API Endpoint
1. Add a method to the appropriate `*Resource` class in `containers.py` (or a new resource file)
2. Call `self._client._get(path, params)` — it handles errors and returns the parsed JSON body
3. Extract `data["data"]` and return a model object
4. Add tests in `tests/test_client.py` using mocks
5. Update `README.md` and docstrings

### Adding a New Model Field
1. Add the field to the model class in `models.py`
2. Update the docstring
3. Update the README field table
4. Add a test verifying extraction

### Adding a New Exception Type
1. Add the class to `jsoncargo/exceptions.py` (subclass `JSONCargoError`)
2. Export it in `jsoncargo/__init__.py`
3. Map the relevant HTTP status code in `client.py _get()`

## Key Files

| File | Purpose | Edit when |
|---|---|---|
| `jsoncargo/client.py` | HTTP transport, error mapping | Changing auth, timeout, error handling |
| `jsoncargo/containers.py` | Container/BOL methods + validation | Adding/modifying track() or from_bol() |
| `jsoncargo/models.py` | Data classes | Adding new response fields |
| `jsoncargo/exceptions.py` | Custom exceptions | Adding new error types |
| `jsoncargo/__init__.py` | Package exports | Adding new public symbols |
| `tests/test_client.py` | Full test suite | Always — any change needs a test |
| `pyproject.toml` | Package metadata | Bumping version, adding dependencies |
| `README.md` | User docs | Any user-facing change |

## Development Notes

- **Python version**: 3.8+ (see `pyproject.toml`)
- **Dependencies**: Only `requests` (minimal footprint)
- **Versioning**: Keep `__version__` in `__init__.py` in sync with `pyproject.toml`
- **Commits**: Use conventional commits — `fix:`, `feat:`, `docs:`, `chore:`
