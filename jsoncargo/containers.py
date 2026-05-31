import re
from .models import Container, BolResult

VALID_SHIPPING_LINES = {
    "MAERSK", "HAPAG_LLOYD", "HMM", "ONE", "EVERGREEN",
    "MSC", "CMA_CGM", "COSCO", "ZIM", "YANG_MING", "PIL",
}

_CONTAINER_RE = re.compile(r'^[A-Z]{4}\d{7}$')
_BOL_UNSAFE_RE = re.compile(r'[/\\%#?&+\x00]|\.\.')


def _validate_tracking_number(tracking_number: str) -> None:
    if not _CONTAINER_RE.match(tracking_number):
        raise ValueError(
            f"Invalid container number '{tracking_number}'. "
            "Expected 4 uppercase letters followed by 7 digits (e.g. MSCU1234567)."
        )


def _validate_bol(bill_of_lading: str) -> None:
    if _BOL_UNSAFE_RE.search(bill_of_lading):
        raise ValueError(f"Invalid bill of lading number '{bill_of_lading}'.")


class ContainersResource:
    """
    Container tracking methods. Access via client.containers.
    """

    def __init__(self, client):
        self._client = client

    def track(self, tracking_number: str, shipping_line: str) -> Container:
        """
        Track a container by its tracking number.

        Args:
            tracking_number (str): Full container number including the 4-letter
                prefix, e.g. "MSCU1234567".
            shipping_line (str): Shipping line. Always required.
                Must be one of: MAERSK, HAPAG_LLOYD, HMM, ONE, EVERGREEN, MSC,
                CMA_CGM, COSCO, ZIM, YANG_MING, PIL.

        Returns:
            Container: A Container object with all tracking fields.

        Example:
            container = client.containers.track("MSCU1234567", shipping_line="MSC")
            print(container.status)
            print(container.eta_final_destination)
        """
        if not shipping_line:
            raise ValueError("shipping_line is required")

        if shipping_line not in VALID_SHIPPING_LINES:
            raise ValueError(
                f"Invalid shipping_line '{shipping_line}'. "
                f"Must be one of: {', '.join(sorted(VALID_SHIPPING_LINES))}"
            )

        _validate_tracking_number(tracking_number)

        params = {"shipping_line": shipping_line}
        data = self._client._get(f"/containers/{tracking_number}", params=params)
        return Container(data["data"])

    def from_bol(self, bill_of_lading: str, shipping_line: str) -> BolResult:
        """
        Get all container numbers linked to a bill of lading.

        Args:
            bill_of_lading (str): Bill of lading number.
            shipping_line (str): Shipping line. Always required for BOL lookups.
                Must be one of: MAERSK, HAPAG_LLOYD, HMM, ONE, EVERGREEN, MSC,
                CMA_CGM, COSCO, ZIM, YANG_MING, PIL.

        Returns:
            BolResult: A BolResult object containing associated_container_numbers.

        Example:
            result = client.containers.from_bol("SELM60819800", shipping_line="HMM")
            for number in result.associated_container_numbers:
                print(number)
        """
        if not shipping_line:
            raise ValueError("shipping_line is required for BOL lookups")

        if shipping_line not in VALID_SHIPPING_LINES:
            raise ValueError(
                f"Invalid shipping_line '{shipping_line}'. "
                f"Must be one of: {', '.join(sorted(VALID_SHIPPING_LINES))}"
            )

        _validate_bol(bill_of_lading)

        params = {"shipping_line": shipping_line}
        data = self._client._get(f"/containers/bol/{bill_of_lading}", params=params)
        return BolResult(data["data"])
