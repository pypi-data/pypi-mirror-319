import pytest
import httpx

@pytest.fixture
def httpx_mock():
    """
    Mock HTTPX client responses.
    For use with pytest-httpx.
    """
    with httpx.MockClient() as client:
        yield client