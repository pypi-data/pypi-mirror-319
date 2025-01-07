# Gramosynth API Client

A Python client for interacting with the Gramosynth API, providing easy access to stem replacement and music search functionality.

## Installation

```bash
pip install gramo-client
```

## Quick Start

```python
import asyncio
from gramo_client import GramosynthAPIClient, StemReplacementRequest, RatingInput
from pathlib import Path

async def main():
    # Initialize client
    client = GramosynthAPIClient(
        base_url="https://qdrant.gramosynth:8000.com",
        api_key="your-api-key"  # Optional
    )
    
    # Get similar tracks
    similar_tracks = await client.get_similar_tracks(
        track_id="track123",
        top_k=5,
        tempo="120",
        min_stems=2
    )
    
    # Print results
    for track in similar_tracks:
        print(f"Track: {track.title} by {track.artist}")
        print(f"Similarity: {track.similarity}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

### Stem Replacement

Replace stems between tracks:

```python
# Create a stem replacement request
replacement = await client.replace_stem(
    StemReplacementRequest(
        target_track_id="track123",
        stem_to_replace="drums",
        source_track_id="track456",
        top_k=5
    )
)
```

### Rating Replacements

Rate stem replacements:

```python
# Submit a rating
rating = await client.rate_replacement(
    RatingInput(
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        rating=5,
        comments="Perfect match!"
    )
)
```

### Search Functionality

#### Text Search

Search tracks by text description:

```python
# Search by genre, mood, and energy
results = await client.search_by_text(
    genre="rock",
    mood="energetic",
    energy="high",
    top_k=5,
    tempo="120"
)
```

#### Audio Search

Search using an audio file:

```python
# Search by audio similarity
results = await client.search_by_audio(
    audio_file=Path("path/to/audio.mp3"),
    n=5,
    tempo="120"
)
```

#### Similar Tracks

Find similar tracks:

```python
# Get similar tracks
similar = await client.get_similar_tracks(
    track_id="track123",
    top_k=5,
    tempo="120",
    min_stems=2,
    include_vectors=True
)
```

## Error Handling

The client raises appropriate exceptions for different error cases:

```python
try:
    results = await client.search_by_text(genre="rock")
except httpx.HTTPStatusError as e:
    print(f"HTTP error occurred: {e.response.status_code}")
except httpx.RequestError as e:
    print(f"Request error occurred: {str(e)}")
```

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/rightsify/gramo-client.git
cd gramo-client

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[test]"
```

### Running tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.