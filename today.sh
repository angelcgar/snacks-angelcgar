#!/bin/bash

# Configuración
TEMPLATE_DIR="$HOME/.config/today-templates"
DEFAULT_TEMPLATE="diario.md"

# Crear directorio de templates si no existe
mkdir -p "$TEMPLATE_DIR"

# Obtener fechas
fecha=$(date +"%d-%m-%Y")
anio=$(date +"%y")
mes=$(date +"%m")
dia=$(date +"%d")

# Mapeo de meses
declare -A meses=(
  ["01"]="enero" ["02"]="febrero" ["03"]="marzo" ["04"]="abril"
  ["05"]="mayo" ["06"]="junio" ["07"]="julio" ["08"]="agosto"
  ["09"]="septiembre" ["10"]="octubre" ["11"]="noviembre" ["12"]="diciembre"
)

# Función para crear directorio del mes
crear_directorio() {
  local nombre_directorio="$anio-$mes-${meses[$mes]}"
  mkdir -p "$nombre_directorio"
  echo "Directorio '$nombre_directorio' creado con éxito en $(pwd)"
}

# Función para crear template por defecto si no existe
crear_template_por_defecto() {
  if [ ! -f "$TEMPLATE_DIR/$DEFAULT_TEMPLATE" ]; then
    cat >"$TEMPLATE_DIR/$DEFAULT_TEMPLATE" <<EOF
# Diario del día $dia de ${meses[$mes]} de 20$anio

## Hoy agradezco por:
1. 
2. 
3. 

## Hoy he vivido:
- 

## Lo más destacado del día:
- 

## Buenas suerte en tu día!
EOF
  fi
}

# Función principal para crear el archivo del día
crear_diario() {
  local template="$1"
  local nombre_directorio="$anio-$mes-${meses[$mes]}"
  local archivo_diario

  # Determinar si crear en subdirectorio o directorio actual
  if [ -d "$nombre_directorio" ]; then
    archivo_diario="$nombre_directorio/$fecha.md"
  else
    archivo_diario="$fecha.md"
  fi

  # Crear archivo
  if [ -n "$template" ]; then
    if [ -f "$TEMPLATE_DIR/$template.md" ]; then
      cp "$TEMPLATE_DIR/$template.md" "$archivo_diario"
      sed -i "s/{{fecha}}/$dia de ${meses[$mes]} de 20$anio/g" "$archivo_diario"
      echo "Archivo '$archivo_diario' creado con template '$template'"
    else
      echo "Template '$template' no encontrado. Usando template por defecto."
      crear_template_por_defecto
      cp "$TEMPLATE_DIR/$DEFAULT_TEMPLATE" "$archivo_diario"
    fi
  else
    touch "$archivo_diario"
    echo "Archivo '$archivo_diario' creado (vacío)"
  fi

  # Abrir el archivo en el editor predeterminado (opcional)
  if [ -n "$EDITOR" ]; then
    $EDITOR "$archivo_diario"
  else
    xdg-open "$archivo_diario" 2>/dev/null || echo "Abre manualmente: $archivo_diario"
  fi
}

# Manejo de argumentos
case "$1" in
"directorio")
  crear_directorio
  ;;
"template")
  crear_template_por_defecto
  echo "Template por defecto creado en: $TEMPLATE_DIR/$DEFAULT_TEMPLATE"
  ;;
"add-template")
  if [ -z "$2" ]; then
    echo "Uso: $0 add-template <nombre-template>"
    exit 1
  fi
  $EDITOR "$TEMPLATE_DIR/$2.md" || vi "$TEMPLATE_DIR/$2.md"
  ;;
*)
  crear_diario "$1"
  ;;
esac

# Mensaje motivacional
frases=(
  "¡Hoy es un excelente día para seguir creciendo!"
  "Cada día es una nueva oportunidad para brillar."
  "Escribe tu día como quieres recordarlo."
  "Pequeños pasos cada día llevan a grandes logros."
  "Tu diario es el espejo de tu crecimiento personal."
)
echo "${frases[$RANDOM % ${#frases[@]}]}"
