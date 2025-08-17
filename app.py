#!/usr/bin/env python3
import argparse
import sys
import unicodedata
from datetime import datetime

# Constantes
VERSION = "0.0.1"
AUTHOR = "Sat Naing"

def hola_mundo(nombre):
    print(f"hola \"{nombre}\"")

def slugify(texto: str) -> str:
    """
    Convierte un texto en un slug legible para URLs.
    - Elimina acentos.
    - Mantiene la ñ como ñ.
    - Convierte espacios en guiones.
    - Pone todo en minúsculas.
    """
    # Normalizar pero conservar ñ
    texto = texto.replace("ñ", "__enie__")  # marcador temporal
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = texto.replace("__enie__", "ñ")
    # Reemplazar espacios y poner en minúscula
    texto = texto.strip().lower().replace(" ", "-")
    return texto

def procesar_basico(path_archivo, description=None):
    try:
        with open(path_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: el archivo '{path_archivo}' no existe.")
        sys.exit(1)

    if lineas[0].startswith("---"):
        print("Error: no se puede modificar este archivo (ya contiene frontmatter).")
        sys.exit(1)

    if not lineas[0].startswith("#"):
        print("Error: la primera línea no es un título principal '#'.")
        sys.exit(1)

    # Extraer título (sin '# ' inicial)
    titulo = lineas[0].lstrip("#").strip()
    slug = slugify(titulo)

    ahora = datetime.utcnow().isoformat() + "Z"

    frontmatter = f"""---
author: {AUTHOR}
pubDatetime: {ahora}
modDatetime: {ahora}
title: {titulo}
slug: {slug}
featured: true
draft: false
tags:
  - configuration
  - docs
description: {description if description else "How you can make AstroPaper theme absolutely yours."}
---
"""

    # Reescribir archivo con frontmatter + contenido original (sin la primera línea de título)
    nuevo_contenido = frontmatter + "".join(lineas[1:])

    with open(path_archivo, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

    print(f"Archivo '{path_archivo}' modificado con éxito.")

def main():
    parser = argparse.ArgumentParser(description="CLI para manejar archivos Markdown")

    # Subcomandos
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Comando "version"
    subparsers.add_parser("version", help="Muestra la versión del programa")

    # Comando "hola"
    parser_hola = subparsers.add_parser("hola", help="Saluda a una persona")
    parser_hola.add_argument("--nombre", type=str, default="Joe Doe", help="Nombre de la persona a saludar")

    # Comando "basico"
    parser_basico = subparsers.add_parser("basico", help="Agrega frontmatter a un archivo Markdown")
    parser_basico.add_argument("-a", "--agregar", type=str, required=True, help="Ruta del archivo Markdown a modificar")
    parser_basico.add_argument("-d", "--description", type=str, help="Descripción personalizada para el frontmatter")

    # Parsear argumentos
    args = parser.parse_args()

    if args.comando == "version":
        print(VERSION)
    elif args.comando == "hola":
        hola_mundo(args.nombre)
    elif args.comando == "basico":
        procesar_basico(args.agregar, args.description)

if __name__ == "__main__":
    main()
