# JSONCargo Python SDK — Agent Reference

Python client for the [JSONCargo](https://jsoncargo.com) container tracking API.
It wraps a REST API for tracking containers, bills of lading, and vessels, and
for looking up ports and terminals.

## Getting started

```python
from jsoncargo import Client

client = Client("your_api_key")
```

`Client(api_key, base_url="https://api.jsoncargo.com/api/v1", timeout=30)` —
`api_key` is required (empty raises `ValueError`). Resources are reached as
`client.containers`, `client.vessels`, `client.ports`, `client.terminals`.
`client.stats()` returns a dict with `plan`, `requests_total`, `requests_made`,
`requests_available`.

## Public API surface

### `client.containers`

```python
track(tracking_number: str, shipping_line: str) -> Container
from_bol(bill_of_lading: str, shipping_line: str) -> BolResult
```

- `shipping_line` is **always required** for both methods.
- `tracking_number` must match ISO 6346: 4 uppercase letters + 7 digits
  (e.g. `MSCU1234567`).

### `client.vessels`

All keyword-only. `basic`, `pro`, `bulk`, and `specs` require **at least one** of
`uuid`, `mmsi`, or `imo`.

```python
basic(*, uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselBasic
pro(*,   uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselPro
bulk(*,  uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselBulkResult
specs(*, uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselInfo

finder(*, name=None, fuzzy=None, vessel_type=None, type_specific=None,
       country_iso=None, gross_tonnage_min=None, gross_tonnage_max=None,
       deadweight_min=None, deadweight_max=None, length_min=None, length_max=None,
       breadth_min=None, breadth_max=None, year_built_min=None, year_built_max=None,
       next=None, page=None, limit=None) -> list[VesselInfo]
```

- `finder()` requires at least one search parameter.
- Use `vessel_type` (not `type`) to filter by vessel type.

### `client.ports`

```python
find(*, lat=None, lon=None, radius=None, name=None, country_iso=None,
     port_type=None, fuzzy=None, page=None, limit=None) -> list[Port]
```

- Requires at least one search parameter.

### `client.terminals`

```python
find(unlocode: str, *, page=None, limit=None) -> list[Terminal]
```

- `unlocode` must be at least 2 non-whitespace characters.

## Constraints

- `shipping_line` is mandatory for `track()` and `from_bol()`, and must be one of:
  `MAERSK`, `HAPAG_LLOYD`, `HMM`, `ONE`, `EVERGREEN`, `MSC`, `CMA_CGM`, `COSCO`,
  `ZIM`, `YANG_MING`, `PIL`.
- Container numbers must match ISO 6346 (4 uppercase letters + 7 digits).
- `bill_of_lading` must not contain `/`, `\`, `%`, `#`, `?`, `&`, `+`, null bytes, or `..` sequences (rejected before any request).
- Vessel `basic`/`pro`/`bulk`/`specs` require at least one of `uuid`, `mmsi`, `imo`.
- `vessels.finder()` and `ports.find()` require at least one search parameter.
- `terminals.find()` requires `unlocode` of at least 2 non-whitespace characters.
- Invalid arguments raise `ValueError` before any request is made.

## Exceptions

All SDK errors derive from `JSONCargoError`. Catch these instead of `requests`
exceptions — HTTP and network failures are always mapped to one of these.

```
JSONCargoError          # base class
├── AuthenticationError # invalid or missing API key (HTTP 401/403)
├── NotFoundError       # resource not found (HTTP 404)
├── RateLimitError      # rate limit exceeded (HTTP 429)
└── APIError            # everything else (5xx, timeouts, bad/malformed JSON);
                        #   has a .status_code attribute (may be None)
```

## Models

Every model exposes a `raw` dict with the full response payload.

- `Container` — full container tracking: `container_id`, `container_type`,
  `status` (maps from the `container_status` raw key), `tare`, shipping line,
  origin/destination, ATD/ETA, last/next location, loading/discharging ports,
  vessel and voyage info, `bill_of_lading`, `customs_clearance`, `last_updated`.
- `BolResult` — `bill_of_lading`, `shipping_line_name`, `shipping_line_id`,
  `associated_containers` (count), `associated_container_numbers` (list of str),
  `last_updated`.
- `VesselBasic` — identity (`uuid`, `name`, `mmsi`, `imo`, `eni`, `country_iso`),
  type (`type`, `type_specific`), position (`lat`, `lon`, `speed`, `course`,
  `heading`), navigation status, destination, last position and ETA timestamps.
- `VesselPro` — superset of `VesselBasic` adding `current_draught`,
  `dest_port_uuid`, `dest_port`, `dest_port_unlocode`, `dep_port_uuid`,
  `dep_port`, `dep_port_unlocode`, `atd_epoch`, `atd_UTC`, `timezone_offset_sec`,
  `timezone`.
- `VesselBulkResult` — `total` (int) and `vessels` (list of `VesselBasic`).
- `VesselInfo` — full vessel specification: identity (`uuid`, `name`, `name_ais`,
  `mmsi`, `imo`, `eni`, `country_iso`, `country_name`, `callsign`), type,
  tonnage/deadweight/TEU, `liquid_gas`, dimensions, draught stats (`draught_avg`,
  `draught_max`), speed stats (`speed_avg`, `speed_max`), `year_built`,
  `is_navaid`, `home_port`. Returned by `finder()` and `specs()`.
- `Port` — `uuid`, `name`, `unlocode`, `type`, `size`, `area`, `area_lvl1`,
  `area_lvl2`, `city`, `country_iso`, `country_name`, location (`lat`, `lon`).
- `Terminal` — `unlocode`, `alt_unlocode`, `code`, `terminal_name`,
  `company_name`, location, `url`, `address`.

## File structure

```
jsoncargo/client.py       # Client + resource wiring
jsoncargo/containers.py   # track(), from_bol()
jsoncargo/vessels.py      # basic(), pro(), bulk(), finder(), specs()
jsoncargo/ports.py        # find()
jsoncargo/terminals.py    # find()
jsoncargo/models.py       # Container, BolResult, VesselBasic, VesselPro,
                          # VesselBulkResult, VesselInfo, Port, Terminal
jsoncargo/exceptions.py   # JSONCargoError hierarchy
jsoncargo/__init__.py     # Public exports
```
