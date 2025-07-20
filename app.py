#!/usr/bin/env python3

import subprocess
import argparse
from pathlib import Path

def agregar_libro(libro: str | None = None):

    if libro:
        tem_libro_nombre = libro.strip().lower().split(".")[-2]
        current_path = str(Path.cwd())
        path_libro = current_path + "/" + libro
        print("path_libro",path_libro)
        subprocess.run(["zathura", path_libro])
        print(tem_libro_nombre)

def main():
    parser = argparse.ArgumentParser(
        description='Biblioteca CLI - Sistema para gestionar libros desde la Terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos de uso:
        %(prog)s leer alias-archivo     Abre el archivo pdf con su lector preferido"""
    )

    subparsers = parser.add_subparsers(
        title='comandos',
        dest='comando',
        description='Operaciones disponibles',
        metavar='COMANDO'
    )

    # Comando para agregar un nuevo libro
    agregar_parser = subparsers.add_parser(
        "agregar",
        help='Agrega un nuevo libro',
        description='Agrega un nuevo libro a tu biblioteca'
    )
    agregar_parser.add_argument(
        '-n', '--nombre',
        help='Identificador opcional para la bitácora (ej: nombre_proyecto)',
        metavar='NOMBRE',
        default=None,
        type=str,
        nargs='?'  # Permite que el argumento sea opcional
    )

    args = parser.parse_args()

    if args.comando == "agregar":
        agregar_libro(args.nombre)
    elif args.comando == "version":
        print("0.0.1")
    elif args.comando is None:
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
