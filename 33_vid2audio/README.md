# vid2audio

Extrae audio de archivos de video y convierte a formato MP3 con buena calidad.

## 📋 Descripción

`vid2audio` es una herramienta de línea de comandos que utiliza `ffmpeg` para extraer el audio de archivos de video y convertirlo a formato MP3. La configuración de calidad está optimizada para obtener un buen balance entre calidad de audio y tamaño de archivo.

## ✨ Características

- ✅ Extracción de audio desde cualquier formato de video soportado por ffmpeg
- ✅ Conversión automática a MP3 con codec libmp3lame
- ✅ Calidad optimizada (q:a 2 - aproximadamente 190 kbps VBR)
- ✅ Generación automática del nombre de salida si no se especifica
- ✅ Validación de archivos de entrada
- ✅ Validación de dependencias (ffmpeg)

## 📦 Instalación

### Requisitos previos

- `ffmpeg` - Para la conversión de medios

**Instalar ffmpeg:**

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# macOS
brew install ffmpeg
```

### Instalar vid2audio

```bash
cd 33_vid2audio
chmod +x install.sh
./install.sh
```

El script se instalará como `vid2audio` en `~/.local/bin/`.

## 🚀 Uso

### Sintaxis básica

```bash
vid2audio <video_entrada> [audio_salida]
```

### Ejemplos

**Convertir video a MP3 (nombre automático):**
```bash
vid2audio video.mp4
# Genera: video.mp3
```

**Especificar nombre de salida:**
```bash
vid2audio video.mp4 mi_audio.mp3
# Genera: mi_audio.mp3
```

**Diferentes formatos de entrada:**
```bash
vid2audio pelicula.mkv banda_sonora.mp3
vid2audio grabacion.avi audio.mp3
vid2audio clip.mov podcast.mp3
```

### Opciones

- `-h, --help` - Muestra la ayuda

## 📊 Calidad de audio

El script utiliza la configuración `-q:a 2` (VBR Quality 2) que resulta en:
- **Bitrate promedio**: ~190 kbps VBR
- **Rango de bitrate**: 170-210 kbps
- **Calidad**: Muy buena para la mayoría de usos
- **Tamaño**: Balance óptimo entre calidad y peso

Si necesitas cambiar la calidad, edita el script y modifica el parámetro `-q:a`:
- `0` = mejor calidad (~245 kbps)
- `2` = muy buena calidad (~190 kbps) ⭐ **predeterminado**
- `4` = buena calidad (~165 kbps)
- `6` = calidad aceptable (~130 kbps)

## 🗑️ Desinstalación

```bash
cd 33_vid2audio
./uninstall.sh
```

## 🔧 Solución de problemas

**Error: ffmpeg no está instalado**
```
❌ Error: ffmpeg no está instalado.
Instala ffmpeg para usar este script.
```
Solución: Instala ffmpeg usando tu gestor de paquetes.

**Error: El archivo no existe**
```
❌ Error: El archivo 'video.mp4' no existe.
```
Solución: Verifica que la ruta del archivo sea correcta.

**Error al procesar el video**
```
❌ Error al procesar el video.
```
Solución: Verifica que el archivo de video no esté corrupto y que ffmpeg pueda leerlo.

## 💡 Casos de uso

- Extraer audio de videos descargados para escuchar offline
- Convertir grabaciones de pantalla a podcasts
- Crear archivos de audio desde conferencias grabadas
- Extraer música de videos musicales
- Generar audiolibros desde videos educativos

## 📝 Notas técnicas

- **Codec de salida**: libmp3lame (MP3)
- **Sin video**: `-vn` flag
- **Calidad VBR**: `-q:a 2`
- **Validación**: Verifica entrada y dependencias antes de procesar
- **Error handling**: Detecta errores de ffmpeg y reporta status

## 🔗 Ver también

- [ffmpeg Documentation](https://ffmpeg.org/documentation.html)
- [MP3 VBR Quality Settings](https://trac.ffmpeg.org/wiki/Encode/MP3)

## 📄 Licencia

Este script es de uso libre y forma parte de la colección de snacks personales.

---

**Autor**: Angel Contreras Garcia
**Versión**: 1.0.0
