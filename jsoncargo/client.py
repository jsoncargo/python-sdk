import requests
from .containers import ContainersResource
from .vessels import VesselsResource
from .ports import PortsResource
from .terminals import TerminalsResource
from .exceptions import APIError, AuthenticationError, NotFoundError, RateLimitError


BASE_URL = "http://api.jsoncargo.com/api/v1"


class Client:
    """
    JSONCargo API client.

    Usage:
        from jsoncargo import Client

        client = Client("your_api_key")
        container = client.containers.track("MSCU1234567", shipping_line="MSC")
        print(container.status)
    """

    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: int = 30):
        if not api_key:
            raise ValueError("api_key is required")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"x-api-key": self._api_key})
        self.containers = ContainersResource(self)
        self.vessels = VesselsResource(self)
        self.ports = PortsResource(self)
        self.terminals = TerminalsResource(self)

    def _get(self, path: str, params: dict = None) -> dict:
        url = f"{self._base_url}{path}"
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.exceptions.Timeout:
            raise APIError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise APIError(f"Connection failed: {e}")

        if response.status_code in (401, 403):
            raise AuthenticationError("Invalid or missing API key")
        if response.status_code == 404:
            raise NotFoundError("Resource not found")
        if response.status_code == 429:
            raise RateLimitError("API rate limit exceeded")
        if not response.ok:
            try:
                body = response.json()
                raw = body.get("error") or body.get("message")
                if isinstance(raw, dict):
                    msg = raw.get("title") or raw.get("message") or response.reason
                else:
                    msg = raw or response.reason
            except ValueError:
                msg = response.reason
            raise APIError(msg, status_code=response.status_code)

        try:
            body = response.json()
        except ValueError:
            raise APIError("Server returned a non-JSON response")

        if "data" not in body:
            raise APIError(f"Unexpected response format: missing 'data' key")

        return body

    def stats(self) -> dict:
        """
        Returns API key usage stats: plan name, requests total,
        requests made, and requests available.

        Returns:
            dict with keys: plan, requests_total, requests_made, requests_available
        """
        result = self._get("/api_key/stats")
        return result["data"]
