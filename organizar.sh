#!/bin/bash

# Script mejorado para organizar archivos en directorios específicos
# Versión 2.0

# Configuración de directorios
declare -A DIRECTORIOS=(
  ["LIBROS"]="$HOME/Documentos/Libros"
  ["MUSICA"]="$HOME/Musica"
  ["VIDEOS"]="$HOME/Videos"
  ["IMAGENES"]="$HOME/Imagenes"
  ["DOCUMENTOS"]="$HOME/Documentos"
  ["COMPRIMIDOS"]="$HOME/Documentos/Comprimidos"
  ["PROGRAMAS"]="$HOME/Descargas/Programas"
  ["MISC"]="$HOME/Documentos/Misceláneo"
)

# Extensiones por categoría
declare -A EXTENSIONES=(
  ["LIBROS"]="pdf epub mobi azw3 djvu"
  ["MUSICA"]="mp3 flac wav ogg aac m4a"
  ["VIDEOS"]="mp4 mkv avi mov wmv flv webm"
  ["IMAGENES"]="jpg jpeg png gif svg webp bmp tiff"
  ["DOCUMENTOS"]="doc docx xls xlsx ppt pptx odt ods odp txt rtf csv"
  ["COMPRIMIDOS"]="zip rar 7z tar gz bz2 xz"
  ["PROGRAMAS"]="deb rpm exe appimage dmg pkg"
)

# Colores para mensajes
COLOR_EXITO="\e[32m"
COLOR_ERROR="\e[31m"
COLOR_INFO="\e[34m"
COLOR_ADVERTENCIA="\e[33m"
COLOR_RESET="\e[0m"

# Función para crear directorios si no existen
crear_directorios() {
  echo -e "${COLOR_INFO}Creando directorios si no existen...${COLOR_RESET}"
  for dir in "${DIRECTORIOS[@]}"; do
    mkdir -p "$dir"
  done
}

# Función para mover archivos según su extensión
organizar_archivos() {
  local origen="$1"
  local contador_total=0
  local -A contador_categorias

  echo -e "${COLOR_INFO}Organizando archivos desde: $origen${COLOR_RESET}"

  # Procesar cada categoría
  for categoria in "${!EXTENSIONES[@]}"; do
    local contador=0
    local destino="${DIRECTORIOS[$categoria]}"

    # Procesar cada extensión de la categoría
    for ext in ${EXTENSIONES[$categoria]}; do
      while IFS= read -r -d '' archivo; do
        mv -v "$archivo" "$destino" && ((contador++))
      done < <(find "$origen" -type f ! -path '*/.*' -iname "*.$ext" -print0)
    done

    contador_categorias[$categoria]=$contador
    ((contador_total += contador))
  done

  # Mover archivos restantes a Misceláneo
  local contador_misc=0
  while IFS= read -r -d '' archivo; do
    mv -v "$archivo" "${DIRECTORIOS[MISC]}" && ((contador_misc++))
  done < <(find "$origen" -type f -print0)

  contador_categorias["MISC"]=$contador_misc
  ((contador_total += contador_misc))

  # Mostrar resumen
  echo -e "\n${COLOR_EXITO}Resumen de organización:${COLOR_RESET}"
  for categoria in "${!contador_categorias[@]}"; do
    echo -e "  ${categoria}: ${contador_categorias[$categoria]} archivos"
  done
  echo -e "  ${COLOR_EXITO}TOTAL: $contador_total archivos organizados${COLOR_RESET}"
}

# Función principal
main() {
  local origen="${1:-$HOME/Descargas}"

  if [[ ! -d "$origen" ]]; then
    echo -e "${COLOR_ERROR}El directorio de origen no existe: $origen${COLOR_RESET}"
    exit 1
  fi

  crear_directorios
  organizar_archivos "$origen"

  echo -e "\n${COLOR_EXITO}✅ Organización completada exitosamente.${COLOR_RESET}"
}

# Ejecutar script
main "$@"
