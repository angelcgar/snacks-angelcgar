#!/bin/bash

# Script: i-sh.sh
# Descripción: Instala las dependencias de un proyecto de nodejs
# Uso: i

# Verificar si existe package.json
if [ ! -f "package.json" ]; then
    echo "Error: No se encontró package.json en el directorio actual." >&2
    exit 1
fi

# Intentar con pnpm
if command -v pnpm &> /dev/null; then
    echo "Instalando dependencias con pnpm..."
    pnpm install
    exit $?
fi

# Intentar con bun
if command -v bun &> /dev/null; then
    echo "pnpm no encontrado. Intentando con bun..."
    bun install
    exit $?
fi

# Intentar con npm como última opción
if command -v npm &> /dev/null; then
    echo "pnpm y bun no encontrados. Intentando con npm..."
    npm install
    exit $?
fi

# Si no se encuentra ningún gestor de paquetes
echo "Error: No se encontró pnpm, bun ni npm en el sistema." >&2
exit 1
