from typing import List, Optional
import httpx
from pathlib import Path

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

class GramosynthAPIClient:
    """Client for interacting with the Music API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the Music API client.
        
        Args:
            base_url: Base URL of the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
            
    def _handle_error(self, response: httpx.Response) -> None:
        """Handle error responses from the API."""
        if response.status_code == 401:
            raise AuthenticationError("Invalid or missing API key")
        elif response.status_code == 404:
            raise ResourceNotFoundError("Requested resource not found")
        elif response.status_code == 422:
            raise ValidationError(f"Invalid request data: {response.json()}")
        elif response.status_code == 429:
            raise RateLimitError("API rate limit exceeded")
        elif response.status_code >= 500:
            raise ProcessingError(f"Server error: {response.text}")
        response.raise_for_status()
    
    async def replace_stem(self, request: StemReplacementRequest) -> StemReplacementOutput:
        """
        Replace a stem in the target track with a stem from the source track.
        
        Args:
            request: StemReplacementRequest object containing replacement parameters
            
        Returns:
            StemReplacementOutput containing the replacement result
            
        Raises:
            MusicAPIError: If the API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/swap",
                headers=self.headers,
                json=request.__dict__
            )
            self._handle_error(response)
            return StemReplacementOutput(**response.json())
    
    async def rate_replacement(self, rating: RatingInput) -> RatingOutput:
        """
        Submit a rating for a stem replacement.
        
        Args:
            rating: RatingInput object containing the rating details
            
        Returns:
            RatingOutput containing the stored rating details
            
        Raises:
            MusicAPIError: If the API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/rate",
                headers=self.headers,
                json=rating.__dict__
            )
            self._handle_error(response)
            return RatingOutput(**response.json())
    
    async def search_by_text(
        self,
        genre: Optional[str] = None,
        mood: Optional[str] = None,
        energy: Optional[str] = None,
        top_k: int = 5,
        tempo: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Search tracks by text description.
        
        Args:
            genre: Genre to search for
            mood: Mood to search for
            energy: Energy level to search for
            top_k: Number of results to return
            tempo: Optional tempo filter
            
        Returns:
            List of SearchResult objects
            
        Raises:
            MusicAPIError: If the API request fails
        """
        query = TextQueryInput(
            genre=genre,
            mood=mood,
            energy=energy,
            top_k=top_k,
            tempo=tempo
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/text",
                headers=self.headers,
                json={k: v for k, v in query.__dict__.items() if v is not None}
            )
            self._handle_error(response)
            return [SearchResult(**result) for result in response.json()]
    
    async def get_similar_tracks(
        self,
        track_id: str,
        top_k: int = 5,
        tempo: Optional[str] = None,
        min_stems: int = 2,
        include_vectors: bool = False
    ) -> List[SearchResult]:
        """
        Get tracks similar to the provided track ID.
        
        Args:
            track_id: ID of the reference track
            top_k: Number of similar tracks to retrieve
            tempo: Optional tempo filter
            min_stems: Minimum number of stems required
            include_vectors: Whether to include vectors in the response
            
        Returns:
            List of SearchResult objects
            
        Raises:
            MusicAPIError: If the API request fails
        """
        params = {
            "top_k": top_k,
            "tempo": tempo,
            "min_stems": min_stems,
            "include_vectors": include_vectors
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/similar/{track_id}",
                headers=self.headers,
                params={k: v for k, v in params.items() if v is not None}
            )
            self._handle_error(response)
            return [SearchResult(**result) for result in response.json()]
    
    async def search_by_audio(
        self,
        audio_file: Path,
        n: int = 5,
        tempo: str = "120"
    ) -> List[SearchResult]:
        """
        Search tracks by audio similarity.
        
        Args:
            audio_file: Path to the audio file
            n: Number of results to return
            tempo: Tempo filter
            
        Returns:
            List of SearchResult objects
            
        Raises:
            MusicAPIError: If the API request fails
        """
        files = {"file": audio_file.open("rb")}
        params = {"n": n, "tempo": tempo}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/audio",
                headers=self.headers,
                params=params,
                files=files
            )
            self._handle_error(response)
            return [SearchResult(**result) for result in response.json()]