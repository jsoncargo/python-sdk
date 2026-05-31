import pytest
from unittest.mock import patch, MagicMock
import requests
from jsoncargo import Client, Container, BolResult, AuthenticationError, NotFoundError, RateLimitError, APIError


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
