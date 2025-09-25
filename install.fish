#!/usr/bin/fish

# --- Configuración ---
set -l SCRIPT_NAME "mi_script.fish"
set -l INSTALL_DIR "$HOME/.local/bin"
set -l ALIAS_NAME miscript # Cambia esto si quieres otro alias

# --- Verificar si el script existe ---
if not test -f "$SCRIPT_NAME"
    echo "❌ Error: El archivo '$SCRIPT_NAME' no existe en el directorio actual."
    exit 1
end

# --- Crear directorio de instalación si no existe ---
if not test -d "$INSTALL_DIR"
    echo "📂 Creando directorio de instalación: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
end

# --- Copiar el script ---
echo "🚀 Instalando '$SCRIPT_NAME' en $INSTALL_DIR..."
cp "$SCRIPT_NAME" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# --- Agregar al PATH (si no está ya) ---
if not contains "$INSTALL_DIR" $PATH
    echo "🔧 Agregando $INSTALL_DIR al PATH en ~/.config/fish/config.fish"
    set -Ua fish_user_paths "$INSTALL_DIR"
    echo "✅ PATH actualizado. Reinicia la terminal o ejecuta 'source ~/.config/fish/config.fish'."
end

# --- Crear alias (opcional) ---
echo "🤔 ¿Quieres crear un alias llamado '$ALIAS_NAME' para ejecutarlo fácilmente? (s/n)"
read -P "> " respuesta
if string match -qi "s*" "$respuesta"
    echo "alias $ALIAS_NAME='$SCRIPT_NAME'" >>~/.config/fish/config.fish
    echo "✨ Alias creado. Ejecuta '$ALIAS_NAME' en cualquier lugar."
    echo "⚠️ Reinicia la terminal o usa 'source ~/.config/fish/config.fish' para aplicar cambios."
end

# --- Mensaje final ---
echo ""
echo "🎉 ¡Instalación completada!"
echo "📌 Ejecuta el script con: $SCRIPT_NAME"
if string match -qi "s*" "$respuesta"
    echo "📌 O usa el alias: $ALIAS_NAME"
end
