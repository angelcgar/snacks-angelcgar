# 🎵 add-metadata

CLI para agregar metadatos ID3 (Artist/Album) a archivos de audio **sin
renombrarlos**.

## 📋 Características

- ✅ Actualiza metadatos Artist y Album usando ExifTool
- ✅ Búsqueda de archivos mediante expresiones regulares
- ✅ Procesa múltiples archivos en batch
- ✅ No modifica nombres de archivos
- ✅ Soporta formatos: MP3, M4A, FLAC, WAV, y más
- ✅ Estadísticas detalladas de procesamiento

## 🔧 Requisitos

- Python 3.7+
- ExifTool

### Instalar ExifTool

**Ubuntu/Debian:**

```bash
sudo apt-get install libimage-exiftool-perl
```

**macOS:**

```bash
brew install exiftool
```

**Windows:** Descargar desde [exiftool.org](https://exiftool.org)

## 📦 Instalación

```bash
cd 29_add-author-py
python3 install.py
```

El script instalará el CLI en `~/.local/bin/add-metadata`.

## 🚀 Uso

### Sintaxis básica

```bash
add-metadata --artist "Artist Name" --album "Album Name" --pattern "regex_pattern" [--path directory]
```

### Parámetros

| Flag        | Tipo   | Requerido | Descripción                            |
| ----------- | ------ | --------- | -------------------------------------- |
| `--artist`  | string | Sí        | Artista a escribir en los metadatos    |
| `--album`   | string | Sí        | Álbum a escribir en los metadatos      |
| `--pattern` | regex  | Sí        | Expresión regular para buscar archivos |
| `--path`    | string | No        | Directorio de búsqueda (default: `.`)  |

### Ejemplos

**Actualizar todos los archivos MP3:**

```bash
add-metadata --artist "Led Zeppelin" --album "IV" --pattern ".*\.mp3$"
```

**Actualizar archivos M4A que empiecen con "track":**

```bash
add-metadata --artist "Pink Floyd" --album "Dark Side" --pattern "^track.*\.m4a$"
```

**Procesar archivos en directorio específico:**

```bash
add-metadata --artist "The Beatles" --album "Abbey Road" --pattern ".*\.flac$" --path /home/music/albums
```

**Actualizar archivos numerados:**

```bash
add-metadata --artist "AC/DC" --album "Back in Black" --pattern "^[0-9]{2}.*\.mp3$"
```

## 📊 Salida

El CLI muestra:

- ✅ Archivos procesados exitosamente
- ❌ Archivos con errores
- 📊 Resumen final con estadísticas

### Ejemplo de salida

```
🔍 Buscando archivos en '.' con patrón: .*\.mp3$
✅ Encontrados 5 archivo(s)

🎵 Procesando 5 archivo(s)...

📝 Actualizando: song1.mp3
   ✅ Éxito

📝 Actualizando: song2.mp3
   ✅ Éxito

📝 Actualizando: song3.mp3
   ✅ Éxito

============================================================
📊 RESUMEN
============================================================
Artista aplicado:  Led Zeppelin
Álbum aplicado:    IV

Archivos procesados: 5
  ✅ Exitosos:       5
  ❌ Fallidos:       0
============================================================
```

## 🧩 Estructura del código

```
29_add-author-py/
├── add_metadata.py    # Script principal del CLI
├── install.py         # Script de instalación
└── README.md          # Este archivo
```

### Funciones principales

- `parse_arguments()` - Configura y parsea argumentos CLI
- `check_exiftool_installed()` - Verifica disponibilidad de ExifTool
- `find_matching_files()` - Busca archivos por patrón regex
- `update_file_metadata()` - Actualiza metadatos con ExifTool
- `process_files()` - Procesa múltiples archivos en batch
- `print_summary()` - Muestra estadísticas finales

## 🔍 Expresiones regulares útiles

| Patrón                    | Descripción                                |
| ------------------------- | ------------------------------------------ |
| `.*\.mp3$`                | Todos los archivos .mp3                    |
| `.*\.m4a$`                | Todos los archivos .m4a                    |
| `^track.*\.mp3$`          | Archivos que empiezan con "track"          |
| `^[0-9]{2}.*\.flac$`      | Archivos que empiezan con 2 dígitos        |
| `.*(song\|track).*\.mp3$` | Archivos con "song" o "track" en el nombre |

## ⚙️ Notas técnicas

- **ExifTool** escribe metadatos sin archivo de respaldo (`-overwrite_original`)
- Los metadatos se escriben usando campos estándar: `-Artist` y `-Album`
- El CLI usa `subprocess` para invocar ExifTool
- La búsqueda de archivos es recursiva (`rglob`)
- Los nombres de archivos **no se modifican**

## 🐛 Solución de problemas

**Error: ExifTool no está instalado**

- Instala ExifTool siguiendo las instrucciones de instalación

**Error: Patrón regex inválido**

- Verifica la sintaxis de tu expresión regular
- Usa herramientas como [regex101.com](https://regex101.com) para testear

**No se encontraron archivos**

- Verifica que el patrón coincide con los nombres de archivo
- Asegúrate de estar en el directorio correcto o usa `--path`

## 📝 Licencia

Este proyecto es parte del repositorio `snacks` y sigue la misma licencia.

## 👤 Autor

angelcgar
