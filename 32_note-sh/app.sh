#!/usr/bin/env bash
set -euo pipefail

########################################
# Global Configuration
########################################

SCRIPT_VERSION="1.0.0"

# Datos dinámicos de fecha / hora
DATE_FULL="$(date +"%Y%m%d")"
TIME_FULL="$(date +"%H:%M")"
TIME_ID="$(date +"%H%M")"

# Usuario del sistema (puedes cambiarlo a fijo si quieres)
AUTHOR="${USER:-$(whoami)}"

########################################
# Utilidad: slugify título
# Convierte texto a formato apto para ID/archivo
# Normaliza caracteres acentuados (á→a, é→e, etc.)
########################################
slugify() {
  local text="$1"

  # Normalizar caracteres acentuados
  # Primero intentamos con iconv si está disponible
  if command -v iconv >/dev/null 2>&1; then
    text=$(echo "$text" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$text")
  fi

  # Normalización manual como fallback o complemento
  text=$(echo "$text" | sed 'y/ÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜÑ/AEIOUAEIOUAEIOUAEIOUN/')
  text=$(echo "$text" | sed 'y/áéíóúàèìòùâêîôûäëïöüñ/aeiouaeiouaeiouaeioun/')

  # Convertir a minúsculas, reemplazar no-alfanuméricos con guiones
  echo "$text" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g' \
    | sed -E 's/^-+|-+$//g'
}

########################################
# Mostrar ayuda
########################################
show_help() {
cat <<EOF
Usage:
  note.sh [template] [title]

Templates disponibles:
  (vacío)    → plantilla simple por defecto
  uni        → plantilla universitaria

Ejemplos:
  ./nota
  ./nota uni "Algoritmos Clase 1"
  ./nota default "Idea rápida"

Opciones:
  -h, --help     Mostrar ayuda
  -v, --version  Mostrar versión
EOF
}

########################################
# Mostrar versión
########################################
show_version() {
  echo "note.sh version ${SCRIPT_VERSION}"
}

########################################
# TEMPLATE: simple / default
########################################
generate_default_template() {
  local title="$1"
  local slug
  slug="$(slugify "$title")"
  local id="${DATE_FULL}_${TIME_ID}-${slug}"
  local filename="${id}.md"

cat > "$filename" <<EOF
---
id: ${id}
aliases:
  - "${title}"
tags: []
author: ${AUTHOR}
hours: ${TIME_FULL}
---

# ${title}

Notas rápidas aquí…
EOF

  echo "✔️ Nota creada: ${filename}"
}

########################################
# TEMPLATE: universitaria
# Más estructurada para clase
########################################
generate_uni_template() {
  local title="$1"
  local slug
  slug="$(slugify "$title")"
  local id="${DATE_FULL}_${TIME_ID}-${slug}"
  local filename="${id}.md"

cat > "$filename" <<EOF
---
id: ${id}
aliases:
  - "${title}"
tags: [university]
author: ${AUTHOR}
hours: ${TIME_FULL}
---

# ${title}

## 🎯 Objetivo de la clase
-

---

## 🧠 Conceptos clave
- **Concepto:** explicación corta

---

## 📓 Desarrollo
Escribe las ideas principales aquí.

---

## 🧮 Ejemplos
1.

---

## ✅ Puntos importantes
-

---

## 🧩 Fórmulas
-

---

## 📝 Tareas
- [ ]

---

## 🔍 Dudas
-

---

## 🧾 Resumen final
Idea clave aquí.
EOF

  echo "✔️ Nota creada (plantilla universidad): ${filename}"
}

########################################
# MAIN LOGIC
########################################

# Flags
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  show_help
  exit 0
fi

if [[ "${1:-}" == "-v" || "${1:-}" == "--version" ]]; then
  show_version
  exit 0
fi

TEMPLATE="${1:-default}"
TITLE="${2:-Nueva nota}"

case "$TEMPLATE" in
  ""|default)
    generate_default_template "$TITLE"
    ;;
  uni)
    generate_uni_template "$TITLE"
    ;;
  *)
    echo "⚠️  Plantilla desconocida: '$TEMPLATE'"
    echo
    show_help
    exit 1
    ;;
esac
