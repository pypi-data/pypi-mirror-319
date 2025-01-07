# Gramosynth API Client Examples

## Basic Usage Examples

### Setting up the Client

```python
import asyncio
from gramo_client import GramosynthAPIClient

# Initialize the client
client = GramosynthAPIClient(
    base_url="https://qdrant.gramosynth.com",
    api_key="your-api-key"
)

# Create an async function for our operations
async def main():
    # Client operations will go here
    pass

# Run the async function
asyncio.run(main())
```

### Searching for Tracks

#### Text-based Search

```python
async def search_tracks():
    # Search by genre and mood
    rock_tracks = await client.search_by_text(
        genre="rock",
        mood="energetic",
        top_k=5
    )
    
    for track in rock_tracks:
        print(f"Found: {track.title} by {track.artist}")
        print(f"Similarity: {track.similarity}")
```

#### Audio-based Search

```python
from pathlib import Path

async def search_by_audio_example():
    # Search using an audio file
    audio_path = Path("path/to/your/song.mp3")
    similar_tracks = await client.search_by_audio(
        audio_file=audio_path,
        n=5,
        tempo="120"
    )
    
    for track in similar_tracks:
        print(f"Similar track: {track.title}")
```

### Working with Stems

#### Replacing Stems

```python
from music_api_client import StemReplacementRequest

async def replace_stem_example():
    # Create a stem replacement request
    request = StemReplacementRequest(
        target_track_id="track123",
        stem_to_replace="drums",
        source_track_id="track456",
        top_k=5
    )
    
    # Perform the replacement
    result = await client.replace_stem(request)
    
    print(f"Replacement score: {result.similarity_score}")
    print(f"Processed file: {result.processed_url}")
```

#### Rating Stem Replacements

```python
from music_api_client import RatingInput

async def rate_replacement_example():
    # Submit a rating
    rating = RatingInput(
        target_track_id="track123",
        source_track_id="track456",
        stem_type="drums",
        rating=5,
        comments="Great drum replacement!"
    )
    
    result = await client.rate_replacement(rating)
    print(f"Rating ID: {result.id}")
```

## Advanced Examples

### Complete Workflow Example

```python
async def complete_workflow():
    # 1. Search for a target track
    target_tracks = await client.search_by_text(
        genre="rock",
        mood="energetic",
        top_k=1
    )
    target_track = target_tracks[0]
    
    # 2. Find similar tracks for stem replacement
    similar_tracks = await client.get_similar_tracks(
        track_id=target_track.track_id,
        top_k=5,
        min_stems=2
    )
    
    # 3. Replace stems
    for source_track in similar_tracks:
        request = StemReplacementRequest(
            target_track_id=target_track.track_id,
            stem_to_replace="drums",
            source_track_id=source_track.track_id
        )
        
        result = await client.replace_stem(request)
        
        # 4. Rate the replacement if it's good
        if result.similarity_score > 0.8:
            rating = RatingInput(
                target_track_id=target_track.track_id,
                source_track_id=source_track.track_id,
                stem_type="drums",
                rating=5,
                comments="High similarity score!"
            )
            await client.rate_replacement(rating)
```

### Error Handling Example

```python
from music_api_client.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError
)

async def error_handling_example():
    try:
        results = await client.search_by_text(genre="rock")
        
    except AuthenticationError:
        print("Please check your API key")
        
    except ResourceNotFoundError:
        print("No matching tracks found")
        
    except ValidationError as e:
        print(f"Invalid request: {str(e)}")
        
    except RateLimitError:
        print("Please wait before making more requests")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
```

### Batch Processing Example

```python
async def batch_processing():
    # Process multiple tracks in parallel
    async def process_track(track_id: str):
        try:
            similar = await client.get_similar_tracks(track_id, top_k=3)
            return similar
        except Exception as e:
            print(f"Error processing track {track_id}: {str(e)}")
            return []

    # Process multiple tracks
    track_ids = ["track1", "track2", "track3"]
    tasks = [process_track(track_id) for track_id in track_ids]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    
    # Process results
    for track_id, similar_tracks in zip(track_ids, results):
        print(f"\nSimilar tracks for {track_id}:")
        for track in similar_tracks:
            print(f"- {track.title} (similarity: {track.similarity})")
```

## Testing Examples

### Using the Client in Tests

```python
import pytest
from music_api_client import GramosynthAPIClient

@pytest.fixture
async def client():
    # Create a test client
    client = GramosynthAPIClient(
        base_url="https://test-qdrant.gramosynth.com",
        api_key="test-key"
    )
    return client

@pytest.mark.asyncio
async def test_search_workflow(client):
    # Search for tracks
    results = await client.search_by_text(
        genre="rock",
        top_k=1
    )
    
    assert len(results) > 0
    assert results[0].title is not None
    
    # Get similar tracks
    similar = await client.get_similar_tracks(
        track_id=results[0].track_id,
        top_k=3
    )
    
    assert len(similar) <= 3
```