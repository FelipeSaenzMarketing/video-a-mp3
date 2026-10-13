"""
Video URL -> MP3 with Streamlit
Requirements:
    pip install streamlit yt-dlp
    FFmpeg installed on the system (https://ffmpeg.org/download.html)
Run:
    streamlit run video_to_mp3.py
"""

import shutil
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

from branding import apply_branding, brand_header, project_panel, signature

st.set_page_config(page_title="Video to MP3 Converter", layout="centered")

apply_branding()
brand_header(
    "Video to MP3 Converter",
    "Extract the audio from any video URL and download it as an MP3 file.",
    kicker="Media Tools",
)
project_panel(
    "Paste the link to a video and this tool downloads its best available audio track, "
    "converts it to MP3 with FFmpeg and gives you a file ready to play or download. "
    "Everything runs locally on your machine.",
    points=[
        "Paste the video URL.",
        "Choose the MP3 bitrate (higher means better quality and a larger file).",
        "Click Convert, then download the result.",
    ],
)

# Check for FFmpeg
if shutil.which("ffmpeg") is None:
    st.error("FFmpeg was not found on this system. Please install it and try again.")
    st.stop()

url = st.text_input("Video URL", placeholder="https://...")
quality = st.selectbox("MP3 quality (kbps)", ["128", "192", "256", "320"], index=1)


def progress_hook(bar, status_text):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                bar.progress(min(downloaded / total, 1.0))
                status_text.text(f"Downloading... {downloaded / total:.0%}")
        elif d["status"] == "finished":
            bar.progress(1.0)
            status_text.text("Download complete. Converting to MP3...")
    return hook


def convert_to_mp3(url: str, quality: str, folder: Path, hook) -> Path:
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(folder / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "progress_hooks": [hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    files = list(folder.glob("*.mp3"))
    if not files:
        raise FileNotFoundError("The MP3 file was not generated.")
    return files[0]


if st.button("Convert", type="primary", disabled=not url):
    bar = st.progress(0.0)
    status_text = st.empty()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            mp3 = convert_to_mp3(url.strip(), quality, Path(tmp), progress_hook(bar, status_text))
            data = mp3.read_bytes()
            name = mp3.name

        status_text.text("Done!")
        st.success(f"Conversion complete: {name}")
        st.audio(data, format="audio/mp3")
        st.download_button(
            "Download MP3",
            data=data,
            file_name=name,
            mime="audio/mpeg",
        )
    except yt_dlp.utils.DownloadError as e:
        st.error(f"Could not download the video: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.caption("Only use this tool with content you own or have the right to download.")

signature()
