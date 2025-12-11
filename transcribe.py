#!/usr/bin/env python3
"""
TikTok Transcriber

DEPRECATED: This script is kept for backward compatibility.
Please use: python -m video_transcriber or python run.py

Downloads TikTok videos, extracts audio, and generates transcripts using Whisper.
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "transcribe.py is deprecated. Please use 'python -m video_transcriber' or 'python run.py' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import and run the new implementation
try:
    from src.video_transcriber.__main__ import main
    sys.exit(main())
except ImportError:
    # Fallback to old implementation if new modules not available
    import subprocess
    import os
    import re
    import json
    from datetime import datetime

    try:
        import whisper
    except ImportError:
        print("Error: openai-whisper not installed. Run: pip install openai-whisper")
        sys.exit(1)


    def sanitize_filename(name: str, max_length: int = 50) -> str:
        """Remove invalid characters and truncate filename."""
        # Remove invalid filename characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace spaces and multiple underscores
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = re.sub(r'_+', '_', sanitized)
        # Truncate and strip
        return sanitized[:max_length].strip('_')


    def get_video_info(url: str) -> dict:
        """Fetch video metadata using yt-dlp without downloading."""
        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-download", url],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"  Warning: Could not fetch metadata - {e}")
        return {}


    def download_video(url: str, output_path: str) -> bool:
        """Download video using yt-dlp."""
        try:
            result = subprocess.run(
                ["yt-dlp", "-o", output_path, "-f", "mp4", url],
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0 and os.path.exists(output_path)
        except subprocess.TimeoutExpired:
            print("  Error: Download timed out")
            return False


    def extract_audio(video_path: str, audio_path: str) -> bool:
        """Extract audio from video using ffmpeg."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-y", audio_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0 and os.path.exists(audio_path)
        except subprocess.TimeoutExpired:
            print("  Error: Audio extraction timed out")
            return False


    def transcribe_audio(model, audio_path: str) -> str:
        """Transcribe audio file using Whisper."""
        try:
            result = model.transcribe(audio_path)
            return result.get("text", "")
        except Exception as e:
            print(f"  Error during transcription: {e}")
            return ""


    def main():
        # Configuration
        urls_file = "urls.txt"
        model_size = os.environ.get("WHISPER_MODEL", "base")  # base, small, medium, large
        
        # Create output directories
        dirs = ["videos", "audio", "transcripts"]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        
        # Check for urls.txt
        if not os.path.exists(urls_file):
            print(f"Error: {urls_file} not found.")
            print("Create a urls.txt file with one TikTok URL per line.")
            sys.exit(1)
        
        # Read URLs
        with open(urls_file, "r") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        if not urls:
            print("No URLs found in urls.txt")
            sys.exit(1)
        
        print(f"Found {len(urls)} URLs to process.\n")
        
        # Load Whisper model
        print(f"Loading Whisper model ({model_size})...")
        model = whisper.load_model(model_size)
        print("Model loaded.\n")
        
        # Process each URL
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] Processing: {url}")
            
            # Get video metadata for filename
            info = get_video_info(url)
            
            if info:
                creator = info.get("uploader", "unknown")
                title = info.get("title", f"video_{i}")
                video_id = info.get("id", str(i))
                base_name = sanitize_filename(f"{creator}_{title}_{video_id}")
            else:
                base_name = f"video_{i}"
            
            video_path = f"videos/{base_name}.mp4"
            audio_path = f"audio/{base_name}.mp3"
            transcript_path = f"transcripts/{base_name}.txt"
            
            # Skip if transcript already exists
            if os.path.exists(transcript_path):
                print("  Skipping - transcript already exists")
                successful += 1
                continue
            
            # Download video
            print("  Downloading...")
            if not download_video(url, video_path):
                print("  FAILED: Could not download video")
                failed += 1
                continue
            
            # Extract audio
            print("  Extracting audio...")
            if not extract_audio(video_path, audio_path):
                print("  FAILED: Could not extract audio")
                failed += 1
                continue
            
            # Transcribe
            print("  Transcribing...")
            transcript = transcribe_audio(model, audio_path)
            
            if not transcript:
                print("  FAILED: Could not transcribe audio")
                failed += 1
                continue
            
            # Save transcript with metadata
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                if info:
                    f.write(f"Creator: {info.get('uploader', 'Unknown')}\n")
                    f.write(f"Title: {info.get('title', 'Unknown')}\n")
                    f.write(f"Views: {info.get('view_count', 'Unknown')}\n")
                    f.write(f"Likes: {info.get('like_count', 'Unknown')}\n")
                    f.write(f"Duration: {info.get('duration', 'Unknown')}s\n")
                f.write(f"Transcribed: {datetime.now().isoformat()}\n")
                f.write(f"\n{'='*50}\n\n")
                f.write(transcript)
            
            print(f"  Done! Saved to {transcript_path}\n")
            successful += 1
        
        # Summary
        print("=" * 50)
        print(f"Complete! {successful} succeeded, {failed} failed.")
        print(f"Transcripts saved to ./transcripts/")


    if __name__ == "__main__":
        main()

