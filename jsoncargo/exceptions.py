class JSONCargoError(Exception):
    """Base exception for all jsoncargo SDK errors."""
    pass


class AuthenticationError(JSONCargoError):
    """Raised when the API key is invalid or missing (HTTP 401)."""
    pass


class NotFoundError(JSONCargoError):
    """Raised when the requested resource does not exist (HTTP 404)."""
    pass


class RateLimitError(JSONCargoError):
    """Raised when the API rate limit is exceeded (HTTP 429)."""
    pass


class APIError(JSONCargoError):
    """Raised for unexpected API errors (5xx, malformed responses, etc.)."""

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
