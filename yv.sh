#!/bin/bash

# Configuración
TEMPLATES_DIR="$HOME/Documentos/plantillas/youtube"
DEFAULT_TEMPLATE="templete.md"

# Funciones
create_project() {
  local project_name="$1"
  local safe_name=$(echo "$project_name" | tr ' ' '_' | tr -cd '[:alnum:]_')

  echo "Creando proyecto: $project_name"
  mkdir -p "$safe_name" || {
    echo "Error al crear directorio"
    exit 1
  }
  cd "$safe_name" || exit 1

  # Estructura de directorios
  declare -A dirs=(
    ["01_Grabacion/Audio_Raw"]=""
    ["01_Grabacion/Video_Raw"]=""
    ["02_Edicion/Proyecto_$safe_name.kdenlive"]=""
    ["02_Edicion/Exportaciones"]=""
    ["03_Recursos/Musica"]=""
    ["03_Recursos/Imagenes"]=""
    ["03_Recursos/Graficos"]=""
    ["04_Guion"]=""
  )

  for dir in "${!dirs[@]}"; do
    mkdir -p "$dir"
  done

  # Archivos iniciales
  touch "04_Guion/Guion_$safe_name.md"
  echo "# Notas del proyecto" >"04_Guion/Notas_$safe_name.txt"

  if [ -f "$TEMPLATES_DIR/$DEFAULT_TEMPLATE" ]; then
    cp "$TEMPLATES_DIR/$DEFAULT_TEMPLATE" "README.md"
  else
    echo "# $project_name" >"README.md"
    echo "## Descripción" >>"README.md"
  fi

  # Inicializar Git
  git init >/dev/null
  git add . >/dev/null
  git commit -m "Initial commit: $project_name" >/dev/null

  echo "✅ Proyecto creado en: $(pwd)"
  tree -L 2
}

show_help() {
  echo "Uso:"
  echo "  yv new <nombre-proyecto>  Crea nuevo proyecto"
  echo "  yv help                  Muestra esta ayuda"
  echo ""
  echo "Ejemplo:"
  echo "  yv new 'Mi Video Epico'"
}

# Main
case "$1" in
"new")
  if [ -z "$2" ]; then
    echo "Error: Falta nombre del proyecto"
    show_help
    exit 1
  fi
  create_project "$2"
  ;;
"help" | "--help" | "-h")
  show_help
  ;;
*)
  echo "Comando no reconocido"
  show_help
  exit 1
  ;;
esac
