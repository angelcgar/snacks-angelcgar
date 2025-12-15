#!/bin/bash

# =============================================================================
# Script de desinstalación para yv (Video Project Manager)
# =============================================================================
# Elimina el script de gestión de proyectos de video de ~/.local/bin/
# Variables configurables para reutilizar en otros snacks
# =============================================================================

# --- Variables de configuración --- #
SCRIPT_NAME="yv"                        # Nombre del ejecutable en .local/bin
INSTALL_DIR="$HOME/.local/bin"          # Directorio de instalación

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
    echo -e "${BLUE}   Desinstalador de YV${NC}"
    echo -e "${BLUE}   (Video Project Manager)${NC}"
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

check_script_exists() {
    # Verifica si el script está instalado
    local script_path="$INSTALL_DIR/$SCRIPT_NAME"

    if [[ ! -f "$script_path" ]]; then
        print_warning "El script '$SCRIPT_NAME' no está instalado en $INSTALL_DIR"
        print_info "No hay nada que desinstalar"
        exit 0
    fi

    print_info "Script encontrado: $script_path"
}

confirm_uninstall() {
    # Solicita confirmación del usuario
    echo ""
    print_warning "¿Estás seguro de que deseas desinstalar '$SCRIPT_NAME'?"
    read -p "Escribe 'si' para confirmar: " confirmation

    if [[ "$confirmation" != "si" ]]; then
        print_info "Desinstalación cancelada"
        exit 0
    fi

    echo ""
}

remove_script() {
    # Elimina el script del directorio de instalación
    local script_path="$INSTALL_DIR/$SCRIPT_NAME"

    rm -f "$script_path"

    if [[ $? -ne 0 ]]; then
        print_error "Error al eliminar el script"
        exit 1
    fi

    print_success "Script eliminado: $script_path"
}

verify_removal() {
    # Verifica que el script se haya eliminado correctamente
    local script_path="$INSTALL_DIR/$SCRIPT_NAME"

    if [[ -f "$script_path" ]]; then
        print_error "El script no se pudo eliminar completamente"
        exit 1
    fi

    print_success "Verificación exitosa: el script ya no existe"
}

print_uninstall_summary() {
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}   ✅ Desinstalación completada${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    print_info "El script '$SCRIPT_NAME' ha sido eliminado"
    print_info "Directorio: $INSTALL_DIR"
    echo ""
    print_info "Nota: Los proyectos creados con YV no se han eliminado"
    print_info "Puedes eliminarlos manualmente si lo deseas"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

main() {
    print_header

    # Verificar existencia
    check_script_exists

    # Solicitar confirmación
    confirm_uninstall

    # Proceso de desinstalación
    remove_script
    verify_removal

    # Resumen
    print_uninstall_summary
}

# Ejecutar script
main
