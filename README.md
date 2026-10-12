# Video to MP3

A local Streamlit app that downloads the audio from a video URL and converts it to MP3.

## Requirements

- Python 3.9 or higher
- FFmpeg (required for audio conversion)

## Installation

1. Clone the repository and enter the folder:

   ```bash
   git clone https://github.com/FelipeSaenzMarketing/video-a-mp3.git
   cd video-a-mp3
   ```

2. Create a virtual environment and install the Python dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install streamlit yt-dlp
   ```

3. Install FFmpeg if it isn't already on your system:

   - **macOS (with Homebrew):**

     ```bash
     brew install ffmpeg
     ```

   - **macOS without Homebrew:** you can use the `ffmpeg-downloader` package, which downloads the official binary without requiring admin permissions:

     ```bash
     pip install ffmpeg-downloader
     ffdl install
     ```

     Then symlink the downloaded binary into `venv/bin` so the app can detect it:

     ```bash
     ln -sf "$(python -c 'import ffmpeg_downloader as f; print(f.ffmpeg_path)')" venv/bin/ffmpeg
     ```

   - **Windows / Linux:** download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system's PATH.

## Usage

With the virtual environment activated:

```bash
streamlit run video_to_mp3.py
```

This opens the app at `http://localhost:8501`. Paste a video URL, pick the MP3 quality, and click **Convert**.

On macOS you can also use the included shortcut: double-click `Start Video to MP3.command`.

## Disclaimer

Only use this tool with content you own or have the right to download.
