# Gramosynth API Client Documentation

## GramosynthAPIClient

The main client class for interacting with the Gramosynth API.

### Initialization

```python
from gramo_client import GramosynthAPIClient

client = GramosynthAPIClient(
    base_url="https://qdrant.gramosynth.com",
    api_key="your-api-key"  # Optional
)
```

### Methods

#### replace_stem

Replace a stem in the target track with a stem from the source track.

```python
async def replace_stem(request: StemReplacementRequest) -> StemReplacementOutput
```

Parameters:
- `request`: A `StemReplacementRequest` object containing:
  - `target_track_id`: ID of the track to modify
  - `stem_to_replace`: Type of stem to replace ("drums", "bass", etc.)
  - `source_track_id`: ID of the track to take the stem from
  - `top_k`: Number of candidates to consider (default: 5)
  - `tempo`: Optional tempo filter

Returns:
- `StemReplacementOutput` object with replacement results

Example:
```python
result = await client.replace_stem(
    StemReplacementRequest(
        target_track_id="track123",
        stem_to_replace="drums",
        source_track_id="track456"
    )
)
```

#### search_by_text

Search tracks using text descriptions.

```python
async def search_by_text(
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    energy: Optional[str] = None,
    top_k: int = 5,
    tempo: Optional[str] = None
) -> List[SearchResult]
```

Parameters:
- `genre`: Music genre to search for
- `mood`: Mood description
- `energy`: Energy level description
- `top_k`: Number of results to return
- `tempo`: Optional tempo filter

Returns:
- List of `SearchResult` objects

Example:
```python
results = await client.search_by_text(
    genre="rock",
    mood="energetic",
    energy="high",
    top_k=5
)
```

#### get_similar_tracks

Find tracks similar to a reference track.

```python
async def get_similar_tracks(
    track_id: str,
    top_k: int = 5,
    tempo: Optional[str] = None,
    min_stems: int = 2,
    include_vectors: bool = False
) -> List[SearchResult]
```

Parameters:
- `track_id`: ID of the reference track
- `top_k`: Number of similar tracks to retrieve
- `tempo`: Optional tempo filter
- `min_stems`: Minimum number of stems required
- `include_vectors`: Whether to include embedding vectors

Returns:
- List of `SearchResult` objects

Example:
```python
similar_tracks = await client.get_similar_tracks(
    track_id="track123",
    top_k=5,
    include_vectors=True
)
```

#### search_by_audio

Search tracks using an audio file as reference.

```python
async def search_by_audio(
    audio_file: Path,
    n: int = 5,
    tempo: str = "120"
) -> List[SearchResult]
```

Parameters:
- `audio_file`: Path to the audio file
- `n`: Number of results to return
- `tempo`: Tempo filter

Returns:
- List of `SearchResult` objects

Example:
```python
results = await client.search_by_audio(
    audio_file=Path("song.mp3"),
    n=5,
    tempo="120"
)
```

#### rate_replacement

Submit a rating for a stem replacement.

```python
async def rate_replacement(rating: RatingInput) -> RatingOutput
```

Parameters:
- `rating`: A `RatingInput` object containing:
  - `target_track_id`: ID of the modified track
  - `source_track_id`: ID of the source track
  - `stem_type`: Type of stem that was replaced
  - `rating`: Rating score (typically 1-5)
  - `comments`: Optional feedback

Returns:
- `RatingOutput` object with the stored rating details

Example:
```python
result = await client.rate_replacement(
    RatingInput(
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        rating=5,
        comments="Perfect match!"
    )
)
```

## Data Models

### StemReplacementRequest

Request model for stem replacement operations.

Fields:
- `target_track_id` (str): ID of the track to modify
- `stem_to_replace` (str): Type of stem to replace
- `source_track_id` (str): ID of the track to take the stem from
- `top_k` (int, optional): Number of candidates to consider
- `tempo` (str, optional): Tempo filter

### SearchResult

Model for search results.

Fields:
- `track_id` (str): Track identifier
- `title` (str): Track title
- `artist` (str): Artist name
- `similarity` (float): Similarity score
- `vectors` (Dict[str, List[float]], optional): Embedding vectors

### RatingInput

Model for submitting ratings.

Fields:
- `target_track_id` (str): ID of the modified track
- `source_track_id` (str): ID of the source track
- `stem_type` (str): Type of stem that was replaced
- `rating` (int): Rating score
- `comments` (str, optional): Additional feedback

## Error Handling

The client defines several custom exceptions:

- `MusicAPIError`: Base exception for all API errors
- `AuthenticationError`: Invalid or missing API key
- `ResourceNotFoundError`: Requested resource not found
- `ValidationError`: Invalid request data
- `RateLimitError`: API rate limit exceeded
- `ProcessingError`: Server processing error

Example error handling:
```python
try:
    result = await client.search_by_text(genre="rock")
except AuthenticationError:
    print("Invalid API key")
except ResourceNotFoundError:
    print("No matching tracks found")
except MusicAPIError as e:
    print(f"API error: {str(e)}")
```