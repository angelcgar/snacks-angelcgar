#!/bin/bash

# Obtener la fecha actual en formato YYYY-MM-DD
fecha=$(date +"%d-%m-%Y")

# Obtener la ruta desde donde se ejecuta el script
ruta=$(pwd)

# Crear un archivo con la fecha como nombre
touch "$fecha.md"

# Confirmar la creación del archivo y mostrar la ruta
echo "Archivo '$fecha.md' creado con éxito en $ruta"

# Mostrar un pequeño mensaje motivacional o un dato curioso
echo "¡Hoy es un excelente día para seguir creciendo!"
