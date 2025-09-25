#!/bin/bash

# Script: ver_metadata.sh
# Descripción: Visualiza metadatos de archivos según su tipo (imágenes, documentos, multimedia)
# Uso: ./ver_metadata.sh archivo.ext [--brief]
# Opciones:
#   --brief  Muestra sólo información esencial (cuando está disponible)

archivo="$1"
modo_breve=false

# Verificar si se solicita modo breve
if [[ "$2" == "--brief" ]]; then
  modo_breve=true
fi

# Función para mostrar ayuda
mostrar_ayuda() {
  echo "Uso: $0 archivo.ext [--brief]"
  echo ""
  echo "Visualiza metadatos de archivos soportados:"
  echo "  - Documentos: PDF"
  echo "  - Imágenes: JPG, JPEG, PNG, WEBP, HEIC, TIFF"
  echo "  - Multimedia: MP4, MKV, AVI, MOV, MP3, FLAC, OGG, WAV"
  echo "  - Otros: Intenta con exiftool como predeterminado"
  echo ""
  echo "Opciones:"
  echo "  --brief  Muestra información resumida (cuando está disponible)"
  echo ""
  echo "Dependencias necesarias:"
  echo "  - exiftool (para imágenes y metadatos generales)"
  echo "  - pdfinfo (para documentos PDF)"
  echo "  - mediainfo (para archivos multimedia)"
}

# Verificar si no se proporcionó archivo o se pidió ayuda
if [[ -z "$archivo" || "$archivo" == "-h" || "$archivo" == "--help" ]]; then
  mostrar_ayuda
  exit 1
fi

# Verificar si el archivo existe
if [[ ! -f "$archivo" ]]; then
  echo "Error: El archivo '$archivo' no existe o no es un archivo regular." >&2
  exit 2
fi

# Determinar el tipo de archivo
extension="${archivo##*.}"
extension_lower="${extension,,}" # Convertir a minúsculas

# Procesar según el tipo de archivo
case "$extension_lower" in
pdf)
  if $modo_breve; then
    pdfinfo "$archivo" | grep -E 'Title:|Author:|Creator:|Producer:|CreationDate:|ModDate:|Pages:'
  else
    pdfinfo "$archivo"
  fi
  ;;
jpg | jpeg | png | webp | heic | tiff | tif)
  if $modo_breve; then
    exiftool "$archivo" | grep -E 'File Name|File Size|Image Size|Create Date|Modify Date|Camera Model|Artist|Copyright'
  else
    exiftool "$archivo"
  fi
  ;;
mp4 | mkv | avi | mov | mpg | mpeg | wmv | flv)
  if $modo_breve; then
    mediainfo "$archivo" --Inform="General;%CompleteName%\n%Format%\n%Duration/String3%\n%FileSize/String%\nVideo;%Format%\n%Width%x%Height%\n%FrameRate%\nAudio;%Format%\n%BitRate%\n%Channel(s)%\n%Language%"
  else
    mediainfo "$archivo"
  fi
  ;;
mp3 | flac | ogg | wav | aac | m4a)
  if $modo_breve; then
    mediainfo "$archivo" --Inform="General;%CompleteName%\n%Format%\n%Duration/String3%\n%FileSize/String%\nAudio;%Format%\n%BitRate%\n%Channel(s)%\n%Language%\nID3;%Title%\n%Artist%\n%Album%\n%Track/Position%"
  else
    mediainfo "$archivo"
  fi
  ;;
*)
  echo "Tipo de archivo no reconocido (.$extension). Usando exiftool como predeterminado." >&2
  if $modo_breve; then
    exiftool "$archivo" | head -n 20 # Limitar salida en modo breve para archivos desconocidos
  else
    exiftool "$archivo"
  fi
  ;;
esac

exit 0
