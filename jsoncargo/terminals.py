from .models import Terminal


class TerminalsResource:
    """
    Terminal lookup methods. Access via client.terminals.
    """

    def __init__(self, client):
        self._client = client

    def find(self, unlocode, *, page=None, limit=None) -> list:
        """
        Search terminals by UN/LOCODE.

        Args:
            unlocode (str): UN/LOCODE. Must be at least 2 characters.
            page (str): Page number.
            limit (str): Results per page.

        Returns:
            list[Terminal]: A list of Terminal objects.
        """
        unlocode = unlocode.strip() if unlocode else ""
        if len(unlocode) < 2:
            raise ValueError("unlocode must be at least 2 characters")

        params = {"unlocode": unlocode, "page": page, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._client._get("/terminal", params=params)
        return [Terminal(item) for item in data["data"]]
