#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def construir_comando_cwebp(file: str, salida: str, metadata_all: bool, lossless: bool):
    """Construye el comando cwebp con las banderas correspondientes"""
    comando = ["cwebp"]

    # Opciones de compresión
    if lossless:
        comando.append("-lossless")
    else:
        comando.extend(["-q", "80"])  # calidad estándar

    # Metadatos
    if metadata_all:
        comando.extend(["-metadata", "all"])

    # Entrada y salida
    comando.extend([file, "-o", salida])

    return comando


def comprimir_pequeño(file: str, no_renombrar: bool, metadata_all: bool, lossless: bool):
    """Comprime una sola imagen"""
    if not os.path.isfile(file):
        sys.stderr.write(f"❌ Error: No se encontró el archivo {file}\n")
        sys.exit(1)

    ext = os.path.splitext(file)[1].lower()
    formatos_validos = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
    if ext not in formatos_validos:
        sys.stderr.write(f"❌ Error: Formato {ext} no soportado por cwebp\n")
        sys.exit(1)

    # Nombre de salida
    if no_renombrar:
        salida = f"{os.path.splitext(file)[0]}.webp"
    else:
        salida = f"{os.path.splitext(file)[0]}-small.webp"

    # Ejecutar cwebp
    comando = construir_comando_cwebp(file, salida, metadata_all, lossless)
    subprocess.run(comando, check=True)

    print(f"✔ Imagen comprimida guardada como {salida}")


def comprimir_pequeños(files: list[str], no_renombrar: bool, metadata_all: bool, lossless: bool):
    """Comprime múltiples imágenes"""
    for file in files:
        try:
            comprimir_pequeño(file, no_renombrar, metadata_all, lossless)
        except Exception as e:
            print(f"⚠ No se pudo comprimir {file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI para compresión de imágenes con cwebp"
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando "pequeño"
    parser_pequeño = subparsers.add_parser("pequeño", help="Comprimir una sola imagen")
    parser_pequeño.add_argument("file", help="Archivo de imagen de entrada")
    parser_pequeño.add_argument("--no-renombrar", action="store_true", help="Mantener el mismo nombre (solo cambia la extensión a .webp)")
    parser_pequeño.add_argument("--metadata-all", action="store_true", help="Conservar todos los metadatos")
    parser_pequeño.add_argument("--lossless", action="store_true", help="Usar compresión sin pérdida")

    # Subcomando "pequeños"
    parser_pequeños = subparsers.add_parser("pequeños", help="Comprimir varias imágenes")
    parser_pequeños.add_argument("files", nargs="+", help="Archivos de imagen de entrada")
    parser_pequeños.add_argument("--no-renombrar", action="store_true", help="Mantener el mismo nombre (solo cambia la extensión a .webp)")
    parser_pequeños.add_argument("--metadata-all", action="store_true", help="Conservar todos los metadatos")
    parser_pequeños.add_argument("--lossless", action="store_true", help="Usar compresión sin pérdida")

    args = parser.parse_args()

    if args.comando == "pequeño":
        comprimir_pequeño(args.file, args.no_renombrar, args.metadata_all, args.lossless)

    elif args.comando == "pequeños":
        comprimir_pequeños(args.files, args.no_renombrar, args.metadata_all, args.lossless)


if __name__ == "__main__":
    main()
