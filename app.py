#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="CLI para compresión de imágenes con cwebp"
    )

    parser.add_argument(
        "archivo",
        help="Ruta de la imagen a procesar"
    )

    args = parser.parse_args()

    print(f"✔ Procesando archivo: {args.archivo}")

if __name__ == "__main__":
    main()
