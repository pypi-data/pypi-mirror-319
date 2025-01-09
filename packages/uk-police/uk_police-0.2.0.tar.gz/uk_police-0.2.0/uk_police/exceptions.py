class APIError(Exception):
    """Base exception for API errors."""
    pass

class ValidationError(APIError):
    """Exception for invalid inputs."""
    pass

class AuthenticationError(APIError):
    """Exception for authentication failures."""
    pass

class NotFoundError(APIError):
    """Exception for 404 errors."""
    pass

class RateLimitError(APIError):
    """Exception for rate limiting (429 errors)."""
    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message)
        self.retry_after = retry_after

class ServerError(APIError):
    """Exception for server-side errors (5xx)."""
    pass