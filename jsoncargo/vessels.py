from .models import VesselBasic, VesselPro, VesselBulkResult, VesselInfo


class VesselsResource:
    """
    Vessel tracking and lookup methods. Access via client.vessels.
    """

    def __init__(self, client):
        self._client = client

    def basic(self, *, uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselBasic:
        """
        Track a single vessel with basic position data.

        Args:
            uuid (str): Internal vessel UUID.
            mmsi (str): Maritime Mobile Service Identity.
            imo (str): IMO number.
            page (str): Page number.
            limit (str): Results per page.

        At least one of uuid, mmsi, or imo must be provided.

        Returns:
            VesselBasic: A VesselBasic object with position and ETA fields.
        """
        if uuid is None and mmsi is None and imo is None:
            raise ValueError("At least one of uuid, mmsi, or imo is required")

        params = {"uuid": uuid, "mmsi": mmsi, "imo": imo, "page": page, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._client._get("/vessel/basic", params=params)
        return VesselBasic(data["data"])

    def pro(self, *, uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselPro:
        """
        Track a single vessel with extended position and port data.

        Args:
            uuid (str): Internal vessel UUID.
            mmsi (str): Maritime Mobile Service Identity.
            imo (str): IMO number.
            page (str): Page number.
            limit (str): Results per page.

        At least one of uuid, mmsi, or imo must be provided.

        Returns:
            VesselPro: A VesselPro object with extended tracking fields.
        """
        if uuid is None and mmsi is None and imo is None:
            raise ValueError("At least one of uuid, mmsi, or imo is required")

        params = {"uuid": uuid, "mmsi": mmsi, "imo": imo, "page": page, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._client._get("/vessel/pro", params=params)
        return VesselPro(data["data"])

    def bulk(self, *, uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselBulkResult:
        """
        Track multiple vessels at once.

        Args:
            uuid (str): Internal vessel UUID.
            mmsi (str): Maritime Mobile Service Identity.
            imo (str): IMO number.
            page (str): Page number.
            limit (str): Results per page.

        At least one of uuid, mmsi, or imo must be provided.

        Returns:
            VesselBulkResult: A VesselBulkResult with total and vessels list.
        """
        if uuid is None and mmsi is None and imo is None:
            raise ValueError("At least one of uuid, mmsi, or imo is required")

        params = {"uuid": uuid, "mmsi": mmsi, "imo": imo, "page": page, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._client._get("/vessel/bulk", params=params)
        return VesselBulkResult(data["data"])

    def finder(self, *, name=None, fuzzy=None, vessel_type=None, type_specific=None,
               country_iso=None, gross_tonnage_min=None, gross_tonnage_max=None,
               deadweight_min=None, deadweight_max=None, length_min=None, length_max=None,
               breadth_min=None, breadth_max=None, year_built_min=None, year_built_max=None,
               next=None, page=None, limit=None) -> list:
        """
        Search vessels by name and specification filters.

        Args:
            name (str): Vessel name.
            fuzzy (int): Enable fuzzy name matching.
            vessel_type (str): Vessel type (sent as "type").
            type_specific (str): Specific vessel type.
            country_iso (str): Flag country ISO code.
            gross_tonnage_min (int): Minimum gross tonnage.
            gross_tonnage_max (int): Maximum gross tonnage.
            deadweight_min (int): Minimum deadweight.
            deadweight_max (int): Maximum deadweight.
            length_min (float): Minimum length.
            length_max (float): Maximum length.
            breadth_min (float): Minimum breadth.
            breadth_max (float): Maximum breadth.
            year_built_min (int): Minimum year built.
            year_built_max (int): Maximum year built.
            next (str): Pagination cursor.
            page (str): Page number.
            limit (str): Results per page.

        At least one search parameter must be provided.

        Returns:
            list[VesselInfo]: A list of VesselInfo objects.
        """
        params = {
            "name": name,
            "fuzzy": fuzzy,
            "type": vessel_type,
            "type_specific": type_specific,
            "country_iso": country_iso,
            "gross_tonnage_min": gross_tonnage_min,
            "gross_tonnage_max": gross_tonnage_max,
            "deadweight_min": deadweight_min,
            "deadweight_max": deadweight_max,
            "length_min": length_min,
            "length_max": length_max,
            "breadth_min": breadth_min,
            "breadth_max": breadth_max,
            "year_built_min": year_built_min,
            "year_built_max": year_built_max,
            "next": next,
            "page": page,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        if not params:
            raise ValueError("At least one search parameter is required")

        data = self._client._get("/vessel/finder", params=params)
        return [VesselInfo(item) for item in data["data"]]

    def specs(self, *, uuid=None, mmsi=None, imo=None, page=None, limit=None) -> VesselInfo:
        """
        Get the specification of a single vessel.

        Args:
            uuid (str): Internal vessel UUID.
            mmsi (str): Maritime Mobile Service Identity.
            imo (str): IMO number.
            page (str): Page number.
            limit (str): Results per page.

        At least one of uuid, mmsi, or imo must be provided.

        Returns:
            VesselInfo: A VesselInfo object with full specifications.
        """
        if uuid is None and mmsi is None and imo is None:
            raise ValueError("At least one of uuid, mmsi, or imo is required")

        params = {"uuid": uuid, "mmsi": mmsi, "imo": imo, "page": page, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._client._get("/vessel/specs", params=params)
        return VesselInfo(data["data"])
