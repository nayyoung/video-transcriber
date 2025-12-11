#!/usr/bin/env python3
"""
Video Transcriber - Entry point script.

This script provides a convenient way to run the video transcriber.
For more options, use: python -m video_transcriber --help
"""

import sys
from src.video_transcriber.__main__ import main

if __name__ == "__main__":
    sys.exit(main())
