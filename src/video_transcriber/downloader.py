"""Video downloading functionality."""

import json
import logging
import subprocess
from typing import Dict, Optional

from .exceptions import DownloadError, MetadataError

logger = logging.getLogger(__name__)


class VideoDownloader:
    """Handles video downloading and metadata fetching."""
    
    def __init__(self, download_timeout: int = 120, metadata_timeout: int = 60):
        """
        Initialize the video downloader.
        
        Args:
            download_timeout: Timeout for video downloads in seconds
            metadata_timeout: Timeout for metadata fetching in seconds
        """
        self.download_timeout = download_timeout
        self.metadata_timeout = metadata_timeout
    
    def get_video_info(self, url: str) -> Dict:
        """
        Fetch video metadata using yt-dlp without downloading.
        
        Args:
            url: Video URL
            
        Returns:
            Dictionary containing video metadata
            
        Raises:
            MetadataError: If metadata cannot be fetched
        """
        logger.info(f"Fetching metadata for {url}")
        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-download", url],
                capture_output=True,
                text=True,
                timeout=self.metadata_timeout
            )
            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                logger.debug(f"Successfully fetched metadata: {metadata.get('title', 'Unknown')}")
                return metadata
            else:
                logger.warning(f"yt-dlp returned non-zero exit code: {result.returncode}")
                return {}
        except subprocess.TimeoutExpired:
            logger.warning("Metadata fetch timed out")
            return {}
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse metadata JSON: {e}")
            return {}
        except Exception as e:
            logger.warning(f"Unexpected error fetching metadata: {e}")
            return {}
    
    def download_video(self, url: str, output_path: str) -> None:
        """
        Download video using yt-dlp.
        
        Args:
            url: Video URL
            output_path: Path where video should be saved
            
        Raises:
            DownloadError: If download fails
        """
        logger.info(f"Downloading video to {output_path}")
        try:
            result = subprocess.run(
                ["yt-dlp", "-o", output_path, "-f", "mp4", url],
                capture_output=True,
                text=True,
                timeout=self.download_timeout
            )
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error"
                raise DownloadError(f"Download failed: {error_msg}")
            
            # Verify file exists
            import os
            if not os.path.exists(output_path):
                raise DownloadError(f"Downloaded file not found at {output_path}")
            
            logger.info("Video downloaded successfully")
            
        except subprocess.TimeoutExpired:
            raise DownloadError(f"Download timed out after {self.download_timeout} seconds")
        except Exception as e:
            if isinstance(e, DownloadError):
                raise
            raise DownloadError(f"Unexpected error during download: {e}")
