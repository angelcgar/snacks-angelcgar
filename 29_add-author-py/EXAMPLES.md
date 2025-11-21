# 🎯 Ejemplos de uso - add-metadata CLI

## Instalación

```bash
# Desde el directorio 29_add-author-py
python3 install.py
```

## Casos de uso comunes

### 1. Actualizar todos los MP3 en el directorio actual

```bash
add-metadata --artist "Led Zeppelin" --album "Led Zeppelin IV" --pattern ".*\.mp3$"
```

### 2. Actualizar archivos M4A con patrón específico

```bash
add-metadata --artist "Pink Floyd" --album "The Dark Side of the Moon" --pattern "track.*\.m4a$"
```

### 3. Procesar archivos en otro directorio

```bash
add-metadata \
  --artist "The Beatles" \
  --album "Abbey Road" \
  --pattern ".*\.flac$" \
  --path ~/Music/Beatles
```

### 4. Archivos numerados (01-song.mp3, 02-song.mp3)

```bash
add-metadata --artist "AC/DC" --album "Back in Black" --pattern "^[0-9]{2}.*\.mp3$"
```

### 5. Buscar archivos con texto específico

```bash
add-metadata --artist "Queen" --album "A Night at the Opera" --pattern ".*bohemian.*\.mp3$"
```

### 6. Múltiples extensiones (mp3 o m4a)

```bash
add-metadata --artist "Miles Davis" --album "Kind of Blue" --pattern ".*\.(mp3|m4a)$"
```

## Patrones regex útiles

| Patrón            | Descripción           | Ejemplo de archivo        |
| ----------------- | --------------------- | ------------------------- | --------------------- |
| `.*\.mp3$`        | Todos los MP3         | cualquier-nombre.mp3      |
| `^track.*\.mp3$`  | Empieza con "track"   | track01.mp3               |
| `^[0-9]{2}.*`     | Empieza con 2 dígitos | 01-song.mp3               |
| `.\*(live         | remix).\*`            | Contiene "live" o "remix" | song-live-version.mp3 |
| `^[A-Z].*\.flac$` | Empieza con mayúscula | Song.flac                 |

## Workflow típico

### 1. Verificar archivos antes de actualizar

```bash
# Listar archivos que coinciden
ls -1 | grep -E ".*\.mp3$"
```

### 2. Ejecutar actualización

```bash
add-metadata --artist "Artist" --album "Album" --pattern ".*\.mp3$"
```

### 3. Verificar metadatos actualizados

```bash
# Usar exiftool directamente para verificar
exiftool -Artist -Album song.mp3
```

## Salida esperada

```
🔍 Buscando archivos en '.' con patrón: .*\.mp3$
✅ Encontrados 3 archivo(s)

🎵 Procesando 3 archivo(s)...

📝 Actualizando: 01-track.mp3
   ✅ Éxito

📝 Actualizando: 02-track.mp3
   ✅ Éxito

📝 Actualizando: 03-track.mp3
   ✅ Éxito

============================================================
📊 RESUMEN
============================================================
Artista aplicado:  Led Zeppelin
Álbum aplicado:    IV

Archivos procesados: 3
  ✅ Exitosos:       3
  ❌ Fallidos:       0
============================================================
```

## Tips

1. **Prueba primero con un archivo**: Usa un patrón específico para probar con
   un solo archivo
2. **Verifica el patrón**: Usa herramientas como https://regex101.com para
   validar tu regex
3. **Backup**: Aunque ExifTool es seguro, considera hacer backup de archivos
   importantes
4. **Verifica después**: Usa `exiftool` o tu reproductor de música para
   confirmar los cambios

## Formatos soportados

ExifTool soporta múltiples formatos de audio:

- MP3 (ID3v1, ID3v2)
- M4A/MP4 (iTunes metadata)
- FLAC (Vorbis comments)
- WAV (RIFF INFO)
- OGG (Vorbis comments)
- WMA (Windows Media)
- Y muchos más...
