#!/usr/bin/env bash

# Script: ver_fechas.sh
# Descripción: Muestra información detallada sobre la fecha y hora actual
# Uso: ./ver_fechas.sh
# Versión: 1.0

# Mapeo de meses
declare -A meses=(
  ["01"]="enero" ["02"]="febrero" ["03"]="marzo" ["04"]="abril"
  ["05"]="mayo" ["06"]="junio" ["07"]="julio" ["08"]="agosto"
  ["09"]="septiembre" ["10"]="octubre" ["11"]="noviembre" ["12"]="diciembre"
)

# Obtener fecha y hora actual
fecha_actual=$(date +"%d-%m-%Y")
anio_abreviado=$(date +"%y")
anio_completo=$(date +"%Y")
mes_numero=$(date +"%m")
dia_numero=$(date +"%d")
semana_anio=$(date +"%V")
dia_semana_ingles=$(date +"%A")
hora_actual=$(date +"%H:%M")

# Convertir a español
mes_actual=${meses[$mes_numero]}

# Mostrar información
echo "Información de fecha y hora actual:"
echo "----------------------------------"
echo "Fecha corta (DD-MM-AAAA): $fecha_actual"
echo "Día del mes: $dia_numero"
echo "Mes: $mes_actual ($mes_numero)"
echo "Año: $anio_completo (abreviado: $anio_abreviado)"
echo "Semana del año: $semana_anio"
echo "Día de la semana: $dia_semana_ingles"
echo "Hora actual: $hora_actual"
echo "----------------------------------"
echo "Fecha completa: $dia_semana_espanol, $dia_numero de $mes_actual de $anio_completo"
