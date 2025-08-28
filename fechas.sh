#!/usr/bin/env bash

# Script: ver_fechas.sh
# Descripción: Muestra información detallada sobre la fecha y hora actual
# Uso: ./ver_fechas.sh
# Versión: 1.3

# Mapeo de meses en inglés
declare -A meses_en=(
  ["01"]="January" ["02"]="February" ["03"]="March" ["04"]="April"
  ["05"]="May" ["06"]="June" ["07"]="July" ["08"]="August"
  ["09"]="September" ["10"]="October" ["11"]="November" ["12"]="December"
)

# Obtener fecha y hora actual
fecha_actual=$(date +"%d-%m-%Y")
fecha_iso=$(date +"%Y%m%d")          # Formato ISO compacto
fecha_iso_ext=$(date +"%Y-%m-%d")    # Formato ISO estándar con guiones
anio_abreviado=$(date +"%y")
anio_completo=$(date +"%Y")
mes_numero=$(date +"%m")
dia_numero=$(date +"%d")
semana_anio=$(date +"%V")
dia_semana_espanol=$(date +"%A")
mes_espanol=$(date +"%B")            # Mes en español (según locale del sistema)
mes_ingles=${meses_en[$mes_numero]}  # Mes en inglés (mapeo manual)
hora_actual=$(date +"%H:%M")

# Mostrar información
echo "Información de fecha y hora actual:"
echo "----------------------------------"
echo "Fecha corta (DD-MM-AAAA): $fecha_actual"
echo "Fecha ISO (AAAAMMDD): $fecha_iso"
echo "Fecha ISO extendida (AAAA-MM-DD): $fecha_iso_ext"
echo "Día del mes: $dia_numero"
echo "Mes: $mes_espanol ($mes_numero) / $mes_ingles"
echo "Año: $anio_completo (abreviado: $anio_abreviado)"
echo "Semana del año: $semana_anio"
echo "Día de la semana: $dia_semana_espanol"
echo "Hora actual: $hora_actual"
echo "----------------------------------"
echo "Fecha completa: $dia_semana_espanol, $dia_numero de $mes_espanol ($mes_ingles) de $anio_completo"
