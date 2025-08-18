#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def comprimir_pequeño(file: str):
    """Comprime una sola imagen usando cwebp"""
    # Validación: existe el archivo
    if not os.path.isfile(file):
        sys.stderr.write(f"❌ Error: No se encontró el archivo {file}\n")
        sys.exit(1)

    # Validación: extensión soportada
    ext = os.path.splitext(file)[1].lower()
    formatos_validos = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
    if ext not in formatos_validos:
        sys.stderr.write(f"❌ Error: Formato {ext} no soportado por cwebp\n")
        sys.exit(1)

    # Generar nombre de salida
    salida = f"{os.path.splitext(file)[0]}-small.webp"

    # Ejecutar cwebp (calidad estándar 80)
    subprocess.run(["cwebp", "-q", "80", file, "-o", salida], check=True)

    print(f"✔ Imagen comprimida guardada como {salida}")


def comprimir_pequeños(files: list[str]):
    """Comprime múltiples imágenes usando la lógica de pequeño"""
    for file in files:
        try:
            comprimir_pequeño(file)
        except Exception as e:
            print(f"⚠ No se pudo comprimir {file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI para compresión de imágenes con cwebp"
    )

    parser.add_argument("comando", help="Comando a ejecutar (ej: pequeño, pequeños)")
    parser.add_argument("files", nargs="+", help="Archivo(s) de imagen de entrada")

    args = parser.parse_args()

    if args.comando == "pequeño":
        if len(args.files) != 1:
            sys.stderr.write("❌ Error: 'pequeño' solo acepta un archivo\n")
            sys.exit(1)
        comprimir_pequeño(args.files[0])

    elif args.comando == "pequeños":
        comprimir_pequeños(args.files)

    else:
        sys.stderr.write(f"❌ Comando desconocido: {args.comando}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
