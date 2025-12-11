"""Configuration management for video transcriber."""

import os
from dataclasses import dataclass
from typing import Optional


# Constants
DEFAULT_WHISPER_MODEL = "base"
DEFAULT_URLS_FILE = "urls.txt"
DEFAULT_VIDEO_DIR = "videos"
DEFAULT_AUDIO_DIR = "audio"
DEFAULT_TRANSCRIPT_DIR = "transcripts"
DEFAULT_DOWNLOAD_TIMEOUT = 120
DEFAULT_AUDIO_TIMEOUT = 60
DEFAULT_METADATA_TIMEOUT = 60
MAX_FILENAME_LENGTH = 50


@dataclass
class TranscriberConfig:
    """Configuration for the transcriber."""
    
    urls_file: str = DEFAULT_URLS_FILE
    whisper_model: str = DEFAULT_WHISPER_MODEL
    video_dir: str = DEFAULT_VIDEO_DIR
    audio_dir: str = DEFAULT_AUDIO_DIR
    transcript_dir: str = DEFAULT_TRANSCRIPT_DIR
    download_timeout: int = DEFAULT_DOWNLOAD_TIMEOUT
    audio_timeout: int = DEFAULT_AUDIO_TIMEOUT
    metadata_timeout: int = DEFAULT_METADATA_TIMEOUT
    max_filename_length: int = MAX_FILENAME_LENGTH
    
    @classmethod
    def from_env(cls) -> "TranscriberConfig":
        """Create configuration from environment variables."""
        return cls(
            urls_file=os.environ.get("URLS_FILE", DEFAULT_URLS_FILE),
            whisper_model=os.environ.get("WHISPER_MODEL", DEFAULT_WHISPER_MODEL),
            video_dir=os.environ.get("VIDEO_DIR", DEFAULT_VIDEO_DIR),
            audio_dir=os.environ.get("AUDIO_DIR", DEFAULT_AUDIO_DIR),
            transcript_dir=os.environ.get("TRANSCRIPT_DIR", DEFAULT_TRANSCRIPT_DIR),
        )
    
    def create_directories(self) -> None:
        """Create necessary output directories."""
        for directory in [self.video_dir, self.audio_dir, self.transcript_dir]:
            os.makedirs(directory, exist_ok=True)
