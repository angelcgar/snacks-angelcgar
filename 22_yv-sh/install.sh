#!/bin/bash

# =============================================================================
# Script de instalación para yv (Video Project Manager)
# =============================================================================
# Instala el script de gestión de proyectos de video en ~/.local/bin/
# Variables configurables para reutilizar en otros snacks
# =============================================================================

# --- Variables de configuración --- #
SCRIPT_NAME="yv"                        # Nombre del ejecutable en .local/bin
SOURCE_FILE="yv.sh"                     # Archivo fuente a instalar
INSTALL_DIR="$HOME/.local/bin"          # Directorio de instalación
REQUIRED_COMMANDS=()                    # Sin dependencias requeridas

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
    echo -e "${BLUE}   📹 Instalador de YV${NC}"
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

check_source_file() {
    # Verifica que el archivo fuente existe
    if [[ ! -f "$SOURCE_FILE" ]]; then
        print_error "No se encuentra el archivo '$SOURCE_FILE'"
        exit 1
    fi
    print_success "Archivo fuente encontrado: $SOURCE_FILE"
}

check_assets_directory() {
    # Verifica si existe el directorio de assets (opcional pero recomendado)
    local assets_dir="$HOME/Documentos/assets"

    if [[ ! -d "$assets_dir" ]]; then
        print_warning "No se encuentra el directorio ~/Documentos/assets/"
        print_info "Los proyectos se crearán sin archivos de muestra"
        print_info "Para agregar archivos de muestra, consulta el Drive"
        echo ""
    else
        # Verificar archivos específicos
        local has_samples=false

        if [[ -f "$assets_dir/raw_atardecer_montana_arbol_piedra.mp4" ]]; then
            print_success "Video de muestra encontrado"
            has_samples=true
        fi

        if [[ -f "$assets_dir/raw_fondo_atardecer_mujer_volando.jpg" ]]; then
            print_success "Imagen de muestra encontrada"
            has_samples=true
        fi

        if [[ "$has_samples" = false ]]; then
            print_warning "Directorio assets existe pero no contiene archivos de muestra"
        fi
    fi
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
    echo "  yv new 'Nombre del Proyecto'"
    echo "  yv help"
    echo ""
    print_info "Crea proyectos de video con estructura profesional"
    print_info "Incluye plantillas de seguimiento y archivos de muestra"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

main() {
    print_header

    # Verificaciones previas
    check_source_file
    check_assets_directory

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
