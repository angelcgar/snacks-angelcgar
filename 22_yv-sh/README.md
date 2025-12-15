# 📹 YV - Video Project Manager

Gestor de proyectos de video que crea automáticamente una estructura profesional de directorios, plantillas de seguimiento y archivos de muestra para tus proyectos audiovisuales.

## 🎯 Características

- ✅ Estructura de directorios organizada profesionalmente
- ✅ Plantilla de seguimiento de proyecto (video_tracker.md)
- ✅ Archivos de muestra automáticos desde ~/Documentos/assets/
- ✅ Soporte para proyectos Kdenlive
- ✅ README.md generado automáticamente
- ✅ Organización por fases: raw → edit → export → resources

## 📋 Requisitos

- Bash
- (Opcional) `tree` para visualización mejorada de estructura
- (Opcional) Directorio `~/Documentos/assets/` con archivos de muestra

## 📦 Instalación

```bash
cd 22_yv-sh
./install.sh
```

El script se instalará como `yv` en `~/.local/bin/`

### Configurar archivos de muestra (opcional)

Para que YV copie automáticamente archivos de muestra a tus proyectos:

1. Crea el directorio de assets:
   ```bash
   mkdir -p ~/Documentos/assets
   ```

2. Coloca los siguientes archivos en ese directorio:
   - `raw_atardecer_montana_arbol_piedra.mp4` - Video de muestra
   - `raw_fondo_atardecer_mujer_volando.jpg` - Imagen de muestra

3. Los nuevos proyectos incluirán estos archivos automáticamente

**Nota:** Si no existe el directorio assets, YV funcionará normalmente pero sin archivos de muestra.

## 🚀 Uso

### Crear un nuevo proyecto

```bash
yv new "Nombre del Proyecto"
```

### Ver ayuda

```bash
yv help
```

## 📁 Estructura generada

Cuando creas un proyecto, YV genera la siguiente estructura:

```
NombreDelProyecto/
├── 01_raw_audio/                          # Audio sin procesar
├── 01_raw_video/                          # Video sin procesar
│   └── raw_atardecer_montana_arbol_piedra.mp4  # (si existe en assets)
├── 02_edit_project/                       # Proyectos de edición
│   └── NombreDelProyecto.kdenlive        # Archivo de proyecto Kdenlive
├── 02_exports/                            # Videos finales exportados
├── 03_resources/                          # Recursos multimedia
│   ├── music/                            # Música y audio
│   ├── images/                           # Imágenes
│   └── graphics/                         # Gráficos y elementos visuales
│       └── raw_fondo_atardecer_mujer_volando.jpg  # (si existe en assets)
├── 04_script/                            # Guiones y notas
│   └── notes_NombreDelProyecto.txt      # Notas del proyecto
├── video_tracker.md                      # Plantilla de seguimiento completa
└── README.md                             # Información del proyecto
```

## 📝 Plantilla de seguimiento (video_tracker.md)

Cada proyecto incluye una plantilla completa con secciones para:

1. **Objetivo del Video** - Tema, objetivo y audiencia
2. **Investigación y Planeación** - Referencias y estructura
3. **Guion** - Introducción, desarrollo y conclusión
4. **Recursos y Materiales** - Equipo y software
5. **Cronograma** - Fases y fechas
6. **Grabación** - Lista de tomas y notas
7. **Edición** - Tareas y software
8. **Miniatura y Título** - Diseño y brainstorming
9. **Publicación** - Descripción, etiquetas y plataforma
10. **Promoción** - Redes sociales y colaboraciones
11. **Postproducción y Revisión** - Métricas y mejoras
12. **Checklist Final** - Verificación de tareas

## 💡 Ejemplos de uso

### Crear proyecto de tutorial
```bash
yv new "Tutorial Python Básico"
```

### Crear proyecto de vlog
```bash
yv new "Vlog Viaje a Madrid"
```

### Crear proyecto con nombre simple
```bash
yv new Review_Camara_2025
```

## 🔧 Workflow recomendado

1. **Crear proyecto:**
   ```bash
   yv new "Mi Video"
   cd Mi_Video
   ```

2. **Importar archivos:**
   - Coloca videos originales en `01_raw_video/`
   - Coloca audio original en `01_raw_audio/`
   - Coloca música en `03_resources/music/`
   - Coloca imágenes en `03_resources/images/`

3. **Planificar:**
   - Edita `video_tracker.md` con los detalles del proyecto
   - Escribe notas en `04_script/notes_*.txt`

4. **Editar:**
   - Abre el proyecto Kdenlive desde `02_edit_project/`
   - Exporta versiones a `02_exports/`

5. **Publicar:**
   - Sigue el checklist en `video_tracker.md`

## 🗑️ Desinstalación

```bash
cd 22_yv-sh
./uninstall.sh
```

**Nota:** La desinstalación solo elimina el comando `yv`. Los proyectos creados NO se eliminan automáticamente.

## ⚙️ Configuración avanzada

### Cambiar directorio de instalación

Edita `install.sh` y modifica:
```bash
INSTALL_DIR="/ruta/personalizada"
```

### Agregar más archivos de muestra

Edita `yv.sh` en la sección de copia de archivos y agrega:
```bash
if [ -f "$assets_dir/tu_archivo.ext" ]; then
  cp "$assets_dir/tu_archivo.ext" "directorio_destino/"
  echo "✅ Tu archivo copiado"
fi
```

## 🐛 Solución de problemas

**Error: No se encuentra el archivo 'yv.sh'**
- Asegúrate de ejecutar `./install.sh` desde el directorio `22_yv-sh`

**Advertencia: No se encuentra ~/Documentos/assets/**
- Es normal si no has creado el directorio de assets
- Los proyectos se crearán sin archivos de muestra
- Crea el directorio y agrega archivos para usarlos en futuros proyectos

**El comando 'yv' no se encuentra**
- Verifica que `~/.local/bin` esté en tu PATH
- Ejecuta: `echo $PATH | grep ".local/bin"`
- Si no aparece, agrega a tu configuración de shell:
  ```bash
  # Fish
  fish_add_path $HOME/.local/bin

  # Bash/Zsh
  export PATH="$HOME/.local/bin:$PATH"
  ```

## 📖 Documentación adicional

- `video_tracker.md` - Plantilla generada en cada proyecto con guía completa
- `install.sh` - Script de instalación con variables reutilizables
- `uninstall.sh` - Script de desinstalación segura

## 🎨 Personalización

### Modificar estructura de directorios

Edita el array `dirs` en `yv.sh`:
```bash
declare -a dirs=(
  "01_raw_audio"
  "01_raw_video"
  "tu_directorio_personalizado"
  # ...
)
```

### Cambiar plantilla de seguimiento

Edita la variable `VIDEO_TRACKER_TEMPLATE` en `yv.sh` para personalizar las secciones y contenido.

## 📄 Licencia

Este proyecto es parte del repositorio `snacks` y sigue la misma licencia.

## 👤 Autor

angelcgar

---

**Tip:** Combina YV con otros snacks como `today` para documentar el progreso diario de tus proyectos de video. 🎬
