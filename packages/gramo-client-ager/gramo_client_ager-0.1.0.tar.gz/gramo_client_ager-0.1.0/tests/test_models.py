import pytest
from gramo_client_ager.models import (
    StemReplacementRequest,
    StemReplacementOutput,
    RatingInput,
    RatingOutput,
    TextQueryInput,
    SearchResult
)

def test_stem_replacement_request():
    request = StemReplacementRequest(
        target_track_id="track123",
        stem_to_replace="drums",
        source_track_id="track456",
        top_k=5,
        tempo="120"
    )
    
    assert request.target_track_id == "track123"
    assert request.stem_to_replace == "drums"
    assert request.source_track_id == "track456"
    assert request.top_k == 5
    assert request.tempo == "120"

def test_stem_replacement_output():
    output = StemReplacementOutput(
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        similarity_score=0.85,
        processed_url="https://example.com/processed.mp3"
    )
    
    assert output.target_track_id == "track123"
    assert output.source_track_id == "track456"
    assert output.stem_type == "drums"
    assert output.similarity_score == 0.85
    assert output.processed_url == "https://example.com/processed.mp3"

def test_rating_input():
    rating = RatingInput(
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        rating=5,
        comments="Great match!"
    )
    
    assert rating.target_track_id == "track123"
    assert rating.source_track_id == "track456"
    assert rating.stem_type == "drums"
    assert rating.rating == 5
    assert rating.comments == "Great match!"

def test_rating_output():
    output = RatingOutput(
        id="rating123",
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        rating=5,
        comments="Great match!",
        timestamp="2024-01-03T12:00:00Z"
    )
    
    assert output.id == "rating123"
    assert output.target_track_id == "track123"
    assert output.rating == 5
    assert output.timestamp == "2024-01-03T12:00:00Z"

def test_text_query_input():
    query = TextQueryInput(
        genre="rock",
        mood="energetic",
        energy="high",
        top_k=5,
        tempo="120"
    )
    
    assert query.genre == "rock"
    assert query.mood == "energetic"
    assert query.energy == "high"
    assert query.top_k == 5
    assert query.tempo == "120"

def test_text_query_input_defaults():
    query = TextQueryInput()
    
    assert query.genre is None
    assert query.mood is None
    assert query.energy is None
    assert query.top_k == 5
    assert query.tempo is None

def test_search_result():
    result = SearchResult(
        track_id="track123",
        title="Test Song",
        artist="Test Artist",
        similarity=0.95,
        vectors={"embedding": [0.1, 0.2, 0.3]}
    )
    
    assert result.track_id == "track123"
    assert result.title == "Test Song"
    assert result.artist == "Test Artist"
    assert result.similarity == 0.95
    assert result.vectors["embedding"] == [0.1, 0.2, 0.3]

def test_search_result_without_vectors():
    result = SearchResult(
        track_id="track123",
        title="Test Song",
        artist="Test Artist",
        similarity=0.95
    )
    
    assert result.vectors is None