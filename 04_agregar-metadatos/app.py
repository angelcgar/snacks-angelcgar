#!/usr/bin/env python3
"""
Blog Post Metadata Manager
Herramienta CLI para gestionar frontmatter de posts en formato Markdown.
"""

import argparse
import os
import sys
import unicodedata
from datetime import datetime, UTC
from pathlib import Path

# Constantes
VERSION = "1.0.0"
AUTHOR = "Angel Contreras Garcia"
# Ruta de destino para guardar archivos procesados
DESTINATION_DIR = Path.home() / "Dev" / "blog-angelcgar" / "src" / "data" / "blog"


def slugify(text: str) -> str:
    """
    Convierte un texto en un slug legible para URLs.

    Args:
        text: Texto a convertir en slug

    Returns:
        String con formato slug (minúsculas, sin acentos, guiones en lugar de espacios)
    """
    # Preservar la ñ temporalmente
    text = text.replace("ñ", "__enie__")

    # Normalizar y eliminar acentos
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Restaurar la ñ
    text = text.replace("__enie__", "ñ")

    # Limpiar caracteres especiales y formatear
    text = text.replace("?", "").replace("¿", "")
    text = text.strip().lower()
    text = text.replace(" ", "-")

    return text

def get_iso_timestamp() -> str:
    """
    Obtiene la fecha y hora actual en formato ISO 8601 con UTC.

    Returns:
        String con formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
    """
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def add_frontmatter(file_path: str, description: str | None = None, rename: bool = False, save: bool = False) -> None:
    """
    Agrega frontmatter a un archivo Markdown.

    Args:
        file_path: Ruta del archivo a procesar
        description: Descripción personalizada para el frontmatter
        rename: Si True, renombra el archivo usando el slug generado
        save: Si True, guarda el archivo en el directorio de destino
    """
    # Leer archivo
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: el archivo '{file_path}' no existe.")
        sys.exit(1)

    # Validaciones
    if not lines:
        print("❌ Error: el archivo está vacío.")
        sys.exit(1)

    if lines[0].startswith("---"):
        print("❌ Error: el archivo ya contiene frontmatter.")
        sys.exit(1)

    if not lines[0].startswith("#"):
        print("❌ Error: la primera línea debe ser un título principal '#'.")
        sys.exit(1)

    # Extraer título y generar slug
    title = lines[0].lstrip("#").strip()
    slug = slugify(title)

    # Descripción por defecto
    default_description = "Post del blog personal de Angel Contreras Garcia."

    # Crear frontmatter
    frontmatter = f"""---
author: {AUTHOR}
pubDatetime: {get_iso_timestamp()}
modDatetime: {get_iso_timestamp()}
title: {title}
slug: {slug}
featured: true
draft: false
tags:
  - blog
description: {description if description else default_description}
---
"""

    new_content = frontmatter + "".join(lines[1:])

    # Determinar ruta final del archivo
    base_dir = Path(file_path).parent
    final_filename = f"{slug}.md"

    if save:
        # Guardar en directorio de destino
        DESTINATION_DIR.mkdir(parents=True, exist_ok=True)
        final_path = DESTINATION_DIR / final_filename
        if final_path.exists():
            print(f"⚠️  Error: ya existe un archivo en destino: '{final_path}'")
            sys.exit(1)
    elif rename:
        # Renombrar en el mismo directorio
        final_path = base_dir / final_filename
        if final_path.exists():
            print(f"⚠️  Error: ya existe un archivo con el nombre '{final_path}'")
            sys.exit(1)
        # Renombrar el archivo original
        Path(file_path).rename(final_path)
    else:
        # Sobrescribir archivo original
        final_path = Path(file_path)

    # Escribir contenido
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Archivo procesado: '{final_path}'")

def move_to_destination(file_path: str) -> None:
    """
    Mueve un archivo al directorio de destino sin modificarlo.

    Args:
        file_path: Ruta del archivo a mover
    """
    DESTINATION_DIR.mkdir(parents=True, exist_ok=True)

    source = Path(file_path)
    destination = DESTINATION_DIR / source.name

    if not source.exists():
        print(f"❌ Error: el archivo '{file_path}' no existe.")
        sys.exit(1)

    if destination.exists():
        print(f"⚠️  Error: ya existe un archivo en destino: '{destination}'")
        sys.exit(1)

    source.rename(destination)
    print(f"✅ Archivo movido a: '{destination}'")

def update_modification_date(file_path: str) -> None:
    """
    Actualiza la fecha de modificación (modDatetime) en el frontmatter.

    Args:
        file_path: Ruta del archivo a actualizar
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: el archivo '{file_path}' no existe.")
        sys.exit(1)

    # Validar que existe frontmatter
    if not lines or not lines[0].startswith("---"):
        print("❌ Error: el archivo no contiene frontmatter.")
        sys.exit(1)

    # Encontrar el final del frontmatter
    frontmatter_end_index = -1
    for i, line in enumerate(lines[1:], 1):
        if line.startswith("---"):
            frontmatter_end_index = i
            break

    if frontmatter_end_index == -1:
        print("❌ Error: el frontmatter no está bien formado.")
        sys.exit(1)

    # Buscar y actualizar modDatetime
    mod_datetime_found = False
    for i in range(1, frontmatter_end_index):
        if lines[i].startswith("modDatetime:"):
            lines[i] = f"modDatetime: {get_iso_timestamp()}\n"
            mod_datetime_found = True
            break

    if not mod_datetime_found:
        print("❌ Error: no se encontró 'modDatetime' en el frontmatter.")
        sys.exit(1)

    # Escribir cambios
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Fecha de modificación actualizada: '{file_path}'")

def main() -> None:
    """Punto de entrada principal de la aplicación."""
    parser = argparse.ArgumentParser(
        description="Blog Post Metadata Manager - Gestiona frontmatter de posts en Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Subcomandos
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Comandos disponibles"
    )

    # Comando "version"
    subparsers.add_parser(
        "version",
        help="Muestra la versión del programa"
    )

    # Comando "add" (antes "basico")
    parser_add = subparsers.add_parser(
        "add",
        help="Agrega frontmatter a un archivo Markdown"
    )
    parser_add.add_argument(
        "-f",
        "--file",
        help="Archivo Markdown a procesar",
        metavar="FILE.md",
        type=str,
        required=True,
    )
    parser_add.add_argument(
        "-d",
        "--description",
        help="Descripción personalizada para el frontmatter",
        metavar="DESCRIPTION",
        default=None,
        type=str,
    )
    parser_add.add_argument(
        "--rename",
        action="store_true",
        help="Renombrar el archivo usando el slug generado"
    )
    parser_add.add_argument(
        "--save",
        action="store_true",
        help=f"Guardar el archivo en el directorio de destino ({DESTINATION_DIR})"
    )

    # Comando "move" (antes "guardar")
    parser_move = subparsers.add_parser(
        "move",
        help=f"Mueve un archivo directamente al directorio de destino ({DESTINATION_DIR})"
    )
    parser_move.add_argument(
        "file",
        type=str,
        help="Ruta del archivo a mover"
    )

    # Comando "update" (antes "actualizar")
    parser_update = subparsers.add_parser(
        "update",
        help="Actualiza la fecha de modificación (modDatetime) en el frontmatter"
    )
    parser_update.add_argument(
        "file",
        type=str,
        help="Ruta del archivo a actualizar"
    )

    args = parser.parse_args()

    # Ejecutar comando
    if args.command == "version":
        print(f"Blog Post Metadata Manager v{VERSION}")
    elif args.command == "add":
        add_frontmatter(args.file, args.description, args.rename, args.save)
    elif args.command == "move":
        move_to_destination(args.file)
    elif args.command == "update":
        update_modification_date(args.file)

if __name__ == "__main__":
    main()
