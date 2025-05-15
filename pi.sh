#!/usr/bin/env bash

# Script: calcular_pi.sh
# Descripción: Calcula e imprime Pi con el número de dígitos especificado (por defecto 10)
# Uso: ./calcular_pi.sh [número-de-dígitos]
# Ejemplo: ./calcular_pi.sh 15

# Función para mostrar ayuda
mostrar_ayuda() {
  echo "Uso: $0 [número-de-dígitos]"
  echo "Ejemplos:"
  echo "  $0       # Muestra 10 dígitos de Pi (por defecto)"
  echo "  $0 15    # Muestra 15 dígitos de Pi"
  echo "  $0 100   # Muestra 100 dígitos de Pi"
}

# Verificar si se pasó un argumento
if [ $# -gt 0 ]; then
  # Verificar si el argumento es un número positivo
  if [[ ! $1 =~ ^[0-9]+$ ]]; then
    echo "Error: '$1' no es un número válido." >&2
    mostrar_ayuda >&2
    exit 1
  fi

  DIGITOS=$1
else
  DIGITOS=10 # Valor por defecto
fi

# Calcular Pi usando bc (scale = dígitos + 1 porque incluye el "3.")
echo "Calculando Pi con $DIGITOS dígitos..."
pi=$(echo "scale=$((DIGITOS + 1)); 4*a(1)" | bc -l 2>/dev/null)

# Verificar si bc está instalado
if [ $? -ne 0 ]; then
  echo "Error: 'bc' no está instalado. Instálalo con:" >&2
  echo "  sudo apt-get install bc  # Debian/Ubuntu" >&2
  echo "  brew install bc          # macOS" >&2
  exit 1
fi

# Mostrar resultado (3 + los dígitos solicitados)
echo "π = ${pi:0:$((DIGITOS + 2))}"
