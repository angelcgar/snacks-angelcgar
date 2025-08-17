#!/usr/bin/env python3
import argparse
import sys
import unicodedata
import os
from datetime import datetime, UTC

# Constantes
VERSION = "0.0.2"
AUTHOR = "Sat Naing"
DESTINO = os.path.expanduser("~/Descargas/md_con_formatos/")

def hola_mundo(nombre):
    print(f"hola \"{nombre}\"")

def slugify(texto: str) -> str:
    """
    Convierte un texto en un slug legible para URLs.
    - Elimina acentos.
    - Mantiene la ñ y caracteres como ¿?.
    - Convierte espacios en guiones.
    - Pone todo en minúsculas.
    """
    texto = texto.replace("ñ", "__enie__")
    texto = texto.replace("¿", "__interrogacion__")

    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    texto = texto.replace("__enie__", "ñ")
    texto = texto.replace("__interrogacion__", "¿")
    texto = texto.strip().lower()
    texto = texto.replace(" ", "-")
    return texto

def procesar_basico(path_archivo, description=None, renombrar=False, guardar=False):
    try:
        with open(path_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: el archivo '{path_archivo}' no existe.")
        sys.exit(1)

    if not lineas:
        print("Error: el archivo está vacío.")
        sys.exit(1)

    if lineas[0].startswith("---"):
        print("Error: no se puede modificar este archivo (ya contiene frontmatter).")
        sys.exit(1)

    if not lineas[0].startswith("#"):
        print("Error: la primera línea no es un título principal '#'.")
        sys.exit(1)

    # Extraer título
    titulo = lineas[0].lstrip("#").strip()
    slug = slugify(titulo)

    ahora = datetime.now(UTC).isoformat()

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

    nuevo_contenido = frontmatter + "".join(lineas[1:])

    # Lógica de guardado
    base_dir = os.path.dirname(path_archivo) or "."
    nombre_final = f"{slug}.md"

    if guardar:
        os.makedirs(DESTINO, exist_ok=True)
        destino_path = os.path.join(DESTINO, nombre_final)
        if os.path.exists(destino_path):
            print(f"⚠️ Error: ya existe un archivo en destino con el nombre '{destino_path}'.")
            sys.exit(1)
        nuevo_nombre = destino_path
    elif renombrar:
        destino_path = os.path.join(base_dir, nombre_final)
        if os.path.exists(destino_path):
            print(f"⚠️ Error: ya existe un archivo en origen con el nombre '{destino_path}'.")
            sys.exit(1)
        os.rename(path_archivo, destino_path)
        nuevo_nombre = destino_path
    else:
        nuevo_nombre = path_archivo

    # Guardar contenido
    with open(nuevo_nombre, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

    print(f"✅ Archivo '{nuevo_nombre}' modificado con éxito.")

def main():
    parser = argparse.ArgumentParser(
        prog="app.py",
        description="CLI para manejar archivos Markdown"
    )

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
    parser_basico.add_argument("--renombrar", action="store_true", help="Renombrar el archivo usando el slug generado")
    parser_basico.add_argument("--guardar", action="store_true", help=f"Guardar el archivo en {DESTINO}")

    args = parser.parse_args()

    if args.comando == "version":
        print(VERSION)
    elif args.comando == "hola":
        hola_mundo(args.nombre)
    elif args.comando == "basico":
        procesar_basico(args.agregar, args.description, args.renombrar, args.guardar)

if __name__ == "__main__":
    main()
