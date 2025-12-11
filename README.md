# Video Transcriber

A modular command-line tool that downloads TikTok videos, extracts audio, and generates transcripts using OpenAI's Whisper model.

## What It Does

1. Reads TikTok URLs from a text file
2. Downloads each video using `yt-dlp`
3. Extracts audio using `ffmpeg`
4. Transcribes audio using Whisper (runs locally, no API costs)
5. Saves transcripts with metadata (creator, views, likes, duration)

## Requirements

- Python 3.10-3.12 (3.13+ not yet supported by Whisper's dependencies)
- ffmpeg
- ~1-4GB disk space for Whisper models

## Installation

### 1. Install system dependencies

**macOS (Homebrew):**
```bash
brew install ffmpeg python@3.12
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg python3.12 python3.12-venv
```

**Windows:**
- Install [Python 3.12](https://www.python.org/downloads/)
- Install [ffmpeg](https://ffmpeg.org/download.html) and add to PATH

### 2. Clone and set up the project

```bash
git clone https://github.com/YOUR_USERNAME/video-transcriber.git
cd video-transcriber

# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### 1. Add URLs to process

Edit `urls.txt` and add TikTok URLs, one per line:

```
https://www.tiktok.com/@username/video/1234567890
https://www.tiktok.com/@another/video/0987654321
# Lines starting with # are ignored
```

### 2. Run the transcriber

```bash
# Using the run script
python run.py

# Or using the module directly
python -m video_transcriber

# With options
python -m video_transcriber --model medium --debug
```

### 3. Find your transcripts

Transcripts are saved to `./transcripts/` with metadata headers:

```
URL: https://www.tiktok.com/@creator/video/123
Creator: creator
Title: My Cool Video
Views: 50000
Likes: 2500
Duration: 45s
Transcribed: 2024-12-10T15:30:00

==================================================

[transcript text here]
```

## Configuration

### Whisper Model Size

Set the `WHISPER_MODEL` environment variable to choose accuracy vs. speed:

| Model  | Size   | Speed    | Accuracy |
|--------|--------|----------|----------|
| tiny   | 39 MB  | Fastest  | Lower    |
| base   | 74 MB  | Fast     | Good     |
| small  | 244 MB | Medium   | Better   |
| medium | 769 MB | Slow     | Great    |
| large  | 1550 MB| Slowest  | Best     |

```bash
# Use medium model for better accuracy
python -m video_transcriber --model medium

# Or with the run script
WHISPER_MODEL=medium python run.py
```

Default is `base` (good balance of speed and accuracy for short TikTok videos).

### Command-Line Options

The transcriber supports various command-line options for customization:

```bash
python -m video_transcriber [OPTIONS]

Options:
  --urls FILE           Path to URLs file (default: urls.txt)
  --model MODEL         Whisper model: tiny, base, small, medium, large (default: base)
  --video-dir DIR       Directory for videos (default: videos)
  --audio-dir DIR       Directory for audio (default: audio)
  --transcript-dir DIR  Directory for transcripts (default: transcripts)
  --debug               Enable debug logging
  --help                Show help message
```

**Examples:**
```bash
# Use custom URLs file and medium model
python -m video_transcriber --urls my_videos.txt --model medium

# Save outputs to custom directories
python -m video_transcriber --video-dir /tmp/videos --transcript-dir ./output

# Enable debug logging for troubleshooting
python -m video_transcriber --debug
```

## Project Structure

```
video-transcriber/
├── src/
│   └── video_transcriber/      # Main package
│       ├── __init__.py         # Package initialization
│       ├── __main__.py         # CLI entry point
│       ├── config.py           # Configuration management
│       ├── downloader.py       # Video downloading
│       ├── audio.py            # Audio extraction
│       ├── transcriber.py      # Transcription logic
│       ├── processor.py        # Main orchestration
│       ├── utils.py            # Utility functions
│       └── exceptions.py       # Custom exceptions
├── run.py                      # Convenience entry point
├── urls.txt                    # Your TikTok URLs (one per line)
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore patterns
├── videos/                     # Downloaded videos (auto-created)
├── audio/                      # Extracted audio (auto-created)
└── transcripts/                # Output transcripts (auto-created)
```

## Features

- **Modular architecture**: Clean separation of concerns with dedicated modules
- **Command-line interface**: Rich CLI with argument parsing and help
- **Smart filenames**: Files are named using creator + title + video ID instead of generic numbers
- **Skip existing**: Re-running won't re-process videos that already have transcripts
- **Metadata preservation**: Each transcript includes view count, likes, duration, and source URL
- **Error handling**: Failed downloads don't stop the batch; you get a summary at the end
- **Timeout protection**: Long-running downloads or transcriptions are killed to prevent hangs
- **Proper logging**: Structured logging with configurable levels (INFO/DEBUG)
- **Type hints**: Full type annotations for better code quality
- **Configurable**: Environment variables and CLI arguments for flexibility

## Troubleshooting

### "No module named whisper"
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
pip install openai-whisper
```

### "yt-dlp: command not found"
```bash
pip install yt-dlp
```

### "ffmpeg: command not found"
Install ffmpeg using your system package manager (see Installation above).

### Python 3.13+ errors
Whisper's `numba` dependency doesn't support Python 3.13 yet. Use Python 3.12:
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download failures
Some TikTok videos have download restrictions. The script will skip these and continue with the rest.

## Use Cases

- Content analysis and pattern extraction
- Creating searchable archives of video content
- Accessibility (converting video to text)
- Research and competitive analysis

## License

MIT License - do whatever you want with it.

## Credits

Built with:
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloading
- [ffmpeg](https://ffmpeg.org/) - Audio extraction
