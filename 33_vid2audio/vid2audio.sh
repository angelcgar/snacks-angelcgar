#!/usr/bin/env bash

# vid2audio - Extrae audio de videos y convierte a MP3
# Utiliza ffmpeg para extraer audio con buena calidad

set -euo pipefail

show_help() {
  echo "Uso: vid2audio <video_entrada> [audio_salida]"
  echo
  echo "Convierte un video a MP3 con buena calidad sin pesar demasiado."
  echo
  echo "Argumentos:"
  echo "  video_entrada   Archivo de video (mp4 u otro soportado por ffmpeg)"
  echo "  audio_salida    (Opcional) Nombre del archivo de salida .mp3"
  echo
  echo "Opciones:"
  echo "  -h, --help      Muestra esta ayuda"
  echo
  echo "Ejemplo:"
  echo "  vid2audio video.mp4 salida.mp3"
  echo
  echo "Si no se especifica salida:"
  echo "  vid2audio video.mp4   -> genera video.mp3"
}

# Si pide ayuda
if [[ "$1" == "-h" || "$1" == "--help" ]] 2>/dev/null; then
  show_help
  exit 0
fi

# Validar entrada
if [[ -z "${1:-}" ]]; then
  echo "❌ Error: No se proporcionó archivo de entrada."
  show_help
  exit 1
fi

INPUT="$1"

if [[ ! -f "$INPUT" ]]; then
  echo "❌ Error: El archivo '$INPUT' no existe."
  exit 1
fi

# Validar que ffmpeg esté instalado
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "❌ Error: ffmpeg no está instalado."
  echo "Instala ffmpeg para usar este script."
  exit 1
fi

# Salida opcional
if [[ -z "${2:-}" ]]; then
  BASENAME=$(basename "$INPUT")
  OUTPUT="${BASENAME%.*}.mp3"
else
  OUTPUT="$2"
fi

echo "🎧 Extrayendo audio..."
echo "Entrada: $INPUT"
echo "Salida : $OUTPUT"

ffmpeg -i "$INPUT" -vn -acodec libmp3lame -q:a 2 "$OUTPUT"

if [[ $? -eq 0 ]]; then
  echo "✅ Listo!"
else
  echo "❌ Error al procesar el video."
  exit 1
fi
