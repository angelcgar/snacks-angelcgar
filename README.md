# Snacks - Colección de Scripts Personales

Repositorio de scripts y herramientas CLI personales para automatización y productividad.

## 📦 Inventario de Snacks

| #   | Carpeta                        | Comando                | Descripción                                       | Notas                    |
| --- | ------------------------------ | ---------------------- | ------------------------------------------------- | ------------------------ |
| 00  | `00_actualizar-sh`             | `actualizar`           | Actualiza sistema y paquetes (apt, flatpak, snap) |                          |
| 01  | `01_actualizar-cv-sh`          | -                      | Actualiza CV en formato específico                |                          |
| 02  | `02_img-py`                    | -                      | Procesamiento de imágenes                         |                          |
| 03  | `03_bitacora-cli-py`           | `bitacora`             | Sistema de bitácora CLI con templates             |                          |
| 04  | `04_agregar-metadatos`         | `add-metadata`         | Agrega frontmatter a posts de blog                | Refactorizado v1.0.0     |
| 05  | `05_biblioteca-cli-py`         | `biblioteca`           | Gestión de biblioteca personal                    |                          |
| 06  | `06_fechas-sh`                 | `fechas`               | Manipulación y conversión de fechas               |                          |
| 07  | `07_fish-sh`                   | -                      | Scripts personalizados para Fish shell            |                          |
| 08  | `08_gh-helper`                 | `gh-helper`            | Helper para comandos de GitHub CLI                |                          |
| 09  | `09_i-sh`                      | `i`                    | Instalador rápido de paquetes                     |                          |
| 10  | `10_inicio-sh`                 | `inicio`               | Script de inicio/configuración de entorno         |                          |
| 11  | `11_md-to-pdf-py`              | `mdtool`               | Convierte Markdown a PDF                          |                          |
| 12  | `12_metadata-sh`               | `metadata`             | Gestión de metadatos de archivos                  |                          |
| 13  | `13_orden-sh`                  | `organizar`            | Organiza archivos por tipo/fecha                  |                          |
| 14  | `14_pi-sh`                     | `pi`                   | Calculadora de dígitos de Pi                      |                          |
| 15  | `15_renombrar-minusculas-sh`   | `renombrar_minusculas` | Convierte nombres de archivo a minúsculas         |                          |
| 16  | `16_tablas-multiplicar-sh`     | `tablas_multiplicar`   | Genera tablas de multiplicar                      |                          |
| 17  | `17_today-sh`                  | `today`                | Generador de notas diarias con templates          |                          |
| 18  | `18_today-sh-templates`        | -                      | Templates para today                              |                          |
| 19  | `19_bitacora-cli-py-templates` | -                      | Templates para bitacora                           |                          |
| 20  | `20_ts-init-node-sh`           | `ts-init-node`         | Inicializa proyectos TypeScript/Node.js           |                          |
| 21  | `21_veamos`                    | `veamos`               | Visor de archivos y contenido                     |                          |
| 22  | `22_yv-sh`                     | `yv`                   | Generador de estructura para proyectos de video   | Instalado con assets     |
| 23  | `23_doc-manager-py`            | `doc-manager`          | Gestor de documentos                              |                          |
| 24  | `24_harbor-py`                 | `harbor`               | Gestor de contenedores y proyectos                |                          |
| 25  | `25_actualizar-cv-py`          | `actualizar-cv`        | Versión Python de actualizar CV                   |                          |
| 26  | `26_fetch_ig_photos`           | -                      | Descarga fotos de Instagram                       |                          |
| 27  | `27_social-cli`                | `social`               | CLI para redes sociales                           |                          |
| 28  | `28_mvnx`                      | `mvnx`                 | Mover archivos con patrón extendido               |                          |
| 29  | `29_add-author-py`             | `add-metadata`         | Agrega metadatos ID3 a archivos de audio          | Soporta ExifTool e id3v2 |
| 30  | `30_switch_teclado-sh`         | `switch-keyboard`      | Alterna entre layouts de teclado US/LATAM         | Con guía reutilizable    |
| 32  | `32_note-sh`                   | `nota`                 | Gestor de notas con templates Markdown            | Normalización UTF-8      |
| 33  | `33_vid2audio`                 | `vid2audio`            | Extrae audio de videos a MP3                      | Calidad VBR optimizada   |


## 🔧 Estructura Típica

La mayoría de los snacks siguen esta estructura:

```
XX_nombre-herramienta/
├── app.sh / app.py          # Script principal
├── install.sh / install.py  # Script de instalación
├── uninstall.sh            # Script de desinstalación
└── README.md               # Documentación
```

## 📝 Notas

- Algunos scripts continuaron su desarrollo en otros repositorios
- Los scripts con carpeta de templates necesitan configuración adicional
- Revisar README individual de cada snack para instrucciones específicas
