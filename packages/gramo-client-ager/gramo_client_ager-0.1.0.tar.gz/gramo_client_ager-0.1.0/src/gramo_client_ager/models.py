from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class StemReplacementRequest:
    """Request model for stem replacement."""
    target_track_id: str
    stem_to_replace: str
    source_track_id: str
    top_k: int = 5
    tempo: Optional[str] = None

@dataclass
class StemReplacementOutput:
    """Response model for stem replacement."""
    target_track_id: str
    source_track_id: str
    stem_type: str
    similarity_score: float
    processed_url: Optional[str] = None

@dataclass
class RatingInput:
    """Input model for rating submissions."""
    target_track_id: str
    source_track_id: str
    stem_type: str
    rating: int
    comments: Optional[str] = None

@dataclass
class RatingOutput:
    """Response model for rating submissions."""
    id: str
    target_track_id: str
    source_track_id: str
    stem_type: str
    rating: int
    comments: Optional[str] = None
    timestamp: str

@dataclass
class TextQueryInput:
    """Input model for text-based search."""
    genre: Optional[str] = None
    mood: Optional[str] = None
    energy: Optional[str] = None
    top_k: int = 5
    tempo: Optional[str] = None

@dataclass
class SearchResult:
    """Response model for search results."""
    track_id: str
    title: str
    artist: str
    similarity: float
    vectors: Optional[Dict[str, List[float]]] = None