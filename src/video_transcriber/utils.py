"""Utility functions for video transcriber."""

import re
import logging
from typing import List

logger = logging.getLogger(__name__)


def sanitize_filename(name: str, max_length: int = 50) -> str:
    """
    Remove invalid characters and truncate filename.
    
    Args:
        name: The filename to sanitize
        max_length: Maximum length for the filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces and multiple underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    # Truncate and strip
    return sanitized[:max_length].strip('_')


def read_urls_from_file(filepath: str) -> List[str]:
    """
    Read URLs from a text file, filtering out comments and empty lines.
    
    Args:
        filepath: Path to the file containing URLs
        
    Returns:
        List of URLs
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    logger.info(f"Reading URLs from {filepath}")
    with open(filepath, "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    logger.info(f"Found {len(urls)} URLs")
    return urls


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
