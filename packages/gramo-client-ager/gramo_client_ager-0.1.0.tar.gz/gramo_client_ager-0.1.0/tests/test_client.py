import pytest
from gramo_client_ager import (
    MusicAPIClient,
    StemReplacementRequest,
    RatingInput,
    MusicAPIError,
    AuthenticationError,
    ResourceNotFoundError
)

@pytest.fixture
def client():
    return MusicAPIClient(base_url="https://api.example.com", api_key="test-key")

@pytest.mark.asyncio
async def test_replace_stem_success(client, httpx_mock):
    # Mock the successful response
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/swap",
        json={
            "target_track_id": "track123",
            "source_track_id": "track456",
            "stem_type": "drums",
            "similarity_score": 0.85,
            "processed_url": "https://example.com/processed.mp3"
        },
        status_code=200
    )

    request = StemReplacementRequest(
        target_track_id="track123",
        stem_to_replace="drums",
        source_track_id="track456"
    )
    
    result = await client.replace_stem(request)
    
    assert result.target_track_id == "track123"
    assert result.source_track_id == "track456"
    assert result.stem_type == "drums"
    assert result.similarity_score == 0.85
    assert result.processed_url == "https://example.com/processed.mp3"

@pytest.mark.asyncio
async def test_replace_stem_auth_error(client, httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/swap",
        json={"detail": "Invalid API key"},
        status_code=401
    )

    request = StemReplacementRequest(
        target_track_id="track123",
        stem_to_replace="drums",
        source_track_id="track456"
    )
    
    with pytest.raises(AuthenticationError):
        await client.replace_stem(request)

@pytest.mark.asyncio
async def test_search_by_text_success(client, httpx_mock):
    mock_response = [
        {
            "track_id": "track123",
            "title": "Test Song",
            "artist": "Test Artist",
            "similarity": 0.95
        }
    ]
    
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/text",
        json=mock_response,
        status_code=200
    )

    results = await client.search_by_text(
        genre="rock",
        mood="energetic",
        top_k=1
    )
    
    assert len(results) == 1
    assert results[0].track_id == "track123"
    assert results[0].title == "Test Song"
    assert results[0].artist == "Test Artist"
    assert results[0].similarity == 0.95

@pytest.mark.asyncio
async def test_get_similar_tracks_success(client, httpx_mock):
    mock_response = [
        {
            "track_id": "track456",
            "title": "Similar Song",
            "artist": "Another Artist",
            "similarity": 0.88,
            "vectors": {"embedding": [0.1, 0.2, 0.3]}
        }
    ]
    
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/similar/track123",
        json=mock_response,
        status_code=200
    )

    results = await client.get_similar_tracks(
        track_id="track123",
        include_vectors=True
    )
    
    assert len(results) == 1
    assert results[0].track_id == "track456"
    assert results[0].vectors["embedding"] == [0.1, 0.2, 0.3]

@pytest.mark.asyncio
async def test_search_by_audio_success(client, httpx_mock, tmp_path):
    # Create a temporary test file
    test_file = tmp_path / "test.mp3"
    test_file.write_bytes(b"test audio content")
    
    mock_response = [
        {
            "track_id": "track789",
            "title": "Found Song",
            "artist": "Found Artist",
            "similarity": 0.75
        }
    ]
    
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/audio",
        json=mock_response,
        status_code=200
    )

    results = await client.search_by_audio(
        audio_file=test_file,
        n=1,
        tempo="120"
    )
    
    assert len(results) == 1
    assert results[0].track_id == "track789"
    assert results[0].similarity == 0.75

@pytest.mark.asyncio
async def test_rate_replacement_success(client, httpx_mock):
    mock_response = {
        "id": "rating123",
        "target_track_id": "track123",
        "source_track_id": "track456",
        "stem_type": "drums",
        "rating": 5,
        "comments": "Great match!",
        "timestamp": "2024-01-03T12:00:00Z"
    }
    
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/rate",
        json=mock_response,
        status_code=200
    )

    rating = RatingInput(
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        rating=5,
        comments="Great match!"
    )
    
    result = await client.rate_replacement(rating)
    
    assert result.id == "rating123"
    assert result.target_track_id == "track123"
    assert result.rating == 5
    assert result.timestamp == "2024-01-03T12:00:00Z"