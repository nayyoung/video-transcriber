"""Main video processing orchestration."""

import logging
import os
from datetime import datetime
from typing import Dict, List, Tuple

from .audio import AudioExtractor
from .config import TranscriberConfig
from .downloader import VideoDownloader
from .exceptions import AudioExtractionError, DownloadError, TranscriptionError
from .transcriber import AudioTranscriber
from .utils import sanitize_filename

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Orchestrates the video downloading, audio extraction, and transcription process."""
    
    def __init__(
        self,
        config: TranscriberConfig,
        downloader: VideoDownloader,
        audio_extractor: AudioExtractor,
        transcriber: AudioTranscriber,
    ):
        """
        Initialize the video processor.
        
        Args:
            config: Configuration object
            downloader: Video downloader instance
            audio_extractor: Audio extractor instance
            transcriber: Audio transcriber instance
        """
        self.config = config
        self.downloader = downloader
        self.audio_extractor = audio_extractor
        self.transcriber = transcriber
    
    def process_url(self, url: str, index: int) -> Tuple[bool, str]:
        """
        Process a single URL through the complete pipeline.
        
        Args:
            url: Video URL to process
            index: Index of the URL in the list
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        logger.info(f"Processing URL: {url}")
        
        # Get video metadata for filename
        info = self.downloader.get_video_info(url)
        
        if info:
            creator = info.get("uploader", "unknown")
            title = info.get("title", f"video_{index}")
            video_id = info.get("id", str(index))
            base_name = sanitize_filename(
                f"{creator}_{title}_{video_id}",
                self.config.max_filename_length
            )
        else:
            base_name = f"video_{index}"
        
        video_path = os.path.join(self.config.video_dir, f"{base_name}.mp4")
        audio_path = os.path.join(self.config.audio_dir, f"{base_name}.mp3")
        transcript_path = os.path.join(self.config.transcript_dir, f"{base_name}.txt")
        
        # Skip if transcript already exists
        if os.path.exists(transcript_path):
            logger.info("Transcript already exists, skipping")
            return True, "Skipped - transcript already exists"
        
        try:
            # Download video
            logger.info("Downloading video...")
            self.downloader.download_video(url, video_path)
            
            # Extract audio
            logger.info("Extracting audio...")
            self.audio_extractor.extract_audio(video_path, audio_path)
            
            # Transcribe
            logger.info("Transcribing audio...")
            transcript = self.transcriber.transcribe(audio_path)
            
            # Save transcript with metadata
            self._save_transcript(transcript_path, url, info, transcript)
            
            logger.info(f"Successfully processed: {base_name}")
            return True, f"Saved to {transcript_path}"
            
        except DownloadError as e:
            logger.error(f"Download failed: {e}")
            return False, f"Download failed: {e}"
        except AudioExtractionError as e:
            logger.error(f"Audio extraction failed: {e}")
            return False, f"Audio extraction failed: {e}"
        except TranscriptionError as e:
            logger.error(f"Transcription failed: {e}")
            return False, f"Transcription failed: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False, f"Unexpected error: {e}"
    
    def _save_transcript(
        self,
        filepath: str,
        url: str,
        metadata: Dict,
        transcript: str
    ) -> None:
        """
        Save transcript with metadata to file.
        
        Args:
            filepath: Path where transcript should be saved
            url: Original video URL
            metadata: Video metadata dictionary
            transcript: Transcribed text
        """
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n")
            if metadata:
                f.write(f"Creator: {metadata.get('uploader', 'Unknown')}\n")
                f.write(f"Title: {metadata.get('title', 'Unknown')}\n")
                f.write(f"Views: {metadata.get('view_count', 'Unknown')}\n")
                f.write(f"Likes: {metadata.get('like_count', 'Unknown')}\n")
                f.write(f"Duration: {metadata.get('duration', 'Unknown')}s\n")
            f.write(f"Transcribed: {datetime.now().isoformat()}\n")
            f.write(f"\n{'='*50}\n\n")
            f.write(transcript)
        
        logger.info(f"Transcript saved to {filepath}")
    
    def process_urls(self, urls: List[str]) -> Tuple[int, int]:
        """
        Process multiple URLs.
        
        Args:
            urls: List of URLs to process
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls):
            logger.info(f"[{i+1}/{len(urls)}] Processing: {url}")
            success, message = self.process_url(url, i)
            
            if success:
                successful += 1
                logger.info(f"  ✓ {message}")
            else:
                failed += 1
                logger.error(f"  ✗ {message}")
        
        return successful, failed
