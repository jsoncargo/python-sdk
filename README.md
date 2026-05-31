# Container Tracking Python SDK Library

The official Python SDK for the [JSONCargo](https://jsoncargo.com) container tracking API. Track shipping containers, look up bills of lading, and monitor API usage — all from Python with a single `pip install`.

```bash
pip install jsoncargo
```

Full API documentation: [jsoncargo.com/documentation-api](https://jsoncargo.com/documentation-api/)

## Requirements

Python 3.8 or higher.

## Setup

```python
from jsoncargo import Client

client = Client("your_api_key")
```

Store your API key in an environment variable rather than hardcoding it:

```python
import os
from jsoncargo import Client

client = Client(os.environ["JSONCARGO_API_KEY"])
```

## Track a container

`shipping_line` is always required.

```python
container = client.containers.track("MSCU1234567", shipping_line="MSC")

print(container.container_id)           # MSCU1234567
print(container.status)                 # In Transit
print(container.shipped_from)           # SHANGHAI, CN
print(container.shipped_to)             # ROTTERDAM, NL
print(container.eta_final_destination)  # 2024-08-01 00:00
print(container.current_vessel_name)    # MSC LENA F
```

Valid shipping line values: `MAERSK`, `HAPAG_LLOYD`, `HMM`, `ONE`, `EVERGREEN`, `MSC`, `CMA_CGM`, `COSCO`, `ZIM`, `YANG_MING`, `PIL`

## Get containers from a bill of lading

`shipping_line` is always required for bill of lading lookups.

```python
result = client.containers.from_bol("SELM60819800", shipping_line="HMM")

print(result.bill_of_lading)               # SELM60819800
print(result.associated_containers)        # 16
print(result.associated_container_numbers) # ['CAIU9933760', 'HMMU6053862', ...]
```

## Check API key usage

```python
stats = client.stats()

print(stats["plan"])                # MARINER
print(stats["requests_total"])      # 2000
print(stats["requests_made"])       # 47
print(stats["requests_available"])  # 1953
```

## Error handling

```python
from jsoncargo import Client, AuthenticationError, NotFoundError, RateLimitError, APIError

client = Client(os.environ["JSONCARGO_API_KEY"])

try:
    container = client.containers.track("MSCU1234567", shipping_line="MSC")
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Container not found")
except RateLimitError:
    print("Rate limit exceeded — try again later")
except APIError as e:
    print(f"API error {e.status_code}: {e}")
```

## Timeout

By default the client times out after 30 seconds. Pass `timeout` to override:

```python
client = Client("your_api_key", timeout=60)   # 60-second timeout
client = Client("your_api_key", timeout=None) # no timeout
```

## Container fields

| Field | Type | Description |
|---|---|---|
| `container_id` | str | Container number |
| `container_type` | str | Container type |
| `status` | str | Current status |
| `shipping_line_name` | str | Full shipping line name |
| `shipping_line_id` | str | Internal shipping line ID |
| `tare` | float | Tare weight in kg |
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
| `current_vessel_name` | str | Current vessel |
| `current_voyage_number` | str | Current voyage |
| `last_updated` | str | Data last refreshed |
| `raw` | dict | Full raw API response |

## License

MIT
