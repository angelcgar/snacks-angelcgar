#!/bin/bash

archivo="$1"

if [[ -z "$archivo" ]]; then
  echo "Uso: ./ver_metadata.sh archivo.ext"
  exit 1
fi

case "$archivo" in
*.pdf) pdfinfo "$archivo" ;;
*.jpg | *.jpeg | *.png | *.webp) exiftool "$archivo" ;;
*.mp4 | *.mkv | *.avi | *.mov) mediainfo "$archivo" ;;
*.mp3 | *.flac | *.ogg) mediainfo "$archivo" ;;
*)
  echo "Tipo de archivo no reconocido. Usando exiftool como predeterminado."
  exiftool "$archivo"
  ;;
esac
