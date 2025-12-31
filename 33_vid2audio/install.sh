#!/usr/bin/env bash

# Script de instalación para vid2audio
# Instala el comando en ~/.local/bin/ para uso global en el sistema

set -euo pipefail

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

# Configuración
SCRIPT_NAME="vid2audio"
SOURCE_FILE="vid2audio.sh"
INSTALL_DIR="$HOME/.local/bin"
REQUIRED_COMMANDS=("ffmpeg")

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

# Función: Verificar que el archivo fuente existe
check_source_file() {
  print_info "Verificando archivo fuente..."

  if [[ ! -f "$SOURCE_FILE" ]]; then
    print_error "No se encontró el archivo '$SOURCE_FILE'"
    echo "Asegúrate de ejecutar este script desde el directorio que contiene '$SOURCE_FILE'"
    exit 1
  fi

  print_success "Archivo fuente encontrado"
}

# Función: Crear directorio de instalación si no existe
create_install_directory() {
  print_info "Verificando directorio de instalación..."

  if [[ ! -d "$INSTALL_DIR" ]]; then
    print_warning "El directorio '$INSTALL_DIR' no existe. Creándolo..."
    mkdir -p "$INSTALL_DIR"
    print_success "Directorio creado"
  else
    print_success "Directorio de instalación existe"
  fi
}

# Función: Verificar que el directorio está en el PATH
check_path_configuration() {
  print_info "Verificando configuración de PATH..."

  if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    print_warning "El directorio '$INSTALL_DIR' no está en tu PATH"
    echo
    echo "Agrega la siguiente línea a tu archivo de configuración de shell:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo
    echo "Para Fish shell (~/.config/fish/config.fish):"
    echo "  set -gx PATH \$HOME/.local/bin \$PATH"
    echo
  else
    print_success "PATH configurado correctamente"
  fi
}

# Función: Verificar dependencias requeridas
check_dependencies() {
  print_info "Verificando dependencias..."

  local missing_deps=()

  for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      missing_deps+=("$cmd")
    fi
  done

  if [[ ${#missing_deps[@]} -gt 0 ]]; then
    print_error "Faltan las siguientes dependencias:"
    for dep in "${missing_deps[@]}"; do
      echo "  - $dep"
    done
    echo
    echo "Instala ffmpeg:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Fedora: sudo dnf install ffmpeg"
    echo "  Arch: sudo pacman -S ffmpeg"
    echo "  macOS: brew install ffmpeg"
    exit 1
  fi

  print_success "Todas las dependencias están instaladas"
}

# Función: Copiar el script al directorio de instalación
install_script() {
  print_info "Instalando script..."

  local target_path="$INSTALL_DIR/$SCRIPT_NAME"

  # Si ya existe, preguntar si desea sobrescribir
  if [[ -f "$target_path" ]]; then
    print_warning "Ya existe una instalación de '$SCRIPT_NAME'"
    read -p "¿Deseas sobrescribir? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
      echo "Instalación cancelada."
      exit 0
    fi
  fi

  cp "$SOURCE_FILE" "$target_path"
  print_success "Script copiado a '$target_path'"
}

# Función: Dar permisos de ejecución
set_executable_permissions() {
  print_info "Configurando permisos..."

  local target_path="$INSTALL_DIR/$SCRIPT_NAME"
  chmod +x "$target_path"

  print_success "Permisos de ejecución configurados"
}

# Función: Mostrar resumen de instalación
print_installation_summary() {
  echo
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  print_success "Instalación completada"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo
  echo -e "Script instalado como: ${GREEN}$SCRIPT_NAME${NC}"
  echo "Ubicación: $INSTALL_DIR/$SCRIPT_NAME"
  echo
  echo "Uso:"
  echo "  $SCRIPT_NAME <video.mp4> [salida.mp3]"
  echo "  $SCRIPT_NAME --help"
  echo
}

# Función principal
main() {
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Instalador de vid2audio"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo

  check_source_file
  check_dependencies
  create_install_directory
  check_path_configuration
  install_script
  set_executable_permissions
  print_installation_summary
}

# Ejecutar instalación
main
