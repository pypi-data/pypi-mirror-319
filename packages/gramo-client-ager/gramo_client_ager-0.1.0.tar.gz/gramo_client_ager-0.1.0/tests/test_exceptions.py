import pytest
from gramo_client_ager.exceptions import (
    MusicAPIError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError,
    ProcessingError
)

def test_music_api_error():
    error = MusicAPIError("General API error")
    assert str(error) == "General API error"
    assert isinstance(error, Exception)

def test_authentication_error():
    error = AuthenticationError("Invalid API key")
    assert str(error) == "Invalid API key"
    assert isinstance(error, MusicAPIError)

def test_resource_not_found_error():
    error = ResourceNotFoundError("Track not found")
    assert str(error) == "Track not found"
    assert isinstance(error, MusicAPIError)

def test_validation_error():
    error = ValidationError("Invalid request data")
    assert str(error) == "Invalid request data"
    assert isinstance(error, MusicAPIError)

def test_rate_limit_error():
    error = RateLimitError("Too many requests")
    assert str(error) == "Too many requests"
    assert isinstance(error, MusicAPIError)

def test_processing_error():
    error = ProcessingError("Failed to process audio")
    assert str(error) == "Failed to process audio"
    assert isinstance(error, MusicAPIError)

def test_error_hierarchy():
    # Test that all custom exceptions inherit from MusicAPIError
    assert issubclass(AuthenticationError, MusicAPIError)
    assert issubclass(ResourceNotFoundError, MusicAPIError)
    assert issubclass(ValidationError, MusicAPIError)
    assert issubclass(RateLimitError, MusicAPIError)
    assert issubclass(ProcessingError, MusicAPIError)