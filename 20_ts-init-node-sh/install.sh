#!/bin/bash

# Nombre del programa y del script
nombre_programa="ts-init-node"
script_name="ts-init-node.sh"

# Directorio de instalación
install_dir="$HOME/.local/bin"
template_dir="$HOME/.config/ts-init-node"

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

# Instalar template
echo "Instalando template..."
if [ ! -d "$template_dir" ]; then
  echo "Creando directorio de templates..."
  mkdir -p "$template_dir"
fi

if [ ! -f "$template_dir/gitignore.bash" -o ! -f "$template_dir/LICENSE" ]; then
  git clone https://github.com/angelcgar/ts-init-node-templates "$template_dir"
  rm -rf "$template_dir/.git"
  echo "Template instalado correctamente."
fi
