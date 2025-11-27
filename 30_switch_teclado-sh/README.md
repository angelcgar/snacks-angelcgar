# ⌨️ switch-keyboard

Script bash para alternar rápidamente entre distribuciones de teclado US y LATAM
en Linux.

## 🎯 Características

- ✅ Cambio automático entre teclados US ↔ LATAM
- ✅ Detección automática del layout actual
- ✅ Notificaciones de escritorio
- ✅ Instalación simple en `~/.local/bin/`
- ✅ Scripts de instalación/desinstalación incluidos

## 📋 Requisitos

- `setxkbmap` (generalmente viene con X11)
- `notify-send` (para notificaciones de escritorio)

### Instalación de requisitos

**Ubuntu/Debian:**

```bash
sudo apt-get install x11-xkb-utils libnotify-bin
```

**Arch Linux:**

```bash
sudo pacman -S xorg-setxkbmap libnotify
```

**Fedora:**

```bash
sudo dnf install xorg-x11-xkb-utils libnotify
```

## 📦 Instalación

```bash
cd 30_switch_teclado-sh
chmod +x install.sh
./install.sh
```

El script se instalará como `switch-keyboard` en `~/.local/bin/`

### Configurar PATH (si es necesario)

Si `~/.local/bin` no está en tu PATH:

**Fish shell:**

```fish
fish_add_path $HOME/.local/bin
```

**Bash/Zsh:**

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # o ~/.zshrc
source ~/.bashrc  # o ~/.zshrc
```

## 🚀 Uso

```bash
switch-keyboard
```

El script:

1. Detecta el layout actual (US o LATAM)
2. Cambia al layout opuesto
3. Muestra una notificación indicando el nuevo layout

### Atajo de teclado recomendado

Configura un atajo de teclado en tu entorno de escritorio para ejecutar:

```
switch-keyboard
```

**GNOME:**

1. Configuración → Teclado → Atajos personalizados
2. Nombre: "Cambiar teclado"
3. Comando: `switch-keyboard`
4. Atajo: Por ejemplo, `Super+Space`

**KDE Plasma:**

1. Configuración del sistema → Atajos
2. Agregar → Comando o URL
3. Comando: `switch-keyboard`

**XFCE:**

1. Configuración → Teclado → Atajos de aplicación
2. Agregar → `switch-keyboard`

## 🗑️ Desinstalación

```bash
cd 30_switch_teclado-sh
chmod +x uninstall.sh
./uninstall.sh
```

## 🧩 Estructura del proyecto

```
30_switch_teclado-sh/
├── app.sh          # Script principal
├── install.sh      # Script de instalación
├── uninstall.sh    # Script de desinstalación
└── README.md       # Este archivo
```

## 🔧 Cómo funciona

El script utiliza:

- `setxkbmap -query` para detectar el layout actual
- `setxkbmap us` o `setxkbmap latam` para cambiar el layout
- `notify-send` para mostrar notificaciones de escritorio

## 💡 Personalización

### Cambiar los layouts

Edita `app.sh` y modifica las líneas:

```bash
setxkbmap latam  # Cambia 'latam' por tu layout preferido
setxkbmap us     # Cambia 'us' por tu otro layout
```

Layouts comunes:

- `us` - Inglés estadounidense
- `latam` - Latinoamericano
- `es` - Español (España)
- `gb` - Inglés británico
- `de` - Alemán
- `fr` - Francés

### Personalizar el nombre del comando

Edita `install.sh` y cambia la variable:

```bash
SCRIPT_NAME="tu-nombre-preferido"
```

## 📝 Notas

- El script solo afecta la sesión actual de X11/Wayland
- El layout se restablecerá al valor por defecto al reiniciar
- Para cambios permanentes, configura tu layout en la configuración del sistema

## 🐛 Solución de problemas

**Error: setxkbmap: command not found**

```bash
sudo apt-get install x11-xkb-utils
```

**Error: notify-send: command not found**

```bash
sudo apt-get install libnotify-bin
```

**El script no cambia el teclado**

- Verifica que estás en una sesión X11 (no Wayland puro)
- Intenta ejecutar manualmente: `setxkbmap us`

**No aparecen notificaciones**

- Verifica que el servicio de notificaciones esté activo
- Prueba: `notify-send "Test" "Mensaje de prueba"`

## 📄 Licencia

Este proyecto es parte del repositorio `snacks` y sigue la misma licencia.

## 👤 Autor

angelcgar
