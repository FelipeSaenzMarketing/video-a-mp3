# Video a MP3

Aplicación local con Streamlit que descarga el audio de una URL de video y lo convierte a MP3.

## Requisitos

- Python 3.9 o superior
- FFmpeg (necesario para la conversión de audio)

## Instalación

1. Clona el repositorio y entra en la carpeta:

   ```bash
   git clone https://github.com/FelipeSaenzMarketing/video-a-mp3.git
   cd video-a-mp3
   ```

2. Crea un entorno virtual e instala las dependencias de Python:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install streamlit yt-dlp
   ```

3. Instala FFmpeg si no lo tienes ya en el sistema:

   - **macOS (con Homebrew):**

     ```bash
     brew install ffmpeg
     ```

   - **macOS sin Homebrew:** puedes usar el paquete `ffmpeg-downloader`, que descarga el binario oficial sin necesitar permisos de administrador:

     ```bash
     pip install ffmpeg-downloader
     ffdl install
     ```

     Después, enlaza el binario descargado dentro de `venv/bin` para que la app lo detecte:

     ```bash
     ln -sf "$(python -c 'import ffmpeg_downloader as f; print(f.ffmpeg_path)')" venv/bin/ffmpeg
     ```

   - **Windows / Linux:** descarga FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html) y agrégalo al PATH del sistema.

## Uso

Con el entorno virtual activado:

```bash
streamlit run video_a_mp3.py
```

Esto abre la app en `http://localhost:8501`. Pega la URL de un video, elige la calidad del MP3 y pulsa **Convertir**.

En macOS también puedes usar el acceso directo incluido: doble clic en `Iniciar Video a MP3.command`.

## Aviso

Usa esta herramienta solo con contenido propio o del que tengas derecho a descargar.
