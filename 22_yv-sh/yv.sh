#!/bin/bash

# =============================
# 📹 Plantilla de Seguimiento
# =============================
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
  shift
  local args=("$@")

  local safe_name
  safe_name=$(echo "$project_name" | tr ' ' '_' | tr -cd '[:alnum:]_')
  local use_git=false

  # Parsear flags
  for arg in "${args[@]}"; do
    case "$arg" in
      --git) use_git=true ;;
    esac
  done

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

  # Archivos iniciales
  touch "02_edit_project/${safe_name}.kdenlive"
  touch "02_exports/${safe_name}_v1.mp4"
  touch "02_exports/${safe_name}_thumbnail.jpg"

  touch "04_script/script_${safe_name}.md"
  echo "# Notas del proyecto" > "04_script/notes_${safe_name}.txt"

  # Generar video_tracker.md desde la variable global
  echo "$VIDEO_TRACKER_TEMPLATE" \
    | sed "s/{{FECHA}}/$(date '+%Y-%m-%d')/g" \
    | sed "s/{{NOMBRE_PROYECTO}}/$safe_name/g" \
    > "video_tracker.md"

  # README.md básico
  echo "# $project_name" > "README.md"
  echo "- Fecha: $(date '+%Y-%m-%d')" >> "README.md"
  echo "- Estado: En curso" >> "README.md"

  # Git opcional
  if [ "$use_git" = true ]; then
    git init >/dev/null
    git add . >/dev/null
    git commit -m "Initial commit: $project_name" >/dev/null
    echo "✅ Repositorio Git inicializado"
  fi

  echo "✅ Proyecto creado en: $(pwd)"
  echo "Estructura creada:"
  if command -v tree >/dev/null; then
    tree -L 3
  else
    find . -maxdepth 3 -type d
  fi
}

show_help() {
  echo "Uso:"
  echo "  yv new <nombre-proyecto> [--git]  Crea nuevo proyecto"
  echo "  yv help                          Muestra esta ayuda"
  echo ""
  echo "Ejemplo:"
  echo "  yv new 'MiVideo' --git"
}

# =============================
# Main
# =============================
case "$1" in
"new")
  if [ -z "$2" ]; then
    echo "Error: Falta nombre del proyecto"
    show_help
    exit 1
  fi
  project_name="$2"
  shift 2
  create_project "$project_name" "$@"
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
