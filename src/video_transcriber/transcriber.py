"""Audio transcription functionality."""

import logging
from typing import Any

from .exceptions import TranscriptionError

logger = logging.getLogger(__name__)


class AudioTranscriber:
    """Handles audio transcription using Whisper."""
    
    def __init__(self, model: Any):
        """
        Initialize the audio transcriber.
        
        Args:
            model: Whisper model instance
        """
        self.model = model
    
    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
            
        Raises:
            TranscriptionError: If transcription fails
        """
        logger.info(f"Transcribing audio from {audio_path}")
        try:
            result = self.model.transcribe(audio_path)
            text = result.get("text", "")
            
            if not text:
                raise TranscriptionError("Transcription returned empty text")
            
            logger.info("Transcription completed successfully")
            return text
            
        except Exception as e:
            if isinstance(e, TranscriptionError):
                raise
            raise TranscriptionError(f"Unexpected error during transcription: {e}")
