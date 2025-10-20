#!/usr/bin/env bash

# Script: ver_fechas.sh
# Descripción: Muestra información detallada sobre la fecha y hora actual
# Uso: ./ver_fechas.sh [fecha_javascript]
# Versión: 1.5

# Mapeo de meses en inglés
declare -A meses_en=(
  ["01"]="January" ["02"]="February" ["03"]="March" ["04"]="April"
  ["05"]="May" ["06"]="June" ["07"]="July" ["08"]="August"
  ["09"]="September" ["10"]="October" ["11"]="November" ["12"]="December"
)

# Mapeo de días en inglés
declare -A dias_en=(
  ["lunes"]="Monday" ["martes"]="Tuesday" ["miércoles"]="Wednesday"
  ["jueves"]="Thursday" ["viernes"]="Friday" ["sábado"]="Saturday" ["domingo"]="Sunday"
)

# Mapeo de meses en español
declare -A meses_es=(
  ["01"]="enero" ["02"]="febrero" ["03"]="marzo" ["04"]="abril"
  ["05"]="mayo" ["06"]="junio" ["07"]="julio" ["08"]="agosto"
  ["09"]="septiembre" ["10"]="octubre" ["11"]="noviembre" ["12"]="diciembre"
)

# Mapeo de días en español (para conversión desde inglés)
declare -A dias_es_from_en=(
  ["Monday"]="lunes" ["Tuesday"]="martes" ["Wednesday"]="miércoles"
  ["Thursday"]="jueves" ["Friday"]="viernes" ["Saturday"]="sábado" ["Sunday"]="domingo"
)

# Función para procesar fecha JavaScript
procesar_fecha_javascript() {
    local fecha_js="$1"

    # Convertir fecha JavaScript a formato que pueda usar 'date'
    # Eliminar la 'Z' final y los milisegundos si existen
    fecha_clean=$(echo "$fecha_js" | sed 's/\.\([0-9]\{3\}\)Z$/-\1/g' | sed 's/Z$//')

    # Extraer componentes individuales
    anio_completo=$(echo "$fecha_clean" | cut -d'T' -f1 | cut -d'-' -f1)
    mes_numero=$(echo "$fecha_clean" | cut -d'T' -f1 | cut -d'-' -f2)
    dia_numero=$(echo "$fecha_clean" | cut -d'T' -f1 | cut -d'-' -f3)

    # Si hay componente de tiempo, extraerlo
    if [[ "$fecha_clean" == *"T"* ]]; then
        hora_actual=$(echo "$fecha_clean" | cut -d'T' -f2 | cut -d':' -f1-2)
    else
        hora_actual="00:00"
    fi

    # Crear timestamp para usar con date
    timestamp="${anio_completo}-${mes_numero}-${dia_numero} ${hora_actual}"

    # Obtener información formateada
    fecha_actual=$(date -d "$timestamp" +"%d-%m-%Y")
    fecha_iso=$(date -d "$timestamp" +"%Y%m%d")
    fecha_iso_ext=$(date -d "$timestamp" +"%Y-%m-%d")
    anio_abreviado=$(date -d "$timestamp" +"%y")
    semana_anio=$(date -d "$timestamp" +"%V")
    dia_semana_en=$(date -d "$timestamp" +"%A")
    dia_semana_es=${dias_es_from_en[$dia_semana_en]}
    mes_es=${meses_es[$mes_numero]}
    mes_en=${meses_en[$mes_numero]}
}

# Función para fecha actual
usar_fecha_actual() {
    fecha_actual=$(date +"%d-%m-%Y")
    fecha_iso=$(date +"%Y%m%d")
    fecha_iso_ext=$(date +"%Y-%m-%d")
    anio_completo=$(date +"%Y")
    anio_abreviado=$(date +"%y")
    mes_numero=$(date +"%m")
    dia_numero=$(date +"%d")
    semana_anio=$(date +"%V")
    dia_semana_es=$(date +"%A")
    mes_es=$(date +"%B")
    mes_en=${meses_en[$mes_numero]}
    dia_semana_en=${dias_en[$dia_semana_es]}
    hora_actual=$(date +"%H:%M")
}

# Verificar si se proporcionó una fecha JavaScript como argumento
if [ $# -eq 1 ]; then
    if [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} ]]; then
        echo "Procesando fecha JavaScript: $1"
        procesar_fecha_javascript "$1"
        fuente_fecha="JavaScript (proporcionada)"
    else
        echo "Error: Formato de fecha JavaScript no reconocido."
        echo "Formato esperado: YYYY-MM-DDTHH:MM:SS.sssZ"
        exit 1
    fi
else
    # Obtener fecha en formato JavaScript con milisegundos y Z
    fecha_js_sistema=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
    echo "Procesando fecha JavaScript: $fecha_js_sistema"
    usar_fecha_actual
    fuente_fecha="sistema"
fi

# Mostrar información
echo "Información de fecha y hora:"
echo "----------------------------------"
echo "Fuente: $fuente_fecha"
if [ $# -eq 1 ]; then
    echo "Fecha original: $1"
fi
echo "Fecha corta (DD-MM-AAAA): $fecha_actual"
echo "Fecha ISO (AAAAMMDD): $fecha_iso"
echo "Fecha ISO extendida (AAAA-MM-DD): $fecha_iso_ext"
echo "Día del mes: $dia_numero"
echo "Mes: $mes_es ($mes_numero) / $mes_en"
echo "Año: $anio_completo (abreviado: $anio_abreviado)"
echo "Semana del año: $semana_anio"
echo "Día de la semana: $dia_semana_es / $dia_semana_en"
echo "Hora actual: $hora_actual"
echo "----------------------------------"
echo "Fecha completa: $dia_semana_es ($dia_semana_en), $dia_numero de $mes_es ($mes_en) de $anio_completo"
