#!/bin/bash

# Script: inicio.sh
# Descripción: Resolver el bug temporal de el arranque de los inconos de audio
# Uso: ./inicio.sh
# Opciones:
#

# Función para pausar la ejecución
sleep_seconds() {
    sleep $1
}

echo "Iniciando el icono de volumen..."
volumeicon &

sleep_seconds 2  # Espera 2 segundos para que volumeicon se inicie completamente

echo "Icono de volumen iniciado correctamente"

sleep_seconds 1  # Espera 1 segundo antes de mostrar el siguiente mensaje

echo "Abriendo htop"

sleep_seconds 1  # Espera 1 segundo antes de abrir htop

htop
