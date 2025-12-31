#!/usr/bin/env bash

# Script de desinstalación para vid2audio
# Elimina el comando instalado en ~/.local/bin/

set -euo pipefail

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

# Configuración
SCRIPT_NAME="vid2audio"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"

# Función para imprimir mensajes de error
print_error() {
  echo -e "${RED}❌ Error: $1${NC}" >&2
}

# Función para imprimir mensajes de éxito
print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Función para imprimir mensajes informativos
print_info() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

# Función para imprimir advertencias
print_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

# Función: Verificar si el script está instalado
check_script_exists() {
  print_info "Verificando instalación..."

  if [[ ! -f "$SCRIPT_PATH" ]]; then
    print_error "'$SCRIPT_NAME' no está instalado en '$INSTALL_DIR'"
    exit 1
  fi

  print_success "Script encontrado en '$SCRIPT_PATH'"
}

# Función: Confirmar desinstalación
confirm_uninstall() {
  echo
  print_warning "¿Estás seguro de que deseas desinstalar '$SCRIPT_NAME'?"
  read -p "Escribe 'si' para confirmar: " -r
  echo

  if [[ ! $REPLY == "si" ]]; then
    echo "Desinstalación cancelada."
    exit 0
  fi
}

# Función: Eliminar el script
remove_script() {
  print_info "Eliminando script..."

  rm "$SCRIPT_PATH"
  print_success "Script eliminado"
}

# Función: Verificar que se eliminó correctamente
verify_removal() {
  if [[ -f "$SCRIPT_PATH" ]]; then
    print_error "No se pudo eliminar el script"
    exit 1
  fi

  if command -v "$SCRIPT_NAME" >/dev/null 2>&1; then
    print_warning "El comando '$SCRIPT_NAME' todavía está disponible"
    echo "Puede que tengas otra instalación en tu sistema"
  fi
}

# Función: Mostrar resumen de desinstalación
print_uninstall_summary() {
  echo
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  print_success "Desinstalación completada"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo
  echo "'$SCRIPT_NAME' ha sido eliminado del sistema."
  echo
}

# Función principal
main() {
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Desinstalador de vid2audio"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo

  check_script_exists
  confirm_uninstall
  remove_script
  verify_removal
  print_uninstall_summary
}

# Ejecutar desinstalación
main
