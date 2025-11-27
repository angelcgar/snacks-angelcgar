#!/bin/bash

# =============================================================================
# Script de instalación para switch-keyboard
# =============================================================================
# Instala el script de cambio de teclado en ~/.local/bin/
# Variables configurables para reutilizar en otros snacks
# =============================================================================

# --- Variables de configuración --- #
SCRIPT_NAME="switch-keyboard"           # Nombre del ejecutable en .local/bin
SOURCE_FILE="app.sh"                    # Archivo fuente a instalar
INSTALL_DIR="$HOME/.local/bin"          # Directorio de instalación
REQUIRED_COMMANDS=("setxkbmap" "notify-send")  # Comandos requeridos

# --- Colores para output --- #
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Funciones
# =============================================================================

print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}   Instalador de ${SCRIPT_NAME}${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_source_file() {
    # Verifica que el archivo fuente existe
    if [[ ! -f "$SOURCE_FILE" ]]; then
        print_error "No se encuentra el archivo '$SOURCE_FILE'"
        exit 1
    fi
    print_success "Archivo fuente encontrado: $SOURCE_FILE"
}

check_required_commands() {
    # Verifica que los comandos requeridos estén instalados
    local missing_commands=()

    for cmd in "${REQUIRED_COMMANDS[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing_commands+=("$cmd")
        fi
    done

    if [[ ${#missing_commands[@]} -gt 0 ]]; then
        print_error "Faltan comandos requeridos: ${missing_commands[*]}"
        print_info "Instala los comandos faltantes antes de continuar"

        # Sugerencias de instalación
        if [[ " ${missing_commands[*]} " =~ " setxkbmap " ]]; then
            print_info "Ubuntu/Debian: sudo apt-get install x11-xkb-utils"
        fi
        if [[ " ${missing_commands[*]} " =~ " notify-send " ]]; then
            print_info "Ubuntu/Debian: sudo apt-get install libnotify-bin"
        fi

        exit 1
    fi

    print_success "Todos los comandos requeridos están instalados"
}

create_install_directory() {
    # Crea el directorio de instalación si no existe
    if [[ ! -d "$INSTALL_DIR" ]]; then
        mkdir -p "$INSTALL_DIR"
        print_success "Directorio creado: $INSTALL_DIR"
    else
        print_info "Directorio ya existe: $INSTALL_DIR"
    fi
}

check_path_configuration() {
    # Verifica si ~/.local/bin está en PATH
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        print_warning "$INSTALL_DIR no está en tu PATH"
        echo ""
        print_info "Agrega esto a tu archivo de configuración de shell:"
        echo ""
        echo "  # Para Bash (~/.bashrc):"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "  # Para Fish (~/.config/fish/config.fish):"
        echo "  fish_add_path \$HOME/.local/bin"
        echo ""
        echo "  # Para Zsh (~/.zshrc):"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
    else
        print_success "$INSTALL_DIR está en PATH"
    fi
}

install_script() {
    # Copia el script al directorio de instalación
    local dest_path="$INSTALL_DIR/$SCRIPT_NAME"

    cp "$SOURCE_FILE" "$dest_path"

    if [[ $? -ne 0 ]]; then
        print_error "Error al copiar el script"
        exit 1
    fi

    print_success "Script copiado a: $dest_path"
}

set_executable_permissions() {
    # Hace el script ejecutable
    local dest_path="$INSTALL_DIR/$SCRIPT_NAME"

    chmod +x "$dest_path"

    if [[ $? -ne 0 ]]; then
        print_error "Error al establecer permisos de ejecución"
        exit 1
    fi

    print_success "Permisos de ejecución establecidos"
}

print_installation_summary() {
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}   ✅ Instalación completada${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    print_info "Script instalado como: $SCRIPT_NAME"
    print_info "Ubicación: $INSTALL_DIR/$SCRIPT_NAME"
    echo ""
    print_info "Uso:"
    echo "  $SCRIPT_NAME"
    echo ""
    print_info "El script cambiará automáticamente entre teclados US y LATAM"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

main() {
    print_header

    # Verificaciones previas
    check_source_file
    check_required_commands

    echo ""

    # Proceso de instalación
    create_install_directory
    check_path_configuration

    echo ""

    install_script
    set_executable_permissions

    # Resumen
    print_installation_summary
}

# Ejecutar script
main
