#!/bin/bash

# Configuración
TEMPLATE_DIR="$HOME/.config/today-templates"
DEFAULT_TEMPLATE="diario.md"

# Crear directorio de templates si no existe
# mkdir -p "$TEMPLATE_DIR"

# Obtener fechas
# Obtener fecha actual en formato dd-mm-YYYY
fecha=$(date +"%d-%m-%Y")
# Obtener los dos ultimos digitos del año
anio=$(date +"%y")
# Obtener el mes en formato 2 digitos
mes=$(date +"%m")
# Obtener el día en formato 2 digitos
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

  local directorio_de_ejecucion=$(pwd)

  # Determinar ubicación del archivo
  if [ -d "$nombre_directorio" ]; then
    archivo_diario="$nombre_directorio/$fecha.md"
  else
    archivo_diario="$fecha.md"
  fi

  if [ -f "$archivo_diario" ]; then
    echo "El archivo '$archivo_diario' ya existe. Abriendo..."
    ${EDITOR:-xdg-open} "$archivo_diario"
    return 0
  fi

  # TODO: Manejar rutas absolutas en caso de que el script se ejecute desde otro directorio
  if [ "$directorio_de_ejecucion" != "$HOME/Documentos/reflexiones" ]; then
    echo "Error. No estas en la carpeta de tu diario. $HOME/Documentos/reflexiones"
    exit 1
  fi

  # Variables disponibles
  # Numero de la semana relativo al año
  local semana=$(date +"%V")
  # Nombre del día de la semana
  local dia_semana=$(date +"%A")
  # Hora en formato HH:MM
  local hora_actual=$(date +"%H:%M")
  # Nombre del mes en español
  local mes_actual=${meses[$mes]}
  # Año completo
  local anio_completo="20$anio"

  # Crear archivo con template
  if [ -n "$template" ]; then
    if [ -f "$TEMPLATE_DIR/$template.md" ]; then
      # Copiar template y procesar variables
      cp "$TEMPLATE_DIR/$template.md" "$archivo_diario"

      # Sustituir variables básicas
      sed -i "
                s/{{fecha}}/$dia de $mes_actual de $anio_completo/g;
                s/{{dia}}/$dia/g;
                s/{{mes}}/$mes_actual/g;
                s/{{mes_date}}/$mes/g;
                s/{{anio}}/$anio_completo/g;
                s/{{semana}}/$semana/g;
                s/{{dia_semana}}/$dia_semana/g;
                s/{{hora}}/$hora_actual/g;
                s/{{timestamp}}/$(date +"%Y-%m-%d %H:%M:%S")/g
            " "$archivo_diario"

      # Agregar estas líneas al bloque sed -i para sustituir variables
      # s/{{variable_existente}}/valor/g

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

  # Abrir el archivo en editor
  ${EDITOR:-xdg-open} "$archivo_diario"
}

list_templates() {
  echo -e "\nPlantillas disponibles en $TEMPLATE_DIR/:"
  echo "---------------------------------------------"

  if [ ! -d "$TEMPLATE_DIR" ] || [ -z "$(ls -A "$TEMPLATE_DIR")" ]; then
    echo "No hay plantillas disponibles."
    echo "Crea una con: today add-template <nombre>"
    return 1
  fi

  for template in "$TEMPLATE_DIR"/*.md; do
    template_name=$(basename "$template" .md)
    description=$(head -n 1 "$template" | sed -e 's/^# //' -e 's/{{.*}}//g')

    # Marcar plantilla por defecto
    if [ "$template_name.md" == "$DEFAULT_TEMPLATE" ]; then
      default_flag=" (Plantilla por defecto)"
    else
      default_flag=""
    fi

    echo -e "• ${template_name}${default_flag}"
    [ -n "$description" ] && echo "  $description"
  done

  echo -e "\nUsa: today <nombre-plantilla> para usar una"
}

commit_today() {
  local nombre_directorio="$anio-$mes-${meses[$mes]}"
  local archivo_diario="$nombre_directorio/$fecha.md"

  if [ ! -f "$archivo_diario" ]; then
    echo "No se encontró el diario de hoy. Crea uno primero."
    return 1
  fi

  git add "$archivo_diario"
  git commit -m "$fecha"
  echo "Commit creado para el diario de hoy: $archivo_diario"
}

show_help() {
  echo "Uso: today [comando|template]"
  echo ""
  echo "Comandos disponibles:"
  echo "  --help                            Muestra esta ayuda"
  echo "  --directorio                      Crea solo el directorio del mes"
  echo "  --add-template nombre-template    Crea un nuevo template personalizado"
  echo "  --list, -l                        Lista los templates disponibles"
  echo "  --commit-today                    Crea un commit con el diario de hoy"
  echo "  --show-template <nombre-template> Muestra el contenido de un template"
  echo "  template                          Crea el template por defecto"
  echo ""
  echo "Uso con templates:"
  echo "  today                     Crea diario con template por defecto"
  echo "  today <nombre-template>   Crea diario con template específico"
  echo ""
  echo "Ejemplos:"
  echo "  today                       Crea diario del día con template básico"
  echo "  today reflexiones           Usa el template 'reflexiones'"
  echo "  today --add-template ideas  Crea nuevo template llamado 'ideas'"
  echo ""
  echo "Los templates se guardan en: $TEMPLATE_DIR"
}

# Manejo de argumentos
case "$1" in
"template")
  crear_template_por_defecto
  echo "Template por defecto creado en: $TEMPLATE_DIR/$DEFAULT_TEMPLATE"
  ;;
"--directorio")
  crear_directorio
  ;;
"--add-template")
  if [ -z "$2" ]; then
    echo "Uso: $0 add-template <nombre-template>"
    exit 1
  fi
  $EDITOR "$TEMPLATE_DIR/$2.md" || vi "$TEMPLATE_DIR/$2.md"
  ;;
"--list" | "-l")
  list_templates
  exit 0
  ;;
"help" | "--help" | "-h")
  show_help
  exit 0
  ;;
"--commit-today")
  commit_today
  exit 0
  ;;
"--show-template")
  if [ -z "$2" ]; then
    echo "Uso: $0 --show-template <nombre-template>"
    exit 1
  fi
  cat "$TEMPLATE_DIR/$2.md"
  exit 0
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
