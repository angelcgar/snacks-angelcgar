# 🎯 Referencia Rápida: Flag --use-id3v2

## ✅ Cambio implementado

Se ha agregado el flag opcional `--use-id3v2` que permite usar **id3v2** en
lugar de **ExifTool** para actualizar metadatos.

## 🔧 Cuándo usar --use-id3v2

Usa este flag cuando:

- ✅ Trabajas con archivos MP3 muy antiguos
- ✅ Procesas archivos descargados de YouTube
- ✅ ExifTool te da el error: "Writing of MP3 files is not yet supported"
- ✅ Quieres una herramienta más específica para MP3

## 📦 Instalación de id3v2

Antes de usar `--use-id3v2`, instala id3v2:

**Ubuntu/Debian:**

```bash
sudo apt-get install id3v2
```

**macOS:**

```bash
brew install id3v2
```

**Arch Linux:**

```bash
sudo pacman -S id3v2
```

## 🚀 Ejemplos de uso

### Ejemplo 1: Procesar archivos con patrón

```bash
# Todos los MP3 en directorio actual
add-metadata --artist "plantasVsZombies" --pattern ".*\.mp3$" --use-id3v2

# Con álbum opcional
add-metadata --artist "plantasVsZombies" --album "PvZ OST" --pattern ".*\.mp3$" --use-id3v2
```

### Ejemplo 2: Modo debugging (un solo archivo)

```bash
# Sin álbum
add-metadata --artist "plantasVsZombies" --file "Ultimate Battle.mp3" --use-id3v2

# Con álbum
add-metadata --artist "plantasVsZombies" --album "PvZ OST" --file "Ultimate Battle.mp3" --use-id3v2
```

### Ejemplo 3: Directorio específico

```bash
add-metadata --artist "Artist" --pattern ".*\.mp3$" --path ~/Music/YouTube --use-id3v2
```

## 📊 Comparación: ExifTool vs id3v2

| Característica      | ExifTool                          | id3v2                          |
| ------------------- | --------------------------------- | ------------------------------ |
| Formatos soportados | Todos (MP3, M4A, FLAC, WAV, etc.) | Solo MP3                       |
| MP3 antiguos        | ⚠️ Puede fallar                   | ✅ Funciona bien               |
| MP3 de YouTube      | ⚠️ Puede fallar                   | ✅ Funciona bien               |
| Velocidad           | Media                             | Rápida                         |
| Instalación         | Más compleja                      | Fácil                          |
| Uso                 | `add-metadata ...`                | `add-metadata ... --use-id3v2` |

## 🧩 Cambios técnicos realizados

### Archivos modificados:

- ✅ `add_metadata.py` - Añadido soporte completo para id3v2

### Funciones nuevas:

1. `check_id3v2_installed()` - Verifica si id3v2 está disponible
2. `update_file_metadata_id3v2()` - Actualiza metadatos usando id3v2
3. `update_file_metadata_exiftool()` - Función refactorizada para ExifTool
4. `update_file_metadata()` - Wrapper que decide qué herramienta usar

### Parámetros actualizados:

- `update_file_metadata()` ahora acepta `use_id3v2: bool`
- `process_files()` ahora acepta `use_id3v2: bool`
- `main()` valida qué herramienta usar y verifica su instalación

## 🎯 Workflow recomendado para tu caso

**Paso 1: Instalar id3v2**

```bash
sudo apt-get install id3v2
```

**Paso 2: Probar con un archivo primero**

```bash
cd ~/plantasVsZombiesSountrack  # o donde estén tus archivos
add-metadata --artist "plantasVsZombies" --file "Ultimate Battle.mp3" --use-id3v2
```

**Paso 3: Si funciona, procesar todos**

```bash
add-metadata --artist "plantasVsZombies" --pattern ".*\.mp3$" --use-id3v2
```

## 💡 Salida esperada

### Con --use-id3v2:

```
🔧 Usando id3v2 para actualizar metadatos

🔍 Buscando archivos en '.' con patrón: .*\.mp3$
✅ Encontrados 22 archivo(s)

🎵 Procesando 22 archivo(s)...

📝 Actualizando: Ultimate Battle.mp3
   ✅ Éxito

📝 Actualizando: Graze the Roof.mp3
   ✅ Éxito

...

============================================================
📊 RESUMEN
============================================================
Artista aplicado:  plantasVsZombies
Álbum aplicado:    (no especificado)

Archivos procesados: 22
  ✅ Exitosos:       22
  ❌ Fallidos:       0
============================================================
```

## 🔍 Verificar metadatos después

```bash
# Con id3v2
id3v2 -l "Ultimate Battle.mp3"

# Con exiftool (lectura)
exiftool -Artist -Album "Ultimate Battle.mp3"

# Con reproductores
vlc "Ultimate Battle.mp3"
```

## ⚠️ Notas importantes

1. **Solo para MP3**: id3v2 solo funciona con archivos MP3, no con M4A, FLAC,
   etc.
2. **Compatibilidad total**: Funciona con todos los flags existentes (`--album`,
   `--file`, `--pattern`, `--path`)
3. **Sin conflicto**: No necesitas desinstalar ExifTool, puedes tener ambos
4. **Álbum opcional**: Funciona igual con o sin `--album`

## 🐛 Si algo falla

**Error: id3v2 no está instalado**

```bash
# El CLI te mostrará cómo instalarlo
sudo apt-get install id3v2
```

**Error: command not found**

```bash
# Verifica que está instalado
which id3v2
id3v2 --version
```

**Los metadatos no se actualizan**

```bash
# Prueba manualmente primero
id3v2 -a "TestArtist" "archivo.mp3"
id3v2 -l "archivo.mp3"  # Ver metadatos
```

## ✨ Ventajas de esta implementación

- ✅ **No rompe nada**: Todo el código anterior sigue funcionando
- ✅ **Totalmente opcional**: Sin `--use-id3v2` usa ExifTool como antes
- ✅ **Mismo comportamiento**: Misma lógica para ambos modos
- ✅ **Validación automática**: Verifica que la herramienta esté instalada
- ✅ **Mensajes claros**: Indica qué herramienta está usando
- ✅ **Debugging sencillo**: Combina con `--file` para probar
