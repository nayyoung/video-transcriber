"""Custom exceptions for video transcriber."""


class TranscriberError(Exception):
    """Base exception for transcriber errors."""
    pass


class DownloadError(TranscriberError):
    """Error during video download."""
    pass


class AudioExtractionError(TranscriberError):
    """Error during audio extraction."""
    pass


class TranscriptionError(TranscriberError):
    """Error during audio transcription."""
    pass


class MetadataError(TranscriberError):
    """Error fetching video metadata."""
    pass
