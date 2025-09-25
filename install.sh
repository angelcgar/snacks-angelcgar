#!/bin/bash

# Nombre del programa y del script
nombre_programa="inicio"
script_name="inicio.sh"

# Directorio de instalación
install_dir="$HOME/.local/bin"

# Verificar si el directorio de instalación existe
if [ ! -d "$install_dir" ]; then
  echo "Error: El directorio de instalación $install_dir no existe."
  echo "Creando directorio..."
  mkdir -p "$install_dir" || {
    echo "Error: No se pudo crear el directorio $install_dir"
    exit 1
  }
fi

# Verificar si el script fuente existe
if [ ! -f "$script_name" ]; then
  echo "Error: El archivo $script_name no existe en el directorio actual."
  exit 1
fi

# Verificar permisos de ejecución
if [ ! -x "$script_name" ]; then
  echo "Otorgando permisos de ejecución a $script_name..."
  chmod +x "$script_name" || {
    echo "Error: No se pudo dar permisos de ejecución a $script_name"
    exit 1
  }
fi

# Instalar el programa
echo "Instalando $nombre_programa en $install_dir..."
if cp "$script_name" "$install_dir/$nombre_programa"; then
  chmod +x "$install_dir/$nombre_programa"
  echo "Instalación completada exitosamente."
  echo "Puedes ejecutar el programa con: $nombre_programa archivo_interes.ext"
else
  echo "Error: No se pudo instalar $nombre_programa"
  exit 1
fi
