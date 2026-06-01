from .models import Port


class PortsResource:
    """
    Port lookup methods. Access via client.ports.
    """

    def __init__(self, client):
        self._client = client

    def find(self, *, lat=None, lon=None, radius=None, name=None, country_iso=None,
             port_type=None, fuzzy=None, page=None, limit=None) -> list:
        """
        Search ports by location, name, or country.

        Args:
            lat (float): Latitude for radius search.
            lon (float): Longitude for radius search.
            radius (float): Search radius.
            name (str): Port name.
            country_iso (str): Country ISO code.
            port_type (str): Port type.
            fuzzy (int): Enable fuzzy name matching.
            page (str): Page number.
            limit (str): Results per page.

        At least one parameter must be provided.

        Returns:
            list[Port]: A list of Port objects.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "name": name,
            "country_iso": country_iso,
            "port_type": port_type,
            "fuzzy": fuzzy,
            "page": page,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        if not params:
            raise ValueError("At least one search parameter is required")

        data = self._client._get("/port/find", params=params)
        return [Port(item) for item in data["data"]]
