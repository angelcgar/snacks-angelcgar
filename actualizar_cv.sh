#!/bin/bash

# === Funciones ===

# Verifica que se haya pasado un argumento
check_argument() {
  if [ -z "$1" ]; then
    echo "❌ Error: No se pasó ningún archivo."
    exit 1
  fi
}

# Verifica que el archivo sea PDF
check_pdf() {
  local file="$1"
  if [[ "${file##*.}" != "pdf" ]]; then
    echo "❌ Error: El archivo no es un PDF."
    exit 1
  fi
}

# Copia y renombra el archivo según idioma
copy_cv() {
  local file="$1"

  # Directorios destino
  local dir_es="$HOME/Documentos/CV/ES"
  local dir_in="$HOME/Documentos/CV/IN"

  mkdir -p "$dir_es" "$dir_in"

  if [[ "$file" == *ES*.pdf ]]; then
    cp "$file" "$dir_es/AngelContreras_Resume.pdf"
    echo "✅ Copiado a $dir_es/AngelContreras_Resume.pdf"
  elif [[ "$file" == *IN*.pdf ]]; then
    cp "$file" "$dir_in/AngelContreras_Resume.pdf"
    echo "✅ Copiado a $dir_in/AngelContreras_Resume.pdf"
  else
    echo "❌ Error: El archivo no contiene 'ES' o 'IN' en el nombre."
    exit 1
  fi
}

# === Programa principal ===
main() {
  local file="$1"
  check_argument "$file"
  check_pdf "$file"
  copy_cv "$file"
}

main "$1"
