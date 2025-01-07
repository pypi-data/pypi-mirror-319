from .client import MusicAPIClient
from .models import (
    StemReplacementRequest,
    StemReplacementOutput,
    RatingInput,
    RatingOutput,
    TextQueryInput,
    SearchResult
)
from .exceptions import (
    MusicAPIError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError,
    ProcessingError
)

__version__ = "0.1.0"

__all__ = [
    'MusicAPIClient',
    'StemReplacementRequest',
    'StemReplacementOutput',
    'RatingInput',
    'RatingOutput',
    'TextQueryInput',
    'SearchResult',
    'MusicAPIError',
    'AuthenticationError',
    'ResourceNotFoundError',
    'ValidationError',
    'RateLimitError',
    'ProcessingError'
]