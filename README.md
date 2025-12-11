# TikTok Transcriber

A command-line tool that downloads TikTok videos, extracts audio, and generates transcripts using OpenAI's Whisper model.

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
git clone https://github.com/YOUR_USERNAME/tiktok-transcriber.git
cd tiktok-transcriber

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
python transcribe.py
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
WHISPER_MODEL=medium python transcribe.py
```

Default is `base` (good balance of speed and accuracy for short TikTok videos).

## Project Structure

```
tiktok-transcriber/
├── transcribe.py      # Main script
├── urls.txt           # Your TikTok URLs (one per line)
├── requirements.txt   # Python dependencies
├── README.md
├── .gitignore
├── videos/            # Downloaded videos (auto-created)
├── audio/             # Extracted audio (auto-created)
└── transcripts/       # Output transcripts (auto-created)
```

## Features

- **Smart filenames**: Files are named using creator + title + video ID instead of generic numbers
- **Skip existing**: Re-running won't re-process videos that already have transcripts
- **Metadata preservation**: Each transcript includes view count, likes, duration, and source URL
- **Error handling**: Failed downloads don't stop the batch; you get a summary at the end
- **Timeout protection**: Long-running downloads or transcriptions are killed to prevent hangs

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
