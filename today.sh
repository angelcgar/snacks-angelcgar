#!/bin/bash

# Obtener la fecha actual en formato YYYY-MM-DD
fecha=$(date +"%d-%m-%Y")

# Obtener la ruta desde donde se ejecuta el script
ruta=$(pwd)

if [ "$1" == "directorio" ]; then
  anio=$(date +"%y")
  mes=$(date +"%m")
  case $mes in
  "01") mesName="enero" ;;
  "02") mesName="febrero" ;;
  "03") mesName="marzo" ;;
  "04") mesName="abril" ;;
  "05") mesName="mayo" ;;
  "06") mesName="junio" ;;
  "07") mesName="julio" ;;
  "08") mesName="agosto" ;;
  "09") mesName="septiembre" ;;
  "10") mesName="octubre" ;;
  "11") mesName="noviembre" ;;
  "12") mesName="diciembre" ;;
  esac

  mkdir "$anio-$mes-$mesName"
  echo "Directorio '$anio-$mes-$mesName' creado con éxito en $ruta"
  exit 1
fi

# Crear un archivo con la fecha como nombre
touch "$fecha.md"

# Confirmar la creación del archivo y mostrar la ruta
echo "Archivo '$fecha.md' creado con éxito en $ruta"

# Mostrar un pequeño mensaje motivacional o un dato curioso
echo "¡Hoy es un excelente día para seguir creciendo!"
