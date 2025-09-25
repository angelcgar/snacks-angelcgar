#!/bin/bash

# Script: ver_metadata.sh
# Descripción: Visualiza metadatos de archivos según su tipo (imágenes, documentos, multimedia)
# Uso: ./ver_metadata.sh archivo.ext [--brief]
# Opciones:
#   --brief  Muestra sólo información esencial (cuando está disponible)

inicio=2
fin=9
limite_tabla=10

# Función de ayuda
mostrar_ayuda() {
  echo "Uso: $0 [opciones] [inicio] [fin] [limite]"
  echo ""
  echo "Imprime las tablas de multiplicar entre los números especificados."
  echo ""
  echo "Opciones:"
  echo "  -h, --help     Muestra esta ayuda y sale"
  echo ""
  echo "Parámetros:"
  echo "  inicio       Número inicial (por defecto: 2)"
  echo "  fin          Número final (por defecto: 9)"
  echo "  limite       Límite para cada tabla (por defecto: 10)"
  echo ""
  echo "Ejemplos:"
  echo "  $0            # Tablas del 2 al 9 hasta 10"
  echo "  $0 3 5        # Tablas del 3 al 5 hasta 10"
  echo "  $0 4 6 7      # Tablas del 4 al 6 hasta 7"
  exit 0
}

# Procesar opciones
while [[ $# -gt 0 ]]; do
  case "$1" in
  -h | --help)
    mostrar_ayuda
    ;;
  *)
    # El primer argumento no es una opción, salimos del bucle
    break
    ;;
  esac
done

# Procesar parámetros posicionales
if [[ $# -ge 1 ]]; then
  inicio=$1
fi

if [[ $# -ge 2 ]]; then
  fin=$2
fi

if [[ $# -ge 3 ]]; then
  limite_tabla=$3
fi

# Validar parámetros
if [[ $inicio -lt 1 || $fin -lt 1 || $limite_tabla -lt 1 ]]; then
  echo "Error: Los números deben ser positivos." >&2
  exit 1
fi

if [[ $inicio -gt $fin ]]; then
  echo "Error: El número inicial no puede ser mayor que el final." >&2
  exit 1
fi

# Imprimir tablas
echo "Tablas de multiplicar del $inicio al $fin (hasta $limite_tabla)"
echo "------------------------------------------------"

for ((i = $inicio; i <= $fin; i++)); do
  echo ""
  echo "Tabla del $i:"
  echo "------------"

  for ((j = 1; j <= $limite_tabla; j++)); do
    resultado=$((i * j))
    echo "$i x $j = $resultado"
  done
done

echo ""
echo "Fin de las tablas de multiplicar"
