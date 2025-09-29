#!/bin/bash

# === Configuración ===
BASE_DIR="$HOME/Documentos/CVs"
NAME_PREFIX="AngelContreras_Resumen"

# Tecnologías y sus patrones de búsqueda (puedes agregar más)
declare -A TECH_PATTERNS=(
  ["react"]="react|React|jsx|JSX"
  ["angular"]="angular|Angular|ng|NG"
  ["vue"]="vue|Vue|vite|Vite"
  ["python"]="python|Python|django|Django|flask|Flask"
  ["java"]="java|Java|spring|Spring"
  ["node"]="node|Node|express|Express"
  ["php"]="php|PHP|laravel|Laravel"
  ["net"]="net|NET|asp|ASP|csharp|CSharp"
)

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
    echo "❌ Error: El archivo '$file' no es un PDF."
    exit 1
  fi
}

# Detecta la tecnología del CV
detect_technology() {
  local file="$1"
  local filename=$(basename "$file")

  for tech in "${!TECH_PATTERNS[@]}"; do
    if echo "$filename" | grep -E -q "${TECH_PATTERNS[$tech]}"; then
      echo "$tech"
      return 0
    fi
  done

  echo "general"
}

# Detecta el idioma del CV
detect_language() {
  local file="$1"
  local filename=$(basename "$file")

  # BUG: solo detecta ES o IN
  if echo "$filename" | grep -E -q "ES|es|Español|español"; then
    echo "es"
  elif echo "$filename" | grep -E -q "IN|in|EN|en|English|english"; then
    echo "in"
  else
    echo "❌ Error: No se pudo detectar el idioma. Usa 'ES' o 'IN' en el nombre."
    exit 1
  fi
}

# Copia y renombra el archivo según tecnología e idioma
copy_cv() {
  local file="$1"
  local tech="$2"
  local lang="$3"

  # Directorio destino
  local target_dir="$BASE_DIR/$tech/$lang"

  # Crear directorio si no existe
  mkdir -p "$target_dir"

  # Nuevo nombre del archivo
  local new_filename="${NAME_PREFIX}.pdf"
  local target_path="$target_dir/$new_filename"

  # Copiar archivo
  cp "$file" "$target_path"

  echo "✅ Copiado a: $target_path"
  echo "📁 Tecnología: $tech | Idioma: $lang"
}

# Muestra ayuda
show_help() {
  echo "ESTE SCRIPT ESTA EN DESUSO, NO USAR"
  echo "VER -> 25_actualizar-cv-py"
  echo ""
  echo "📋 Uso: $0 <archivo.pdf>"
  echo ""
  echo "Organiza CVs por tecnología e idioma:"
  echo "  - Tecnologías detectadas: ${!TECH_PATTERNS[*]}"
  echo "  - Idiomas: es (español), in (inglés)"
  echo ""
  echo "Ejemplos de nombres:"
  echo "  - CV_React_ES.pdf → ~/Documentos/CVs/react/es/"
  echo "  - Resume_Angular_IN.pdf → ~/Documentos/CVs/angular/in/"
  echo "  - Angel_Java_ES.pdf → ~/Documentos/CVs/java/es/"
  echo ""
  echo "Patrones de detección:"
  for tech in "${!TECH_PATTERNS[@]}"; do
    echo "  - $tech: ${TECH_PATTERNS[$tech]}"
  done
}

# === Programa principal ===
main() {
  local file="$1"

  # Mostrar ayuda si no hay argumentos o con -h/--help
  if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
  fi

  check_argument "$file"
  check_pdf "$file"

  # Detectar tecnología e idioma
  local technology=$(detect_technology "$file")
  local language=$(detect_language "$file")

  echo "🔍 Analizando: $(basename "$file")"
  echo "💻 Tecnología detectada: $technology"
  echo "🌐 Idioma detectado: $language"

  # Copiar archivo
  copy_cv "$file" "$technology" "$language"
}

main "$1"
