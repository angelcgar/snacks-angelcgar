# 🐛 Debugging: Error "Writing of MP3 files is not yet supported"

## Problema detectado

ExifTool está reportando que **no puede escribir archivos MP3**. Este es un
error inusual porque ExifTool normalmente soporta MP3.

## Posibles causas

### 1. **Versión de ExifTool desactualizada**

ExifTool muy antiguo podría no tener soporte completo para MP3.

```bash
# Verificar versión
exiftool -ver

# Versión recomendada: 12.0 o superior
```

### 2. **ExifTool compilado sin soporte MP3**

Algunas distribuciones podrían tener ExifTool compilado sin soporte para ciertas
características.

### 3. **Archivos MP3 corruptos o con formato no estándar**

Los archivos podrían tener estructura interna problemática.

## 🔍 Cómo debuggear

### Paso 1: Verificar versión de ExifTool

```bash
exiftool -ver
```

### Paso 2: Probar con un solo archivo

```bash
# Usar el modo debugging del CLI
add-metadata --artist "TestArtist" --file "Ultimate Battle.mp3"
```

### Paso 3: Verificar estructura del archivo MP3

```bash
# Ver metadatos actuales (solo lectura)
exiftool "Ultimate Battle.mp3"

# Verificar formato
file "Ultimate Battle.mp3"
```

### Paso 4: Probar ExifTool directamente

```bash
# Intentar escribir directamente con ExifTool
exiftool -Artist="TestArtist" "Ultimate Battle.mp3"
```

Si este comando también falla, el problema es de ExifTool, no del CLI.

## ✅ Soluciones posibles

### Solución 1: Actualizar ExifTool

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install --reinstall libimage-exiftool-perl
```

**macOS:**

```bash
brew upgrade exiftool
```

**Instalación manual (última versión):**

```bash
# Descargar desde https://exiftool.org
cd /tmp
wget https://exiftool.org/Image-ExifTool-12.70.tar.gz
tar -xzf Image-ExifTool-12.70.tar.gz
cd Image-ExifTool-12.70
perl Makefile.PL
make test
sudo make install
```

### Solución 2: Usar ID3v2 en lugar de ExifTool

Si ExifTool no funciona, puedes instalar `id3v2` o `id3tool`:

**Ubuntu/Debian:**

```bash
sudo apt-get install id3v2
```

**Uso:**

```bash
id3v2 --artist "Artist Name" --album "Album Name" "file.mp3"
```

### Solución 3: Usar eyeD3 (Python)

Instalar eyeD3:

```bash
pip install eyeD3
```

Uso:

```bash
eyeD3 --artist "Artist Name" --album "Album Name" "file.mp3"
```

## 🔬 Script de diagnóstico

Crea un archivo `test_exiftool.sh`:

```bash
#!/bin/bash

echo "=== Diagnóstico de ExifTool ==="
echo ""

echo "1. Versión de ExifTool:"
exiftool -ver
echo ""

echo "2. Ubicación de ExifTool:"
which exiftool
echo ""

echo "3. Probando lectura de MP3:"
exiftool -Artist -Album "Ultimate Battle.mp3" 2>&1
echo ""

echo "4. Probando escritura de MP3:"
cp "Ultimate Battle.mp3" "test_temp.mp3"
exiftool -Artist="TestArtist" "test_temp.mp3" 2>&1
rm -f "test_temp.mp3" "test_temp.mp3_original"
echo ""

echo "5. Formato del archivo:"
file "Ultimate Battle.mp3"
echo ""

echo "=== Fin del diagnóstico ==="
```

Ejecutar:

```bash
chmod +x test_exiftool.sh
./test_exiftool.sh
```

## 🎯 Alternativa: Modificar el CLI para usar id3v2

Si ExifTool definitivamente no funciona, puedo modificar `add_metadata.py` para
que use `id3v2` en su lugar, que es más específico para MP3.

### Ventajas de id3v2:

- ✅ Diseñado específicamente para MP3
- ✅ Más ligero y rápido
- ✅ Mejor soporte para ID3v2 tags
- ✅ Ampliamente disponible en repositorios Linux

### Desventajas:

- ❌ Solo funciona con MP3 (no M4A, FLAC, etc.)

## 📊 Comparación de herramientas

| Herramienta | Formatos | Instalación | Confiabilidad |
| ----------- | -------- | ----------- | ------------- |
| ExifTool    | Todos    | Media       | ⭐⭐⭐⭐⭐    |
| id3v2       | Solo MP3 | Fácil       | ⭐⭐⭐⭐      |
| eyeD3       | Solo MP3 | pip         | ⭐⭐⭐⭐      |
| mid3v2      | Solo MP3 | pip         | ⭐⭐⭐        |

## 💡 Próximos pasos

1. Ejecuta el script de diagnóstico
2. Prueba con un solo archivo usando `--file`
3. Comparte la salida del diagnóstico
4. Decidimos si actualizar ExifTool o cambiar a id3v2
