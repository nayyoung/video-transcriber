"""Command-line interface for video transcriber."""

import argparse
import logging
import sys
from pathlib import Path

try:
    import whisper
except ImportError:
    print("Error: openai-whisper not installed. Run: pip install openai-whisper")
    sys.exit(1)

from .audio import AudioExtractor
from .config import TranscriberConfig
from .downloader import VideoDownloader
from .processor import VideoProcessor
from .transcriber import AudioTranscriber
from .utils import read_urls_from_file, setup_logging

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Download TikTok videos and generate transcripts using Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default settings
  python -m video_transcriber
  
  # Use a different Whisper model
  python -m video_transcriber --model medium
  
  # Use a custom URLs file
  python -m video_transcriber --urls my_urls.txt
  
  # Enable debug logging
  python -m video_transcriber --debug
        """
    )
    
    parser.add_argument(
        "--urls",
        type=str,
        default="urls.txt",
        help="Path to file containing URLs (default: urls.txt)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)"
    )
    
    parser.add_argument(
        "--video-dir",
        type=str,
        default="videos",
        help="Directory for downloaded videos (default: videos)"
    )
    
    parser.add_argument(
        "--audio-dir",
        type=str,
        default="audio",
        help="Directory for extracted audio (default: audio)"
    )
    
    parser.add_argument(
        "--transcript-dir",
        type=str,
        default="transcripts",
        help="Directory for transcripts (default: transcripts)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)
    
    logger.info("Starting Video Transcriber")
    
    # Create configuration
    config = TranscriberConfig(
        urls_file=args.urls,
        whisper_model=args.model,
        video_dir=args.video_dir,
        audio_dir=args.audio_dir,
        transcript_dir=args.transcript_dir,
    )
    
    # Check if URLs file exists
    if not Path(config.urls_file).exists():
        logger.error(f"Error: {config.urls_file} not found.")
        logger.error("Create a URLs file with one TikTok URL per line.")
        return 1
    
    # Read URLs
    try:
        urls = read_urls_from_file(config.urls_file)
    except Exception as e:
        logger.error(f"Error reading URLs file: {e}")
        return 1
    
    if not urls:
        logger.error("No URLs found in file")
        return 1
    
    logger.info(f"Found {len(urls)} URLs to process")
    
    # Create output directories
    config.create_directories()
    
    # Load Whisper model
    logger.info(f"Loading Whisper model ({config.whisper_model})...")
    try:
        model = whisper.load_model(config.whisper_model)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load Whisper model: {e}")
        return 1
    
    # Initialize components
    downloader = VideoDownloader(
        download_timeout=config.download_timeout,
        metadata_timeout=config.metadata_timeout
    )
    audio_extractor = AudioExtractor(timeout=config.audio_timeout)
    transcriber = AudioTranscriber(model)
    processor = VideoProcessor(config, downloader, audio_extractor, transcriber)
    
    # Process URLs
    logger.info("Starting processing...")
    successful, failed = processor.process_urls(urls)
    
    # Print summary
    logger.info("=" * 50)
    logger.info(f"Complete! {successful} succeeded, {failed} failed.")
    logger.info(f"Transcripts saved to ./{config.transcript_dir}/")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
