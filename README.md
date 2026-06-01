# JSONCargo Python SDK — Shipping Container Tracking API Client

[![PyPI version](https://img.shields.io/pypi/v/jsoncargo.svg)](https://pypi.org/project/jsoncargo/)
[![Python versions](https://img.shields.io/pypi/pyversions/jsoncargo.svg)](https://pypi.org/project/jsoncargo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [JSONCargo](https://jsoncargo.com) container tracking API. Track shipping containers by number, look up bills of lading, track vessels in real time, search ports and terminals, and monitor your API usage — all with a single `pip install`.

```bash
pip install jsoncargo
```

Full API documentation: [jsoncargo.com/documentation-api](https://jsoncargo.com/documentation-api/)

---

## Features

- **Container tracking** — track any shipping container by number and carrier
- **Bill of lading lookup** — retrieve all containers linked to a BOL number
- **Vessel tracking** — real-time AIS position, speed, heading, ETA (basic and pro)
- **Bulk vessel tracking** — query up to 100 vessels in a single API call
- **Vessel finder** — search vessels by name, type, country, tonnage, or dimensions
- **Vessel specs** — static technical specifications by IMO, MMSI, or UUID
- **Port finder** — find ports by name, UN/LOCODE, coordinates, or country
- **Terminal finder** — look up container terminals by UN/LOCODE
- **API usage stats** — monitor your plan limits and remaining requests

---

## Requirements

Python 3.8 or higher. The only dependency is [`requests`](https://pypi.org/project/requests/).

---

## Installation

```bash
pip install jsoncargo
```

---

## Quick Start

```python
import os
from jsoncargo import Client

client = Client(os.environ["JSONCARGO_API_KEY"])

# Track a shipping container
container = client.containers.track("MSCU1234567", shipping_line="MSC")
print(container.status)               # In Transit
print(container.eta_final_destination) # 2024-08-01 00:00
```

Store your API key in an environment variable rather than hardcoding it in source code.

---

## Container Tracking

### Track a container by number

`shipping_line` is always required. Supported carriers: `MAERSK`, `HAPAG_LLOYD`, `HMM`, `ONE`, `EVERGREEN`, `MSC`, `CMA_CGM`, `COSCO`, `ZIM`, `YANG_MING`, `PIL`

```python
container = client.containers.track("MSCU1234567", shipping_line="MSC")

print(container.container_id)           # MSCU1234567
print(container.status)                 # In Transit
print(container.shipped_from)           # SHANGHAI, CN
print(container.shipped_to)             # ROTTERDAM, NL
print(container.eta_final_destination)  # 2024-08-01 00:00
print(container.current_vessel_name)    # MSC LENA F
print(container.loading_port)           # SHANGHAI
print(container.discharging_port)       # ROTTERDAM
```

### Bill of lading lookup

Retrieve all containers associated with a bill of lading number. `shipping_line` is required.

```python
result = client.containers.from_bol("SELM60819800", shipping_line="HMM")

print(result.bill_of_lading)               # SELM60819800
print(result.associated_containers)        # 16
print(result.associated_container_numbers) # ['CAIU9933760', 'HMMU6053862', ...]
```

---

## Vessel Tracking

### Basic vessel tracking

Real-time AIS position, speed, heading, and ETA. Pass at least one of `uuid`, `mmsi`, or `imo`.

```python
vessel = client.vessels.basic(mmsi="566093000")

print(vessel.name)              # MAERSK CHENNAI
print(vessel.lat)               # 5.51935
print(vessel.lon)               # 0.02906167
print(vessel.speed)             # 0.1
print(vessel.destination)       # CGPNR>GHTEM
print(vessel.eta_UTC)           # 2024-07-22T07:39:00Z
print(vessel.navigation_status) # Moored
```

### Pro vessel tracking

Extended AIS data including actual departure, destination port details, draught, and timezone.

```python
vessel = client.vessels.pro(imo="9525338")

print(vessel.dest_port)           # TEMA
print(vessel.dest_port_unlocode)  # GHTEM
print(vessel.dep_port)            # POINTE NOIRE
print(vessel.current_draught)     # 12.9
print(vessel.atd_UTC)             # 2024-07-19T12:13:00Z
print(vessel.timezone)            # GMT
```

### Bulk vessel tracking

Track up to 100 vessels in a single API call using comma-separated MMSI or IMO numbers.

```python
result = client.vessels.bulk(mmsi="566093000,235362000")

print(result.total)  # 2
for v in result.vessels:
    print(v.name, v.lat, v.lon)
```

### Vessel finder

Search the global vessel database by name, type, flag country, gross tonnage, deadweight, dimensions, or year built.

```python
# Search by name
vessels = client.vessels.finder(name="MAERSK CHENNAI")

for v in vessels:
    print(v.name, v.imo, v.gross_tonnage)

# Filter by vessel type, country, and minimum tonnage
vessels = client.vessels.finder(
    vessel_type="Cargo",
    country_iso="SG",
    gross_tonnage_min=40000,
)
```

Use `vessel_type` (not `type`) to avoid shadowing Python's built-in.

### Vessel specifications

Static technical specifications — dimensions, capacity, build year, and identifiers.

```python
info = client.vessels.specs(imo="9525338")

print(info.name)          # MAERSK CHENNAI
print(info.gross_tonnage) # 50869
print(info.teu)           # 4500
print(info.length)        # 249.12
print(info.breadth)       # 37.3
print(info.year_built)    # 2011
print(info.home_port)     # SINGAPORE
```

---

## Ports

### Find ports

Search for ports by name, UN/LOCODE, GPS coordinates, country, or port type.

```python
# Search by name
ports = client.ports.find(name="LONDON")

for p in ports:
    print(p.port_name, p.unlocode, p.lat, p.lon)

# Radius search — ports within 50 km of a coordinate
ports = client.ports.find(lat=51.5, lon=-0.05, radius=50)

# Filter by country
ports = client.ports.find(country_iso="GB", port_type="Seaport")
```

---

## Terminals

### Find container terminals

Look up container terminals by UN/LOCODE (minimum 2 characters).

```python
terminals = client.terminals.find("CNCQI")

for t in terminals:
    print(t.terminal_name, t.company_name)
    print(t.unlocode, t.lat, t.lon)
    print(t.address)
```

---

## API Key Usage Statistics

Monitor your plan limits, total requests, and remaining quota.

```python
stats = client.stats()

print(stats["plan"])                # MARINER
print(stats["requests_total"])      # 2000
print(stats["requests_made"])       # 47
print(stats["requests_available"])  # 1953
```

---

## Error Handling

All errors raise SDK-specific exceptions — never raw `requests` exceptions.

```python
from jsoncargo import (
    Client,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    APIError,
)

client = Client(os.environ["JSONCARGO_API_KEY"])

try:
    container = client.containers.track("MSCU1234567", shipping_line="MSC")
except AuthenticationError:
    print("Invalid or missing API key")
except NotFoundError:
    print("Container not found")
except RateLimitError:
    print("Rate limit exceeded — try again later")
except APIError as e:
    print(f"API error {e.status_code}: {e}")
```

| Exception | HTTP status | Cause |
|---|---|---|
| `AuthenticationError` | 401, 403 | Invalid or missing API key |
| `NotFoundError` | 404 | Resource not found |
| `RateLimitError` | 429 | Rate limit exceeded |
| `APIError` | 5xx, timeout | Server error or network issue |

---

## Timeout Configuration

The default timeout is 30 seconds.

```python
client = Client("your_api_key", timeout=60)   # 60-second timeout
client = Client("your_api_key", timeout=None) # disable timeout
```

---

## Model Field Reference

### Container

| Field | Type | Description |
|---|---|---|
| `container_id` | str | Container number (ISO 6346) |
| `container_type` | str | Container type |
| `status` | str | Current tracking status |
| `shipping_line_name` | str | Full carrier name |
| `shipping_line_id` | str | Internal carrier ID |
| `tare` | float | Tare weight (kg) |
| `shipped_from` | str | Origin location |
| `shipped_from_terminal` | str | Origin terminal |
| `shipped_to` | str | Destination location |
| `shipped_to_terminal` | str | Destination terminal |
| `atd_origin` | str | Actual departure from origin |
| `eta_final_destination` | str | ETA at final destination |
| `last_location` | str | Most recent location |
| `next_location` | str | Next expected location |
| `loading_port` | str | Port of loading |
| `discharging_port` | str | Port of discharge |
| `bill_of_lading` | str | Associated BOL number |
| `current_vessel_name` | str | Current carrying vessel |
| `current_voyage_number` | str | Current voyage number |
| `last_updated` | str | Data last refreshed |
| `raw` | dict | Full raw API response |

### VesselBasic

| Field | Type | Description |
|---|---|---|
| `uuid` | str | Internal vessel UUID |
| `name` | str | Vessel name |
| `mmsi` | str | MMSI number |
| `imo` | str | IMO number |
| `eni` | str | European inland vessel ID |
| `country_iso` | str | Flag country ISO code |
| `type` | str | Vessel type |
| `type_specific` | str | Specific vessel subtype |
| `lat` | float | Latitude |
| `lon` | float | Longitude |
| `speed` | float | Speed over ground (knots) |
| `course` | float | Course over ground |
| `heading` | float | True heading |
| `navigation_status` | str | AIS navigation status |
| `destination` | str | Reported destination |
| `last_position_epoch` | int | Last position timestamp (epoch) |
| `last_position_UTC` | str | Last position timestamp (UTC) |
| `eta_epoch` | int | ETA (epoch) |
| `eta_UTC` | str | ETA (UTC) |
| `raw` | dict | Full raw API response |

### VesselPro

All `VesselBasic` fields, plus:

| Field | Type | Description |
|---|---|---|
| `current_draught` | float | Current draught (m) |
| `dest_port_uuid` | str | Destination port UUID |
| `dest_port` | str | Destination port name |
| `dest_port_unlocode` | str | Destination port UN/LOCODE |
| `dep_port_uuid` | str | Departure port UUID |
| `dep_port` | str | Departure port name |
| `dep_port_unlocode` | str | Departure port UN/LOCODE |
| `atd_epoch` | int | Actual departure (epoch) |
| `atd_UTC` | str | Actual departure (UTC) |
| `timezone_offset_sec` | int | Timezone offset (seconds) |
| `timezone` | str | Timezone name |

### VesselInfo (finder / specs)

| Field | Type | Description |
|---|---|---|
| `uuid` | str | Internal vessel UUID |
| `name` | str | Vessel name |
| `name_ais` | str | AIS-broadcast name |
| `mmsi` | str | MMSI number |
| `imo` | str | IMO number |
| `eni` | str | European inland vessel ID |
| `country_iso` | str | Flag country ISO code |
| `country_name` | str | Flag country name |
| `callsign` | str | Radio callsign |
| `type` | str | Vessel type |
| `type_specific` | str | Specific vessel subtype |
| `gross_tonnage` | int | Gross tonnage |
| `deadweight` | int | Deadweight tonnage (DWT) |
| `teu` | int | TEU capacity |
| `liquid_gas` | float | Liquid gas capacity |
| `length` | float | Overall length (m) |
| `breadth` | float | Breadth (m) |
| `draught_avg` | float | Average draught (m) |
| `draught_max` | float | Maximum draught (m) |
| `speed_avg` | float | Average speed (knots) |
| `speed_max` | float | Maximum speed (knots) |
| `year_built` | int | Year built |
| `is_navaid` | bool | Whether vessel is a navigation aid |
| `home_port` | str | Home port |
| `raw` | dict | Full raw API response |

### Port

| Field | Type | Description |
|---|---|---|
| `port_name` | str | Port name |
| `port_code` | str | Port code |
| `unlocode` | str | UN/LOCODE |
| `country` | str | Country |
| `country_iso` | str | Country ISO code |
| `country_name` | str | Country name |
| `lat` | float | Latitude |
| `lon` | float | Longitude |
| `port_type` | str | Port type |
| `size` | str | Port size classification |
| `area` | str | Geographic area |
| `area_lvl1` | str | Area level 1 |
| `area_lvl2` | str | Area level 2 |
| `city` | str | City |
| `raw` | dict | Full raw API response |

### Terminal

| Field | Type | Description |
|---|---|---|
| `unlocode` | str | UN/LOCODE |
| `alt_unlocode` | str | Alternative UN/LOCODE |
| `code` | str | Terminal code |
| `terminal_name` | str | Terminal name |
| `company_name` | str | Operating company |
| `lat` | float | Latitude |
| `lon` | float | Longitude |
| `url` | str | Terminal website |
| `address` | str | Terminal address |
| `raw` | dict | Full raw API response |

---

## License

MIT — see [LICENSE](LICENSE) for details.
