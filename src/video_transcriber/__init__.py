"""Video Transcriber - Download and transcribe TikTok videos."""

__version__ = "1.0.0"

from .audio import AudioExtractor
from .config import TranscriberConfig
from .downloader import VideoDownloader
from .exceptions import (
    AudioExtractionError,
    DownloadError,
    MetadataError,
    TranscriptionError,
    TranscriberError,
)
from .processor import VideoProcessor
from .transcriber import AudioTranscriber
from .utils import read_urls_from_file, sanitize_filename, setup_logging

__all__ = [
    "AudioExtractor",
    "AudioExtractionError",
    "DownloadError",
    "MetadataError",
    "TranscriptionError",
    "TranscriberConfig",
    "TranscriberError",
    "VideoDownloader",
    "VideoProcessor",
    "AudioTranscriber",
    "read_urls_from_file",
    "sanitize_filename",
    "setup_logging",
]
