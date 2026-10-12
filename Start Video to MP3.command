#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run video_to_mp3.py
