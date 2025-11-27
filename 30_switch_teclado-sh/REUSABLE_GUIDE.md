# 🔧 Guía de Reutilización de Scripts

Este documento explica cómo adaptar los scripts de instalación/desinstalación
para otros snacks.

## 📋 Variables configurables

Ambos scripts (`install.sh` y `uninstall.sh`) utilizan las mismas variables
principales:

```bash
# --- Variables de configuración --- #
SCRIPT_NAME="switch-keyboard"           # Nombre del ejecutable en .local/bin
SOURCE_FILE="app.sh"                    # Archivo fuente a instalar
INSTALL_DIR="$HOME/.local/bin"          # Directorio de instalación
REQUIRED_COMMANDS=("setxkbmap" "notify-send")  # Comandos requeridos
```

## 🎯 Cómo adaptar para otro snack

### Paso 1: Copiar los scripts

```bash
# Desde tu nuevo proyecto
cp ../30_switch_teclado-sh/install.sh .
cp ../30_switch_teclado-sh/uninstall.sh .
```

### Paso 2: Modificar variables en `install.sh`

```bash
# Ejemplo para un snack de backup
SCRIPT_NAME="backup-tool"               # Nombre del comando final
SOURCE_FILE="backup.sh"                 # Tu script principal
INSTALL_DIR="$HOME/.local/bin"          # Mantener igual
REQUIRED_COMMANDS=("rsync" "tar")       # Comandos que necesita tu script
```

### Paso 3: Modificar variables en `uninstall.sh`

```bash
# Solo necesitas cambiar estas dos:
SCRIPT_NAME="backup-tool"               # Mismo nombre que en install.sh
INSTALL_DIR="$HOME/.local/bin"          # Mantener igual
```

### Paso 4: Hacer ejecutables

```bash
chmod +x install.sh uninstall.sh
```

## 📝 Ejemplos de configuración

### Ejemplo 1: Script de Python

```bash
# install.sh
SCRIPT_NAME="my-python-tool"
SOURCE_FILE="main.py"
INSTALL_DIR="$HOME/.local/bin"
REQUIRED_COMMANDS=("python3")
```

### Ejemplo 2: Script sin dependencias

```bash
# install.sh
SCRIPT_NAME="simple-script"
SOURCE_FILE="script.sh"
INSTALL_DIR="$HOME/.local/bin"
REQUIRED_COMMANDS=()  # Array vacío, sin dependencias
```

### Ejemplo 3: Múltiples dependencias

```bash
# install.sh
SCRIPT_NAME="media-converter"
SOURCE_FILE="convert.sh"
INSTALL_DIR="$HOME/.local/bin"
REQUIRED_COMMANDS=("ffmpeg" "imagemagick" "jq")
```

### Ejemplo 4: Instalación en /usr/local/bin

```bash
# install.sh (requiere sudo)
SCRIPT_NAME="system-tool"
SOURCE_FILE="tool.sh"
INSTALL_DIR="/usr/local/bin"  # Instalación del sistema
REQUIRED_COMMANDS=("systemctl")

# Nota: Modificar la función install_script para usar sudo
install_script() {
    local dest_path="$INSTALL_DIR/$SCRIPT_NAME"
    sudo cp "$SOURCE_FILE" "$dest_path"
    # ... resto del código
}
```

## 🧩 Funciones reutilizables

Todas estas funciones se pueden usar tal cual en otros proyectos:

### Funciones de output

```bash
print_success()   # ✅ Mensaje verde
print_error()     # ❌ Mensaje rojo
print_warning()   # ⚠️  Mensaje amarillo
print_info()      # ℹ️  Mensaje azul
print_header()    # Encabezado del script
```

### Funciones de validación

```bash
check_source_file()        # Verifica que el archivo fuente existe
check_required_commands()  # Verifica dependencias
check_path_configuration() # Verifica PATH
```

### Funciones de instalación

```bash
create_install_directory()    # Crea ~/.local/bin si no existe
install_script()              # Copia el script
set_executable_permissions()  # chmod +x
```

### Funciones de desinstalación

```bash
check_script_exists()  # Verifica si está instalado
confirm_uninstall()    # Solicita confirmación
remove_script()        # Elimina el archivo
verify_removal()       # Verifica la eliminación
```

## 🎨 Personalización de colores

Si quieres cambiar los colores:

```bash
# En ambos scripts, modifica estas variables:
RED='\033[0;31m'      # Rojo
GREEN='\033[0;32m'    # Verde
YELLOW='\033[1;33m'   # Amarillo
BLUE='\033[0;34m'     # Azul
NC='\033[0m'          # Sin color

# Otros colores disponibles:
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
```

## 📦 Plantilla completa

### Para install.sh

```bash
#!/bin/bash

# --- Variables de configuración --- #
SCRIPT_NAME="mi-comando"              # CAMBIAR: nombre del comando
SOURCE_FILE="mi-script.sh"            # CAMBIAR: archivo fuente
INSTALL_DIR="$HOME/.local/bin"        # Mantener o cambiar
REQUIRED_COMMANDS=("cmd1" "cmd2")     # CAMBIAR: dependencias

# --- El resto del código se mantiene igual --- #
# Copiar las funciones de 30_switch_teclado-sh/install.sh
```

### Para uninstall.sh

```bash
#!/bin/bash

# --- Variables de configuración --- #
SCRIPT_NAME="mi-comando"              # CAMBIAR: mismo que install.sh
INSTALL_DIR="$HOME/.local/bin"        # Mantener o cambiar

# --- El resto del código se mantiene igual --- #
# Copiar las funciones de 30_switch_teclado-sh/uninstall.sh
```

## 🔄 Workflow típico

1. **Crear tu snack:**

   ```bash
   mkdir 31_mi-snack-sh
   cd 31_mi-snack-sh
   ```

2. **Crear tu script principal:**

   ```bash
   touch mi-script.sh
   chmod +x mi-script.sh
   # ... escribir código ...
   ```

3. **Copiar scripts de instalación:**

   ```bash
   cp ../30_switch_teclado-sh/install.sh .
   cp ../30_switch_teclado-sh/uninstall.sh .
   chmod +x install.sh uninstall.sh
   ```

4. **Adaptar variables:**

   - Editar `SCRIPT_NAME` en ambos archivos
   - Editar `SOURCE_FILE` en install.sh
   - Editar `REQUIRED_COMMANDS` en install.sh

5. **Probar:**
   ```bash
   ./install.sh
   mi-comando --help
   ./uninstall.sh
   ```

## ⚙️ Variaciones avanzadas

### Instalación de múltiples archivos

```bash
# En install.sh, modificar install_script():
install_script() {
    local files=("script1.sh" "script2.sh" "helper.sh")

    for file in "${files[@]}"; do
        cp "$file" "$INSTALL_DIR/"
        chmod +x "$INSTALL_DIR/$file"
        print_success "Instalado: $file"
    done
}
```

### Crear archivo de configuración

```bash
# Agregar al final de install_script():
create_config_file() {
    local config_dir="$HOME/.config/mi-app"
    mkdir -p "$config_dir"

    if [[ ! -f "$config_dir/config.ini" ]]; then
        cat > "$config_dir/config.ini" <<EOF
[settings]
option1=value1
option2=value2
EOF
        print_success "Archivo de configuración creado"
    fi
}
```

### Instalación interactiva

```bash
# Antes de install_script():
ask_installation_location() {
    print_info "¿Dónde deseas instalar el script?"
    echo "1) ~/.local/bin (usuario actual)"
    echo "2) /usr/local/bin (todos los usuarios, requiere sudo)"
    read -p "Selección (1-2): " choice

    case $choice in
        1) INSTALL_DIR="$HOME/.local/bin" ;;
        2) INSTALL_DIR="/usr/local/bin" ;;
        *) print_error "Opción inválida"; exit 1 ;;
    esac
}
```

## 🎯 Checklist de adaptación

- [ ] Cambiar `SCRIPT_NAME` en install.sh
- [ ] Cambiar `SCRIPT_NAME` en uninstall.sh
- [ ] Cambiar `SOURCE_FILE` en install.sh
- [ ] Actualizar `REQUIRED_COMMANDS` en install.sh
- [ ] Verificar que `INSTALL_DIR` es correcto
- [ ] Hacer ejecutables: `chmod +x install.sh uninstall.sh`
- [ ] Probar instalación: `./install.sh`
- [ ] Verificar comando: `which SCRIPT_NAME`
- [ ] Probar desinstalación: `./uninstall.sh`
- [ ] Actualizar README.md con información específica

## 📚 Recursos adicionales

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Linux Filesystem Hierarchy](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

---

**Nota:** Estos scripts siguen el principio de responsabilidad única (SRP). Cada
función tiene un propósito específico y bien definido, facilitando el
mantenimiento y reutilización.
