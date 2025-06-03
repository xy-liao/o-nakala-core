"""
Exceptions for the Nakala connector.
"""

class NakalaError(Exception):
    """Base exception for all Nakala connector errors."""
    pass

class NakalaValidationError(NakalaError):
    """Raised when data validation fails."""
    def __init__(self, message: str, errors: dict = None):
        self.errors = errors or {}
        super().__init__(message)

class NakalaAPIError(NakalaError):
    """Raised when the Nakala API returns an error."""
    def __init__(self, message: str, status_code: int = None, response=None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)

class NakalaAuthenticationError(NakalaAPIError):
    """Raised when authentication fails."""
    pass

class NakalaNotFoundError(NakalaAPIError):
    """Raised when a resource is not found."""
    pass

class NakalaRateLimitError(NakalaAPIError):
    """Raised when rate limits are exceeded."""
    pass
