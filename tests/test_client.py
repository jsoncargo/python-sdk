import pytest
from unittest.mock import patch, MagicMock
import requests
from jsoncargo import (
    Client, Container, BolResult, VesselBasic, VesselPro, VesselBulkResult,
    VesselInfo, Port, Terminal,
    AuthenticationError, NotFoundError, RateLimitError, APIError,
)


MOCK_CONTAINER = {
    "data": {
        "container_id": "MSCU1234567",
        "container_type": "40' HIGH CUBE",
        "container_status": "In Transit",
        "shipping_line_name": "Mediterranean Shipping Company",
        "shipping_line_id": "0015",
        "tare": 3900,
        "shipped_from": "SHANGHAI, CN",
        "shipped_from_terminal": "YANGSHAN TERMINAL",
        "shipped_to": "ROTTERDAM, NL",
        "shipped_to_terminal": "ECT DELTA TERMINAL",
        "atd_origin": "2024-07-01 00:00",
        "eta_final_destination": "2024-08-01 00:00",
        "last_location": "SINGAPORE, SG",
        "last_location_terminal": "PSA TERMINAL",
        "next_location": "PORT KLANG, MY",
        "next_location_terminal": "WESTPORT",
        "atd_last_location": "2024-07-10 00:00",
        "eta_next_destination": "2024-07-12 00:00",
        "timestamp_of_last_location": "2024-07-10 06:00",
        "last_movement_timestamp": "2024-07-10 06:00",
        "loading_port": "SHANGHAI, CN",
        "discharging_port": "ROTTERDAM, NL",
        "customs_clearance": None,
        "bill_of_lading": "MSCUBL123456",
        "last_vessel_name": "MSC LENA F",
        "last_voyage_number": "YF432A",
        "current_vessel_name": "MSC LENA F",
        "current_voyage_number": "YF432A",
        "last_updated": "2024-07-10 18:00",
    }
}

MOCK_BOL = {
    "data": {
        "bill_of_lading": "SELM60819800",
        "shipping_line_name": "Hyundai Merchant Marine",
        "shipping_line_id": "0012",
        "associated_containers": 3,
        "associated_container_numbers": ["HMMU1234567", "HMMU7654321", "KOCU1234567"],
        "last_updated": "2025-03-28 04:09",
    }
}


MOCK_VESSEL_BASIC = {
    "data": {
        "uuid": "abc-123",
        "name": "MSC LENA F",
        "mmsi": "636017123",
        "imo": "9876543",
        "eni": None,
        "country_iso": "LR",
        "type": "Cargo",
        "type_specific": "Container Ship",
        "lat": 1.234,
        "lon": 103.456,
        "speed": 12.3,
        "course": 90.0,
        "heading": 91,
        "navigation_status": "Under way using engine",
        "destination": "ROTTERDAM",
        "last_position_epoch": 1719500000,
        "last_position_UTC": "2024-06-27 12:00:00",
        "eta_epoch": 1720000000,
        "eta_UTC": "2024-07-03 06:00:00",
    }
}

MOCK_VESSEL_PRO = {
    "data": {
        "uuid": "abc-123",
        "name": "MSC LENA F",
        "mmsi": "636017123",
        "imo": "9876543",
        "eni": None,
        "country_iso": "LR",
        "type": "Cargo",
        "type_specific": "Container Ship",
        "lat": 1.234,
        "lon": 103.456,
        "speed": 12.3,
        "course": 90.0,
        "heading": 91,
        "navigation_status": "Under way using engine",
        "destination": "ROTTERDAM",
        "last_position_epoch": 1719500000,
        "last_position_UTC": "2024-06-27 12:00:00",
        "eta_epoch": 1720000000,
        "eta_UTC": "2024-07-03 06:00:00",
        "current_draught": 14.5,
        "dest_port_uuid": "port-789",
        "dest_port": "ROTTERDAM",
        "dest_port_unlocode": "NLRTM",
        "dep_port_uuid": "port-456",
        "dep_port": "SINGAPORE",
        "dep_port_unlocode": "SGSIN",
        "atd_epoch": 1719000000,
        "atd_UTC": "2024-06-21 18:00:00",
        "timezone_offset_sec": 3600,
        "timezone": "Europe/Amsterdam",
    }
}

MOCK_VESSEL_BULK = {
    "data": {
        "total": 2,
        "vessels": [
            MOCK_VESSEL_BASIC["data"],
            {**MOCK_VESSEL_BASIC["data"], "eta_epoch": None, "eta_UTC": None},
        ],
    }
}

MOCK_VESSEL_INFO = {
    "uuid": "abc-123",
    "name": "MSC LENA F",
    "name_ais": "MSC LENA F",
    "mmsi": "636017123",
    "imo": "9876543",
    "eni": None,
    "country_iso": "LR",
    "country_name": "Liberia",
    "callsign": "D5XX",
    "type": "Cargo",
    "type_specific": "Container Ship",
    "gross_tonnage": 95000,
    "deadweight": 110000,
    "teu": 9000,
    "liquid_gas": None,
    "length": 299.9,
    "breadth": 48.2,
    "draught_avg": 13.5,
    "draught_max": 14.5,
    "speed_avg": 14.0,
    "speed_max": 22.0,
    "year_built": 2015,
    "is_navaid": False,
    "home_port": "MONROVIA",
}

MOCK_VESSEL_FINDER = {"data": [MOCK_VESSEL_INFO]}

MOCK_VESSEL_SPECS = {"data": MOCK_VESSEL_INFO}

MOCK_PORT_FIND = {
    "data": [
        {
            "port_name": "ROTTERDAM",
            "port_code": "RTM",
            "country": "Netherlands",
            "lat": 51.95,
            "lon": 4.13,
            "port_type": "Seaport",
            "size": "Large",
            "area": "Europe",
            "city": "Rotterdam",
            "unlocode": "NLRTM",
            "uuid": "port-789",
            "country_iso": "NL",
            "country_name": "Netherlands",
            "area_lvl1": "Western Europe",
            "area_lvl2": "North Sea",
        }
    ]
}

MOCK_TERMINAL_FIND = {
    "data": [
        {
            "unlocode": "NLRTM",
            "alt_unlocode": None,
            "code": "ECTDELTA",
            "terminal_name": "ECT DELTA TERMINAL",
            "company_name": "Hutchison Ports ECT",
            "lat": 51.95,
            "lon": 4.05,
            "url": "https://example.com",
            "address": "Europaweg 875, Rotterdam",
        }
    ]
}


def make_mock_response(data, status_code=200):
    mock = MagicMock()
    mock.json.return_value = data
    mock.raise_for_status.return_value = None
    mock.status_code = status_code
    mock.ok = status_code < 400
    mock.reason = "OK"
    return mock


def make_error_response(status_code, reason="Error", json_body=None):
    mock = MagicMock()
    mock.status_code = status_code
    mock.ok = False
    mock.reason = reason
    if json_body is not None:
        mock.json.return_value = json_body
    else:
        mock.json.side_effect = ValueError("no json")
    return mock


class TestClient:
    def test_requires_api_key(self):
        with pytest.raises(ValueError):
            Client("")

    def test_containers_resource_available(self):
        client = Client("test_key")
        assert client.containers is not None

    def test_vessels_resource_available(self):
        client = Client("test_key")
        assert client.vessels is not None

    def test_ports_resource_available(self):
        client = Client("test_key")
        assert client.ports is not None

    def test_terminals_resource_available(self):
        client = Client("test_key")
        assert client.terminals is not None

    def test_default_timeout(self):
        client = Client("test_key")
        assert client._timeout == 30

    def test_custom_timeout(self):
        client = Client("test_key", timeout=60)
        assert client._timeout == 60

    def test_no_timeout(self):
        client = Client("test_key", timeout=None)
        assert client._timeout is None


class TestContainerTracking:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_track_returns_container(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_CONTAINER)
        container = self.client.containers.track("MSCU1234567", shipping_line="MSC")
        assert isinstance(container, Container)
        assert container.container_id == "MSCU1234567"
        assert container.status == "In Transit"

    @patch("requests.Session.get")
    def test_track_passes_timeout(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_CONTAINER)
        self.client.containers.track("MNBU0171007", shipping_line="MAERSK")
        _, kwargs = mock_get.call_args
        assert kwargs["timeout"] == 30

    @patch("requests.Session.get")
    def test_track_with_shipping_line(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_CONTAINER)
        container = self.client.containers.track("MNBU0171007", shipping_line="MAERSK")
        assert isinstance(container, Container)
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["shipping_line"] == "MAERSK"

    def test_track_requires_shipping_line(self):
        with pytest.raises(ValueError, match="shipping_line is required"):
            self.client.containers.track("MSCU1234567", shipping_line="")

    def test_track_invalid_shipping_line(self):
        with pytest.raises(ValueError, match="Invalid shipping_line"):
            self.client.containers.track("MSCU1234567", shipping_line="FAKE_LINE")

    def test_track_invalid_container_number_format(self):
        with pytest.raises(ValueError, match="Invalid container number"):
            self.client.containers.track("invalid", shipping_line="MSC")

    def test_track_rejects_path_traversal(self):
        with pytest.raises(ValueError, match="Invalid container number"):
            self.client.containers.track("../../../etc", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_from_bol_returns_bol_result(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_BOL)
        result = self.client.containers.from_bol("SELM60819800", shipping_line="HMM")
        assert isinstance(result, BolResult)
        assert result.bill_of_lading == "SELM60819800"
        assert len(result.associated_container_numbers) == 3

    def test_from_bol_requires_shipping_line(self):
        with pytest.raises(ValueError, match="shipping_line is required"):
            self.client.containers.from_bol("SELM60819800", shipping_line="")

    def test_from_bol_invalid_shipping_line(self):
        with pytest.raises(ValueError, match="Invalid shipping_line"):
            self.client.containers.from_bol("SELM60819800", shipping_line="FAKE")

    def test_from_bol_rejects_path_traversal(self):
        with pytest.raises(ValueError, match="Invalid bill of lading"):
            self.client.containers.from_bol("../admin", shipping_line="MSC")

    def test_from_bol_rejects_url_encoded_slash(self):
        with pytest.raises(ValueError, match="Invalid bill of lading"):
            self.client.containers.from_bol("SELM%2F60819800", shipping_line="MSC")

    def test_from_bol_rejects_fragment_char(self):
        with pytest.raises(ValueError, match="Invalid bill of lading"):
            self.client.containers.from_bol("SELM#60819800", shipping_line="MSC")

    def test_from_bol_rejects_query_chars(self):
        with pytest.raises(ValueError, match="Invalid bill of lading"):
            self.client.containers.from_bol("SELM?foo=bar", shipping_line="MSC")


class TestStats:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_stats_returns_dict(self, mock_get):
        mock_get.return_value = make_mock_response({
            "data": {
                "plan": "MARINER",
                "requests_total": 2000,
                "requests_made": 6,
                "requests_available": 1994,
            }
        })
        stats = self.client.stats()
        assert stats["plan"] == "MARINER"
        assert stats["requests_available"] == 1994


class TestExceptions:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_error_message_extracted_from_nested_json(self, mock_get):
        mock_get.return_value = make_error_response(
            422, "Unprocessable Entity",
            json_body={"error": {"title": "container number is invalid"}}
        )
        with pytest.raises(APIError, match="container number is invalid"):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_error_message_extracted_from_flat_json(self, mock_get):
        mock_get.return_value = make_error_response(
            500, "Error",
            json_body={"error": "upstream service unavailable"}
        )
        with pytest.raises(APIError, match="upstream service unavailable"):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.containers.track("MSCU1234567", shipping_line="MSC")
        assert exc_info.value.status_code == 500

    @patch("requests.Session.get")
    def test_timeout_raises_api_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        with pytest.raises(APIError, match="timed out"):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_connection_error_raises_api_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("refused")
        with pytest.raises(APIError, match="Connection failed"):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")

    @patch("requests.Session.get")
    def test_non_json_response_raises_api_error(self, mock_get):
        mock = MagicMock()
        mock.status_code = 200
        mock.ok = True
        mock.json.side_effect = ValueError("not json")
        mock_get.return_value = mock
        with pytest.raises(APIError, match="non-JSON"):
            self.client.containers.track("MSCU1234567", shipping_line="MSC")


class TestVesselBasic:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_vessel_basic(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BASIC)
        vessel = self.client.vessels.basic(mmsi="636017123")
        assert isinstance(vessel, VesselBasic)
        assert vessel.name == "MSC LENA F"
        assert vessel.mmsi == "636017123"
        assert vessel.lat == 1.234
        assert vessel.lon == 103.456
        assert vessel.eta_epoch == 1720000000
        assert vessel.raw == MOCK_VESSEL_BASIC["data"]

    @patch("requests.Session.get")
    def test_none_params_not_sent(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BASIC)
        self.client.vessels.basic(mmsi="566093000", page=None, limit=None)
        _, kwargs = mock_get.call_args
        assert "page" not in kwargs["params"]
        assert "limit" not in kwargs["params"]

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BASIC)
        self.client.vessels.basic(imo="9876543")
        args, _ = mock_get.call_args
        assert args[0].endswith("/vessel/basic")

    @patch("requests.Session.get")
    def test_passes_params(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BASIC)
        self.client.vessels.basic(uuid="abc-123", limit="5")
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"uuid": "abc-123", "limit": "5"}

    def test_requires_identifier(self):
        with pytest.raises(ValueError, match="At least one of uuid"):
            self.client.vessels.basic()

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.vessels.basic(mmsi="636017123")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.vessels.basic(mmsi="636017123")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.vessels.basic(mmsi="636017123")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.vessels.basic(mmsi="636017123")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.vessels.basic(mmsi="636017123")
        assert exc_info.value.status_code == 500


class TestVesselPro:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_vessel_pro(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_PRO)
        vessel = self.client.vessels.pro(mmsi="636017123")
        assert isinstance(vessel, VesselPro)
        assert vessel.dest_port == "ROTTERDAM"
        assert vessel.timezone == "Europe/Amsterdam"
        assert vessel.atd_epoch == 1719000000
        assert vessel.current_draught == 14.5
        assert vessel.raw == MOCK_VESSEL_PRO["data"]

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_PRO)
        self.client.vessels.pro(mmsi="636017123")
        args, _ = mock_get.call_args
        assert args[0].endswith("/vessel/pro")

    @patch("requests.Session.get")
    def test_passes_params(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_PRO)
        self.client.vessels.pro(imo="9876543", page="1")
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"imo": "9876543", "page": "1"}

    def test_requires_identifier(self):
        with pytest.raises(ValueError, match="At least one of uuid"):
            self.client.vessels.pro()

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.vessels.pro(mmsi="636017123")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.vessels.pro(mmsi="636017123")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.vessels.pro(mmsi="636017123")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.vessels.pro(mmsi="636017123")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.vessels.pro(mmsi="636017123")
        assert exc_info.value.status_code == 500


class TestVesselBulk:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_bulk_result(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BULK)
        result = self.client.vessels.bulk(mmsi="636017123")
        assert isinstance(result, VesselBulkResult)
        assert result.total == 2
        assert len(result.vessels) == 2
        assert all(isinstance(v, VesselBasic) for v in result.vessels)
        assert result.vessels[1].eta_epoch is None
        assert result.raw is not None
        assert result.vessels[0].name == "MSC LENA F"

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BULK)
        self.client.vessels.bulk(mmsi="636017123")
        args, _ = mock_get.call_args
        assert args[0].endswith("/vessel/bulk")

    @patch("requests.Session.get")
    def test_passes_params(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_BULK)
        self.client.vessels.bulk(uuid="abc-123")
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"uuid": "abc-123"}

    def test_requires_identifier(self):
        with pytest.raises(ValueError, match="At least one of uuid"):
            self.client.vessels.bulk()

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.vessels.bulk(mmsi="636017123")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.vessels.bulk(mmsi="636017123")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.vessels.bulk(mmsi="636017123")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.vessels.bulk(mmsi="636017123")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.vessels.bulk(mmsi="636017123")
        assert exc_info.value.status_code == 500


class TestVesselFinder:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_list_of_vessel_info(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_FINDER)
        result = self.client.vessels.finder(name="MSC LENA")
        assert isinstance(result, list)
        assert isinstance(result[0], VesselInfo)
        assert result[0].name == "MSC LENA F"
        assert result[0].gross_tonnage == 95000
        assert result[0].is_navaid is False
        assert result[0].teu == 9000
        assert result[0].home_port == "MONROVIA"
        assert result[0].raw == MOCK_VESSEL_INFO

    @patch("requests.Session.get")
    def test_returns_empty_list(self, mock_get):
        mock_get.return_value = make_mock_response({"data": []})
        result = self.client.vessels.finder(name="NONEXISTENT")
        assert result == []

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_FINDER)
        self.client.vessels.finder(name="MSC LENA")
        args, _ = mock_get.call_args
        assert args[0].endswith("/vessel/finder")

    @patch("requests.Session.get")
    def test_maps_vessel_type_to_type_param(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_FINDER)
        self.client.vessels.finder(vessel_type="Cargo", fuzzy=1)
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"type": "Cargo", "fuzzy": 1}

    @patch("requests.Session.get")
    def test_passes_spec_filters(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_FINDER)
        self.client.vessels.finder(name="X", gross_tonnage_min=1000, length_max=300.0)
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"name": "X", "gross_tonnage_min": 1000, "length_max": 300.0}

    def test_requires_search_param(self):
        with pytest.raises(ValueError, match="At least one search parameter"):
            self.client.vessels.finder()

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.vessels.finder(name="MSC")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.vessels.finder(name="MSC")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.vessels.finder(name="MSC")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.vessels.finder(name="MSC")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.vessels.finder(name="MSC")
        assert exc_info.value.status_code == 500


class TestVesselSpecs:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_vessel_info(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_SPECS)
        vessel = self.client.vessels.specs(imo="9876543")
        assert isinstance(vessel, VesselInfo)
        assert vessel.imo == "9876543"
        assert vessel.deadweight == 110000
        assert vessel.gross_tonnage == 95000
        assert vessel.teu == 9000
        assert vessel.is_navaid is False

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_SPECS)
        self.client.vessels.specs(imo="9876543")
        args, _ = mock_get.call_args
        assert args[0].endswith("/vessel/specs")

    @patch("requests.Session.get")
    def test_passes_params(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_VESSEL_SPECS)
        self.client.vessels.specs(mmsi="636017123")
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"mmsi": "636017123"}

    def test_requires_identifier(self):
        with pytest.raises(ValueError, match="At least one of uuid"):
            self.client.vessels.specs()

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.vessels.specs(imo="9876543")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.vessels.specs(imo="9876543")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.vessels.specs(imo="9876543")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.vessels.specs(imo="9876543")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.vessels.specs(imo="9876543")
        assert exc_info.value.status_code == 500


class TestPortFinder:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_list_of_ports(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_PORT_FIND)
        result = self.client.ports.find(name="ROTTERDAM")
        assert isinstance(result, list)
        assert isinstance(result[0], Port)
        assert result[0].port_name == "ROTTERDAM"
        assert result[0].unlocode == "NLRTM"
        assert result[0].area_lvl1 == "Western Europe"
        assert result[0].lat == 51.95
        assert result[0].raw == MOCK_PORT_FIND["data"][0]

    @patch("requests.Session.get")
    def test_returns_empty_list(self, mock_get):
        mock_get.return_value = make_mock_response({"data": []})
        result = self.client.ports.find(name="NONEXISTENT")
        assert result == []

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_PORT_FIND)
        self.client.ports.find(name="ROTTERDAM")
        args, _ = mock_get.call_args
        assert args[0].endswith("/port/find")

    @patch("requests.Session.get")
    def test_passes_params(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_PORT_FIND)
        self.client.ports.find(lat=51.95, lon=4.13, radius=10.0)
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"lat": 51.95, "lon": 4.13, "radius": 10.0}

    def test_requires_search_param(self):
        with pytest.raises(ValueError, match="At least one search parameter"):
            self.client.ports.find()

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.ports.find(name="ROTTERDAM")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.ports.find(name="ROTTERDAM")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.ports.find(name="ROTTERDAM")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.ports.find(name="ROTTERDAM")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.ports.find(name="ROTTERDAM")
        assert exc_info.value.status_code == 500


class TestTerminalFinder:
    def setup_method(self):
        self.client = Client("test_key")

    @patch("requests.Session.get")
    def test_returns_list_of_terminals(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_TERMINAL_FIND)
        result = self.client.terminals.find("NLRTM")
        assert isinstance(result, list)
        assert isinstance(result[0], Terminal)
        assert result[0].terminal_name == "ECT DELTA TERMINAL"
        assert result[0].unlocode == "NLRTM"
        assert result[0].company_name == "Hutchison Ports ECT"
        assert result[0].raw == MOCK_TERMINAL_FIND["data"][0]

    @patch("requests.Session.get")
    def test_returns_empty_list(self, mock_get):
        mock_get.return_value = make_mock_response({"data": []})
        result = self.client.terminals.find("NLRTM")
        assert result == []

    @patch("requests.Session.get")
    def test_calls_correct_url(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_TERMINAL_FIND)
        self.client.terminals.find("NLRTM")
        args, _ = mock_get.call_args
        assert args[0].endswith("/terminal")

    @patch("requests.Session.get")
    def test_passes_params(self, mock_get):
        mock_get.return_value = make_mock_response(MOCK_TERMINAL_FIND)
        self.client.terminals.find("NL", page="2", limit="10")
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"unlocode": "NL", "page": "2", "limit": "10"}

    def test_unlocode_too_short(self):
        with pytest.raises(ValueError, match="at least 2 characters"):
            self.client.terminals.find("N")

    def test_unlocode_empty(self):
        with pytest.raises(ValueError, match="at least 2 characters"):
            self.client.terminals.find("")

    @patch("requests.Session.get")
    def test_401_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(401, "Unauthorized")
        with pytest.raises(AuthenticationError):
            self.client.terminals.find("NLRTM")

    @patch("requests.Session.get")
    def test_403_raises_authentication_error(self, mock_get):
        mock_get.return_value = make_error_response(403, "Forbidden")
        with pytest.raises(AuthenticationError):
            self.client.terminals.find("NLRTM")

    @patch("requests.Session.get")
    def test_404_raises_not_found_error(self, mock_get):
        mock_get.return_value = make_error_response(404, "Not Found")
        with pytest.raises(NotFoundError):
            self.client.terminals.find("NLRTM")

    @patch("requests.Session.get")
    def test_429_raises_rate_limit_error(self, mock_get):
        mock_get.return_value = make_error_response(429, "Too Many Requests")
        with pytest.raises(RateLimitError):
            self.client.terminals.find("NLRTM")

    @patch("requests.Session.get")
    def test_500_raises_api_error(self, mock_get):
        mock_get.return_value = make_error_response(500, "Internal Server Error")
        with pytest.raises(APIError) as exc_info:
            self.client.terminals.find("NLRTM")
        assert exc_info.value.status_code == 500
