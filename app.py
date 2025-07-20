#!/usr/bin/env python3

import os
import json
import subprocess
import argparse
from pathlib import Path

HOME_USER = os.path.expanduser("~")
BIBLIOTECA_JSON = os.path.join(HOME_USER, ".config", "biblioteca_cli_config", "biblioteca_cli.json")
CONFIG_FILE_PATH = os.path.join(HOME_USER, ".config", "biblioteca_cli_config", "biblioteca_cli_config.json")

class Libro:
    # Crear un id para cada libro
    def __init__(self, titulo: str, autor: str, genero: str, path_absoluto: str):
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._path_absoluto = path_absoluto

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def genero(self):
        return self._genero

    def convertir_a_dict(self) -> dict[str, str]:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "abspath": self._path_absoluto,
        }

class Biblioteca:

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._libros: list[dict[str, str]] = self.cargar_libros()

    def agregar_libro(self, libro: dict[str, str]):
        self._libros.append(libro)

    # def buscar_libros_por_autor(self, autor):
    #     for libro in self._libros:
    #         if libro.autor.lower() == autor.lower():
    #             self.mostrar_libro(libro)

    # def buscar_libros_por_genero(self, genero):
    #     for libro in self._libros:
    #         if libro.genero.lower() == genero.lower():
    #             self.mostrar_libro(libro)

    def buscar_libros_por_titulo(self, titulo) -> str | None:
        for libro in self._libros:
            if libro["titulo"].lower() == titulo.lower():
                return libro["abspath"]

    def mostrar_todos_los_libros(self):
        print(f'Todos los libros de la biblioteca {self._nombre}'.center(70, "="))
        # Bug: Hay un None en la lista de libros
        for libro in self._libros:
            self.mostrar_libros(libro)

    def mostrar_libros(self, libro: dict[str, str]):
        print(f'Libro -> Título: {libro["titulo"]}, Autor: {libro["autor"]}, '
              f'Género: {libro["genero"]}')

    # Lógica de la app
    def cargar_libros(self) -> list[dict[str, str]]:
        with open(BIBLIOTECA_JSON, "r", encoding='utf-8') as f:
            return json.load(f)

    def guardar_libros(self, libros: list[dict[str, str]]):
        with open(BIBLIOTECA_JSON, "w", encoding='utf-8') as f:
            json.dump(libros, f, indent=4, ensure_ascii=False)

    def guardar_libro(self, libro: dict[str, str]):
        libros = self.cargar_libros()
        print(libros)
        libros.append(libro)
        self.guardar_libros(libros)


    @property
    def nombre(self):
        return self._nombre

    @property
    def libros(self):
        return self._libros

BIBLIOTECA_PRINCIPAL = Biblioteca("biblioteca_inicial")

def agregar_libro(libro: str | None = None, autor: str = "Joe Doe", genero: str = "Programming"):

    if libro:
        normalized_book_name = libro.strip().lower().split(".")[-2].replace(" ", "_")
        current_path = str(Path.cwd())
        path_libro = os.path.join(current_path, libro)

        current_libro = Libro(normalized_book_name, autor, genero, path_libro)
        BIBLIOTECA_PRINCIPAL.guardar_libro(current_libro.convertir_a_dict())

def abrir_libro(libro: str):
    if libro:
        current_libro = BIBLIOTECA_PRINCIPAL.buscar_libros_por_titulo(libro)
        if not current_libro:
            print(f"No se encontro el libro: {libro}")

        subprocess.run(["zathura", current_libro], check=True) # type: ignore


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
