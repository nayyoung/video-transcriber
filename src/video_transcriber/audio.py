"""Audio extraction functionality."""

import logging
import os
import subprocess

from .exceptions import AudioExtractionError

logger = logging.getLogger(__name__)


class AudioExtractor:
    """Handles audio extraction from video files."""
    
    def __init__(self, timeout: int = 60):
        """
        Initialize the audio extractor.
        
        Args:
            timeout: Timeout for audio extraction in seconds
        """
        self.timeout = timeout
    
    def extract_audio(self, video_path: str, audio_path: str) -> None:
        """
        Extract audio from video using ffmpeg.
        
        Args:
            video_path: Path to input video file
            audio_path: Path where audio should be saved
            
        Raises:
            AudioExtractionError: If extraction fails
        """
        logger.info(f"Extracting audio from {video_path} to {audio_path}")
        try:
            result = subprocess.run(
                ["ffmpeg", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-y", audio_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error"
                raise AudioExtractionError(f"Audio extraction failed: {error_msg}")
            
            # Verify file exists
            if not os.path.exists(audio_path):
                raise AudioExtractionError(f"Extracted audio file not found at {audio_path}")
            
            logger.info("Audio extracted successfully")
            
        except subprocess.TimeoutExpired:
            raise AudioExtractionError(f"Audio extraction timed out after {self.timeout} seconds")
        except Exception as e:
            if isinstance(e, AudioExtractionError):
                raise
            raise AudioExtractionError(f"Unexpected error during audio extraction: {e}")
