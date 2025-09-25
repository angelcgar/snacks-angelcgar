#!/bin/bash

# Script: renombrar_minusculas.sh
# Descripcion: Renombra todos los archivos en el directorio actual cambiando sus nombres a minúsculas,
#              manteniendo los caracteres especiales sin modificaciones.
# Uso: ./renombrar_minusculas.sh

echo "Iniciando renombrado de archivos a minúsculas..."

# Itera sobre todos los archivos en el directorio actual
for file in *; do
  # Verifica que el archivo exista (para evitar problemas con patrones no coincidentes)
  if [ -e "$file" ]; then
    # Obtiene el nombre del archivo en minúsculas
    newname=$(echo "$file" | tr '[:upper:]' '[:lower:]')

    # Solo renombra si el nombre ha cambiado
    if [ "$file" != "$newname" ]; then
      # Verifica si ya existe un archivo con el nuevo nombre
      if [ -e "$newname" ]; then
        echo "Advertencia: $newname ya existe. No se renombró $file"
      else
        # Renombra el archivo
        mv -v "$file" "$newname"
      fi
    fi
  fi
done

echo "Proceso completado."
