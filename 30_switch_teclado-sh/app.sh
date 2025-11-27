#!/bin/bash

# --- Requisitos --- #
REQUIRED_CMDS=("setxkbmap" "notify-send")

for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ Error: '$cmd' no está instalado. Instálalo y vuelve a ejecutar el script."
        exit 1
    fi
done

# --- Detectar teclado actual --- #
CURRENT_LAYOUT=$(setxkbmap -query | grep layout | awk '{print $2}')

# --- Cambiar layout --- #
if [[ "$CURRENT_LAYOUT" == "us" ]]; then
    setxkbmap latam
    notify-send -i dialog-information "Teclado cambiado" "Ahora estás usando: LATAM"
else
    setxkbmap us
    notify-send -i dialog-information "Teclado cambiado" "Ahora estás usando: US"
fi
