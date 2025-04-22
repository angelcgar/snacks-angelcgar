#!/bin/bash

# Nombre del programa y del script
nombre_programa="today"
script_name="today.sh"

TEMPLATE_DIR="$HOME/.config/today-templates"

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
  echo "Puedes ejecutar el programa con: $nombre_programa"
else
  echo "Error: No se pudo instalar $nombre_programa"
  exit 1
fi

# Crear archivo de configuración
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "Creando directorio de plantillas en $TEMPLATE_DIR..."
  mkdir -p "$TEMPLATE_DIR" || {
    echo "Error: No se pudo crear el directorio de plantillas $TEMPLATE_DIR"
    exit 1
  }
  git clone https://github.com/angelcgar/today-sh-templates.git --depth 1 "$TEMPLATE_DIR"
  rm -rf "$TEMPLATE_DIR/.git"
fi
