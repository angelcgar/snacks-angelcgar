#!/bin/bash

# Script: ver_metadata.sh
# Descripción: Visualiza metadatos de archivos según su tipo (imágenes, documentos, multimedia)
# Uso: ./ver_metadata.sh archivo.ext [--brief]
# Opciones:
#   --brief  Muestra sólo información esencial (cuando está disponible)

echo "Tablas de multiplicar del 2 al 9"
echo "--------------------------------"

for ((i = 2; i <= 9; i++)); do
  echo ""
  echo "Tabla del $i:"
  echo "------------"

  for ((j = 1; j <= 10; j++)); do
    resultado=$((i * j))
    echo "$i x $j = $resultado"
  done
done

echo ""
echo "Fin de las tablas de multiplicar"
