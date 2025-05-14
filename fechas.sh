#!/bin/bash

# Script: ver fechas.sh
# Descripción: Imprime fechas
# Uso: ./fechas.sh

# Obtener fecha actual en formato dd-mm-YYYY
fecha=$(date +"%d-%m-%Y")
# Obtener los dos ultimos digitos del año
anio=$(date +"%y")
# Obtener el mes en formato 2 digitos
mes=$(date +"%m")
# Obtener el día en formato 2 digitos
dia=$(date +"%d")

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

# Mapeo de meses
declare -A meses=(
  ["01"]="enero" ["02"]="febrero" ["03"]="marzo" ["04"]="abril"
  ["05"]="mayo" ["06"]="junio" ["07"]="julio" ["08"]="agosto"
  ["09"]="septiembre" ["10"]="octubre" ["11"]="noviembre" ["12"]="diciembre"
)

echo "La fecha actual es: $fecha"
