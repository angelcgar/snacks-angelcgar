#!/bin/bash

BASENAME="output"
EXT="mp4"
FILE="$BASENAME.$EXT"
i=1

# Buscar un nombre libre
while [ -e "$FILE" ]; do
  FILE="${BASENAME}${i}.${EXT}"
  ((i++))
done

echo "🎥 Grabando pantalla en: $FILE"
echo "⏹️  Detén con Ctrl+C"

# Ajustar el comando según tus necesidades
ffmpeg -video_size 1366x768 -framerate 24 \
  -f x11grab -i :0.0 \
  -vf scale=1280:720 \
  -c:v libx264 -preset fast -crf 26 \
  "$FILE"
