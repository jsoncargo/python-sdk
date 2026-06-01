# JSONCargo Python SDK

Python client for the JSONCargo container tracking API. See `AGENTS.md` for full project conventions.

## Commands

```bash
# Run tests
pytest tests/ -v

# Build package
python -m build

# Release to PyPI (bump version first, then tag)
git tag v0.1.x && git push origin v0.1.x
```

## Key facts

- `shipping_line` is **always required** for `track()` and `from_bol()` — never make it optional
- Container numbers must match ISO 6346: 4 uppercase letters + 7 digits (e.g. `MSCU1234567`)
- All HTTP errors map to custom exceptions in `jsoncargo/exceptions.py` — never let raw `requests` exceptions surface
- `__version__` in `jsoncargo/__init__.py` must stay in sync with `pyproject.toml`
- Tagging a release (e.g. `v0.1.2`) auto-publishes to PyPI via GitHub Actions
- Vessel methods (`basic`, `pro`, `bulk`, `specs`) require at least one of `uuid`, `mmsi`, or `imo`
- `vessels.finder()` uses `vessel_type` parameter (not `type`) to avoid shadowing the Python builtin
- `terminals.find()` requires `unlocode` of at least 2 non-whitespace characters
- Base URL uses HTTPS: `https://api.jsoncargo.com/api/v1`

## Structure

```
jsoncargo/client.py       # HTTP transport + error mapping; wires up all resources
jsoncargo/containers.py   # track() and from_bol() + input validation
jsoncargo/vessels.py      # basic(), pro(), bulk(), finder(), specs()
jsoncargo/ports.py        # find()
jsoncargo/terminals.py    # find()
jsoncargo/models.py       # Container, BolResult, VesselBasic, VesselPro,
                          # VesselBulkResult, VesselInfo, Port, Terminal
jsoncargo/exceptions.py   # JSONCargoError hierarchy
jsoncargo/__init__.py     # Public exports
tests/test_client.py      # 102 tests — always add tests for new behaviour
```
