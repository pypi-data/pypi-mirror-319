class MusicAPIError(Exception):
    """Base exception for Music API client errors."""
    pass

class AuthenticationError(MusicAPIError):
    """Raised when there are authentication issues."""
    pass

class ResourceNotFoundError(MusicAPIError):
    """Raised when a requested resource is not found."""
    pass

class ValidationError(MusicAPIError):
    """Raised when the request data is invalid."""
    pass

class RateLimitError(MusicAPIError):
    """Raised when API rate limits are exceeded."""
    pass

class ProcessingError(MusicAPIError):
    """Raised when there's an error processing the request."""
    pass