"""
Video URL -> MP3 con Streamlit
Requisitos:
    pip install streamlit yt-dlp
    FFmpeg instalado en el sistema (https://ffmpeg.org/download.html)
Ejecutar:
    streamlit run video_a_mp3.py
"""

import shutil
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

st.set_page_config(page_title="Video a MP3", page_icon="🎵", layout="centered")
st.title("🎵 Convertidor de video a MP3")
st.write("Pega la URL de un video y descarga su audio en formato MP3.")

# Verificar FFmpeg
if shutil.which("ffmpeg") is None:
    st.error("No se encontró FFmpeg en el sistema. Instálalo y vuelve a intentarlo.")
    st.stop()

url = st.text_input("URL del video", placeholder="https://...")
calidad = st.selectbox("Calidad del MP3 (kbps)", ["128", "192", "256", "320"], index=1)


def progreso_hook(barra, texto):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            descargado = d.get("downloaded_bytes", 0)
            if total:
                barra.progress(min(descargado / total, 1.0))
                texto.text(f"Descargando... {descargado / total:.0%}")
        elif d["status"] == "finished":
            barra.progress(1.0)
            texto.text("Descarga completa. Convirtiendo a MP3...")
    return hook


def convertir_a_mp3(url: str, calidad: str, carpeta: Path, hook) -> Path:
    opciones = {
        "format": "bestaudio/best",
        "outtmpl": str(carpeta / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "progress_hooks": [hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": calidad,
            }
        ],
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

    archivos = list(carpeta.glob("*.mp3"))
    if not archivos:
        raise FileNotFoundError("No se generó el archivo MP3.")
    return archivos[0]


if st.button("Convertir", type="primary", disabled=not url):
    barra = st.progress(0.0)
    texto = st.empty()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            mp3 = convertir_a_mp3(url.strip(), calidad, Path(tmp), progreso_hook(barra, texto))
            datos = mp3.read_bytes()
            nombre = mp3.name

        texto.text("¡Listo!")
        st.success(f"Conversión completada: {nombre}")
        st.audio(datos, format="audio/mp3")
        st.download_button(
            "⬇️ Descargar MP3",
            data=datos,
            file_name=nombre,
            mime="audio/mpeg",
        )
    except yt_dlp.utils.DownloadError as e:
        st.error(f"No se pudo descargar el video: {e}")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

st.caption("Usa esta herramienta solo con contenido propio o que tengas derecho a descargar.")
