#!/bin/bash

# =============================
# YV - Gestor de Proyectos de Video
# =============================
# Script para crear estructura de proyectos de video con plantillas
# y archivos de muestra automáticamente.
# =============================

# =============================
# 📹 Plantilla de Seguimiento
# =============================
# Esta plantilla se genera como video_tracker.md en cada proyecto
# Contiene secciones para documentar todo el proceso de creación del video
VIDEO_TRACKER_TEMPLATE='
# 📹 **Plantilla de Seguimiento: {{NOMBRE_PROYECTO}}**

`Creado: {{FECHA}}`
`Última actualización: {{FECHA}}`

## 1. **Objetivo del Video**

- **Tema principal**: Describe brevemente de qué trata el video.
- **Objetivo**: ¿Qué quieres lograr con este video? (informar, entretener, educar, etc.)
- **Audiencia**: ¿A quién va dirigido este video? (grupo demográfico, intereses específicos, etc.)

---

## 2. **Investigación y Planeación**

- **Investigación**:
  - Recursos y referencias sobre el tema.
  - Fuentes de información para datos, estadísticas, etc.
- **Estructura del video**:
  - Introducción
  - Desarrollo
  - Conclusión
- **Duración aproximada**: X minutos.

---

## 3. **Guion**

- **Formato**: (Escribe un guion detallado o puntos clave para improvisar)
  - **Introducción**:
    - [ ] Gancho para captar la atención.
    - [ ] Presentación.
  - **Desarrollo**:
    - [ ] Punto 1
    - [ ] Punto 2
    - [ ] Etc.
  - **Conclusión**:
    - [ ] Resumen de los puntos principales.
    - [ ] Llamada a la acción (CTA).

---

## 4. **Recursos y Materiales**

- **Equipo de grabación**:
  - Cámaras
  - Micrófonos
  - Iluminación
  - Trípodes
- **Software de edición**:
  - Ejemplo: Adobe Premiere, DaVinci Resolve, etc.
- **Música**:
  - Canciones de fondo (considerar licencias libres de derechos)
- **Gráficos y efectos**:
  - Animaciones
  - Subtítulos

---

## 5. **Cronograma**

| Fase                  | Fecha de inicio | Fecha de entrega | Responsable |
| --------------------- | --------------- | ---------------- | ----------- |
| Investigación y Guion | DD/MM/YYYY      | DD/MM/YYYY       | Nombre      |
| Grabación             | DD/MM/YYYY      | DD/MM/YYYY       | Nombre      |
| Edición               | DD/MM/YYYY      | DD/MM/YYYY       | Nombre      |
| Revisión              | DD/MM/YYYY      | DD/MM/YYYY       | Nombre      |
| Publicación           | DD/MM/YYYY      | DD/MM/YYYY       | Nombre      |

---

## 6. **Grabación**

- **Fecha de grabación**: DD/MM/YYYY
- **Ubicación**: Lugar o entorno.
- **Lista de tomas**:
  - [ ] Toma 1: Descripción.
  - [ ] Toma 2: Descripción.
  - [ ] B-roll necesario: (tomas adicionales, paisajes, etc.)
- **Notas**:
  - Aspectos técnicos (iluminación, encuadres, etc.)
  - Consejos de actuación.

---

## 7. **Edición**

- **Software**: Indicar el software de edición a utilizar.
- **Tareas**:
  - [ ] Selección de tomas.
  - [ ] Corte de video.
  - [ ] Inserción de música y efectos de sonido.
  - [ ] Transiciones.
  - [ ] Corrección de color.
  - [ ] Subtítulos (si es necesario).
  - [ ] Exportar video en formato adecuado (ej: MP4, 1080p).

---

## 8. **Miniatura y Título**

- **Título del video**: Brainstorming de ideas de título llamativo.
- **Miniatura**:
  - [ ] Diseño de miniatura.
  - [ ] Texto en miniatura.
  - [ ] Estilo visual (colores, tipografía).
  - **Software**: Canva, Photoshop, etc.

---

## 9. **Publicación**

- **Plataforma**: YouTube.
- **Fecha de publicación**: DD/MM/YYYY.
- **Descripción del video**:
  - [ ] Resumen del contenido.
  - [ ] Enlaces y recursos mencionados.
  - [ ] Tiempos (timestamps).
- **Etiquetas**: (palabras clave para mejorar el SEO).
- **Lista de reproducción**: Añadir a las listas correspondientes.
- **Monetización**: Activar si es posible.

---

## 10. **Promoción**

- **Redes sociales**:
  - [ ] Publicación en Instagram, Twitter, Facebook, etc.
- **Colaboraciones**:
  - Menciones o colaboraciones con otros creadores.
- **Publicidad**:
  - [ ] Google Ads, si aplica.

---

## 11. **Postproducción y Revisión**

- **Análisis de métricas**:
  - Visualizaciones.
  - Tiempo de retención.
  - Comentarios y feedback.
- **Mejoras para futuros videos**:
  - Reflexión sobre lo que salió bien y lo que se puede mejorar.

---

## 12. **Checklist Final**

- [ ] Guion finalizado.
- [ ] Grabación completa.
- [ ] Edición terminada.
- [ ] Miniatura creada.
- [ ] Descripción y etiquetas listas.
- [ ] Video publicado.
- [ ] Promoción en redes sociales.
'

# =============================
# Funciones
# =============================

create_project() {
  local project_name="$1"

  # Convertir nombre del proyecto a formato seguro para sistema de archivos
  # - Reemplaza espacios con guiones bajos
  # - Elimina caracteres no alfanuméricos excepto guiones bajos
  local safe_name
  safe_name=$(echo "$project_name" | tr ' ' '_' | tr -cd '[:alnum:]_')

  echo "Creando proyecto: $project_name"
  mkdir -p "$safe_name" || {
    echo "Error al crear directorio"
    exit 1
  }
  cd "$safe_name" || exit 1

  # Estructura de directorios
  declare -a dirs=(
    "01_raw_audio"
    "01_raw_video"
    "02_edit_project"
    "02_exports"
    "03_resources/music"
    "03_resources/images"
    "03_resources/graphics"
    "04_script"
  )

  for dir in "${dirs[@]}"; do
    mkdir -p "$dir"
  done

  # Crear archivo de proyecto Kdenlive vacío
  touch "02_edit_project/${safe_name}.kdenlive"

  # Crear archivo de notas en el directorio de script
  echo "# Notas del proyecto" > "04_script/notes_${safe_name}.txt"

  # Generar video_tracker.md desde la variable global
  echo "$VIDEO_TRACKER_TEMPLATE" \
    | sed "s/{{FECHA}}/$(date '+%Y-%m-%d')/g" \
    | sed "s/{{NOMBRE_PROYECTO}}/$safe_name/g" \
    > "video_tracker.md"

  # README.md básico con información del proyecto
  echo "# $project_name" > "README.md"
  echo "- Fecha: $(date '+%Y-%m-%d')" >> "README.md"
  echo "- Estado: En curso" >> "README.md"

  # Copiar archivos de muestra desde ~/Documentos/assets/
  local assets_dir="$HOME/Documentos/assets"

  if [ ! -d "$assets_dir" ]; then
    echo "⚠️  ADVERTENCIA: No se encuentra el directorio ~/Documentos/assets/"
    echo "   Ver el Drive para solucionar este problema."
    echo "   El proyecto se creó, pero sin archivos de muestra."
  else
    # Copiar video de muestra si existe
    if [ -f "$assets_dir/raw_atardecer_montana_arbol_piedra.mp4" ]; then
      cp "$assets_dir/raw_atardecer_montana_arbol_piedra.mp4" "01_raw_video/"
      echo "✅ Video de muestra copiado a 01_raw_video/"
    fi

    # Copiar imagen de muestra si existe
    if [ -f "$assets_dir/raw_fondo_atardecer_mujer_volando.jpg" ]; then
      cp "$assets_dir/raw_fondo_atardecer_mujer_volando.jpg" "03_resources/graphics/"
      echo "✅ Imagen de muestra copiada a 03_resources/graphics/"
    fi
  fi

  echo ""
  echo "✅ Proyecto creado en: $(pwd)"
  echo ""
  echo "📁 Estructura del proyecto:"

  # Mostrar estructura con tree si está disponible, si no usar find
  if command -v tree >/dev/null; then
    tree -L 3
  else
    find . -maxdepth 3 -type d | sort
  fi
}

show_help() {
  echo "📹 YV - Gestor de Proyectos de Video"
  echo ""
  echo "Uso:"
  echo "  yv new <nombre-proyecto>    Crea un nuevo proyecto de video"
  echo "  yv help                     Muestra esta ayuda"
  echo ""
  echo "Descripción:"
  echo "  Crea una estructura completa de directorios para proyectos de video,"
  echo "  incluyendo plantillas de seguimiento y archivos de muestra."
  echo ""
  echo "Estructura generada:"
  echo "  01_raw_audio/          - Audio sin procesar"
  echo "  01_raw_video/          - Video sin procesar (con archivo de muestra)"
  echo "  02_edit_project/       - Proyecto de edición (Kdenlive)"
  echo "  02_exports/            - Videos exportados"
  echo "  03_resources/          - Recursos (música, imágenes, gráficos)"
  echo "  04_script/             - Guiones y notas"
  echo "  video_tracker.md       - Plantilla de seguimiento del proyecto"
  echo "  README.md              - Información del proyecto"
  echo ""
  echo "Ejemplos:"
  echo "  yv new 'Mi Primer Video'"
  echo "  yv new 'Tutorial_Python'"
  echo "  yv new Vlog_2025"
}

# =============================
# Main - Punto de entrada del script
# =============================
case "$1" in
"new")
  # Validar que se proporcione el nombre del proyecto
  if [ -z "$2" ]; then
    echo "❌ Error: Falta nombre del proyecto"
    echo ""
    show_help
    exit 1
  fi
  project_name="$2"
  create_project "$project_name"
  ;;
"help" | "--help" | "-h")
  show_help
  ;;
*)
  echo "Comando no reconocido"
  show_help
  exit 1
  ;;
esac
