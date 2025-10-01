#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def construir_comando(file: str, salida: str, metadata_all: bool, lossless: bool, to_jpg: bool, resize_twelve: bool):
    """Construye el comando de conversión"""
    if to_jpg:
        comando = ["cwebp", file, "-o", "temp.webp"]

        # Opciones de compresión
        if lossless:
            comando.append("-lossless")
        else:
            comando.extend(["-q", "80"])

        # Metadatos
        if metadata_all:
            comando.extend(["-metadata", "all"])

        # Resize si aplica
        if resize_twelve:
            comando.extend(["-resize", "12", "12"])

        return [comando, ["dwebp", "temp.webp", "-o", salida]]

    else:
        comando = ["cwebp"]

        # Opciones de compresión
        if lossless:
            comando.append("-lossless")
        else:
            comando.extend(["-q", "80"])

        # Metadatos
        if metadata_all:
            comando.extend(["-metadata", "all"])

        # Resize si aplica
        if resize_twelve:
            comando.extend(["-resize", "12", "12"])

        comando.extend([file, "-o", salida])
        return [comando]


def comprimir_pequeño(file: str, no_renombrar: bool, metadata_all: bool, lossless: bool, eliminar: bool, to_jpg: bool, resize_twelve: bool):
    """Comprime una sola imagen"""
    if not os.path.isfile(file):
        sys.stderr.write(f"❌ Error: No se encontró el archivo {file}\n")
        sys.exit(1)

    ext = os.path.splitext(file)[1].lower()
    formatos_validos = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
    if ext not in formatos_validos:
        sys.stderr.write(f"❌ Error: Formato {ext} no soportado\n")
        sys.exit(1)

    # Nombre de salida
    if no_renombrar:
        salida = f"{os.path.splitext(file)[0]}.{'jpg' if to_jpg else 'webp'}"
    else:
        salida = f"{os.path.splitext(file)[0]}-small.{'jpg' if to_jpg else 'webp'}"

    # Ejecutar comandos
    comandos = construir_comando(file, salida, metadata_all, lossless, to_jpg, resize_twelve)
    for cmd in comandos:
        subprocess.run(cmd, check=True)

    print(f"✔ Imagen comprimida guardada como {salida}")

    # Eliminar archivo original si se solicita
    if eliminar:
        try:
            os.remove(file)
            print(f"🗑 Imagen original eliminada: {file}")
        except Exception as e:
            print(f"⚠ No se pudo eliminar {file}: {e}")


def comprimir_pequeños(files: list[str], no_renombrar: bool, metadata_all: bool, lossless: bool, eliminar: bool, to_jpg: bool, resize_twelve: bool):
    """Comprime múltiples imágenes"""
    for file in files:
        try:
            comprimir_pequeño(file, no_renombrar, metadata_all, lossless, eliminar, to_jpg, resize_twelve)
        except Exception as e:
            print(f"⚠ No se pudo comprimir {file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI para compresión/conversión de imágenes con cwebp"
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando "pequeño"
    parser_pequeño = subparsers.add_parser("pequeño", help="Comprimir una sola imagen")
    parser_pequeño.add_argument("file", help="Archivo de imagen de entrada")
    parser_pequeño.add_argument("--no-renombrar", action="store_true", help="Mantener el mismo nombre")
    parser_pequeño.add_argument("--metadata-all", action="store_true", help="Conservar todos los metadatos")
    parser_pequeño.add_argument("--lossless", action="store_true", help="Usar compresión sin pérdida")
    parser_pequeño.add_argument("--eliminar", action="store_true", help="Eliminar la imagen original después")
    parser_pequeño.add_argument("--to-jpg", action="store_true", help="Convertir la imagen a JPG en lugar de WebP")
    parser_pequeño.add_argument("--resize-twelve", action="store_true", help="Redimensionar a 12x12")

    # Subcomando "pequeños"
    parser_pequeños = subparsers.add_parser("pequeños", help="Comprimir varias imágenes")
    parser_pequeños.add_argument("files", nargs="+", help="Archivos de imagen de entrada")
    parser_pequeños.add_argument("--no-renombrar", action="store_true", help="Mantener el mismo nombre")
    parser_pequeños.add_argument("--metadata-all", action="store_true", help="Conservar todos los metadatos")
    parser_pequeños.add_argument("--lossless", action="store_true", help="Usar compresión sin pérdida")
    parser_pequeños.add_argument("--eliminar", action="store_true", help="Eliminar las imágenes originales después")
    parser_pequeños.add_argument("--to-jpg", action="store_true", help="Convertir las imágenes a JPG en lugar de WebP")
    parser_pequeños.add_argument("--resize-twelve", action="store_true", help="Redimensionar a 12x12")

    args = parser.parse_args()

    if args.comando == "pequeño":
        comprimir_pequeño(args.file, args.no_renombrar, args.metadata_all, args.lossless, args.eliminar, args.to_jpg, args.resize_twelve)

    elif args.comando == "pequeños":
        comprimir_pequeños(args.files, args.no_renombrar, args.metadata_all, args.lossless, args.eliminar, args.to_jpg, args.resize_twelve)


if __name__ == "__main__":
    main()
