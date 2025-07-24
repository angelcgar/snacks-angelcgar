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
    def __init__(self, titulo: str, autor: str, genero: str, anio_publicacion: str, path_absoluto: str, idioma: str, estado: str):
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._anio_publicacion = anio_publicacion
        self._path_absoluto = path_absoluto
        self._idioma = idioma
        self._estado = estado

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def genero(self):
        return self._genero

    @property
    def anio_publicacion(self):
        return self._anio_publicacion

    @property
    def idioma(self):
        return self._idioma

    @property
    def estado(self):
        return self._estado


    def convertir_a_dict(self) -> dict[str, str]:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "anio_publicacion": self.anio_publicacion,
            "idioma": self.idioma,
            "estado": self.estado,
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

    def buscar_libros_por_titulo(self, titulo: str) -> str | None:
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
        # print(libros)
        libros.append(libro)
        self.guardar_libros(libros)

    @property
    def nombre(self):
        return self._nombre

    @property
    def libros(self):
        return self._libros

BIBLIOTECA_PRINCIPAL = Biblioteca("biblioteca_inicial")

def agregar_libro(libro: str | None = None, autor: str | None = None, genero: str | None = None, anio_publicacion: str | None = None, idioma: str | None = None, estado: str | None = None):
    """ Agrega un libro a la biblioteca."""
    if anio_publicacion is None:
        anio_publicacion = "2023"

    if genero is None:
        genero = "Programming"

    if autor is None:
        autor = "Joe Doe"

    if idioma is None:
        idioma = "es"

    if estado is None:
        estado = "disponible"

    if libro:
        normalized_book_name = libro.strip().lower()[:-4].replace(" ", "_")
        current_path = str(Path.cwd())
        path_libro = os.path.join(current_path, libro)

        current_libro = Libro(titulo=normalized_book_name, autor=autor, genero=genero, anio_publicacion=anio_publicacion, path_absoluto=path_libro, idioma=idioma, estado=estado)
        BIBLIOTECA_PRINCIPAL.guardar_libro(current_libro.convertir_a_dict())

def abrir_libro(libro: str):
    if libro:
        current_libro = BIBLIOTECA_PRINCIPAL.buscar_libros_por_titulo(libro)
        if not current_libro:
            print(f"No se encontró el libro: {libro}")

        subprocess.run(["zathura", current_libro], check=True) # type: ignore

def listar_libros():
    BIBLIOTECA_PRINCIPAL.mostrar_todos_los_libros()
    if not BIBLIOTECA_PRINCIPAL.libros:
        print("No hay libros en la biblioteca.")

def eliminar_libro(libro: str):
    if libro:
        current_libro = BIBLIOTECA_PRINCIPAL.buscar_libros_por_titulo(libro)
        if not current_libro:
            print(f"No se encontró el libro: {libro}")
            return

        # Eliminar el libro del archivo JSON
        libros = BIBLIOTECA_PRINCIPAL.cargar_libros()
        libros = [l for l in libros if l["titulo"].lower() != libro.lower()]
        BIBLIOTECA_PRINCIPAL.guardar_libros(libros)
        print(f"Libro '{libro}' eliminado de la biblioteca.")

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
        help='Identificador para cada libro (ej: nombre_del_libro.pdf)',
        metavar='NOMBRE',
        default=None,
        type=str,
        nargs='?'  # Permite que el argumento sea opcional
    )
    agregar_parser.add_argument(
        '-a', '--autor',
        help='Autor del libro (por defecto: Joe Doe)',
        metavar='AUTOR',
        default=None,
        nargs='?',
        type=str
    )
    agregar_parser.add_argument(
        '-g', '--genero',
        help='Género del libro (por defecto: Programming)',
        metavar='GENERO',
        default=None,
        nargs='?',
        type=str
    )
    agregar_parser.add_argument(
        '-y', '--anio_publicacion',
        help='Año de publicación del libro (por defecto: 2023)',
        metavar='AÑO_PUBLICACION',
        default=None,
        nargs='?',
        type=str
    )
    agregar_parser.add_argument(
        '-i', '--idioma',
        help='Idioma del libro (por defecto: es)',
        metavar='IDIOMA',
        default=None,
        nargs='?',
        type=str
    )
    agregar_parser.add_argument(
        '-e', '--estado',
        help='Estado del libro (por defecto: disponible)',
        metavar='ESTADO',
        default=None,
        nargs='?',
        type=str
    )

    # Comando para mostrar la versión
    version_parser = subparsers.add_parser(
        "version",
        help='Muestra la versión del CLI',
        description='Muestra la versión actual del CLI'
    )

    # Comando para abrir un libro
    leer_parser = subparsers.add_parser(
        "leer",
        help='Abre un libro con el lector predeterminado',
        description='Abre un libro con el lector predeterminado'
    )
    leer_parser.add_argument(
        'libro',
        help='Nombre del libro a abrir (debe estar en la biblioteca)',
        metavar='LIBRO',
        type=str
    )

    # Comando para listar todos los libros
    # todo: añadir un filtro por autor o género
    listar_parser = subparsers.add_parser(
        "listar",
        help='Lista todos los libros en la biblioteca',
        description='Lista todos los libros en la biblioteca'
    )

    # Comando para eliminar un libro
    eliminar_parser = subparsers.add_parser(
        "eliminar",
        help='Elimina un libro de la biblioteca',
        description='Elimina un libro de la biblioteca'
    )
    eliminar_parser.add_argument(
        'libro',
        help='Nombre del libro a eliminar (debe estar en la biblioteca)',
        metavar='LIBRO',
        type=str
    )

    args = parser.parse_args()

    if args.comando == "agregar":
        agregar_libro(args.nombre, args.autor, args.genero, args.anio_publicacion, args.idioma, args.estado)
    elif args.comando == "leer":
        abrir_libro(args.libro)
    elif args.comando == "listar":
        listar_libros()
    elif args.comando == "eliminar":
        eliminar_libro(args.libro)
    elif args.comando == "version":
        print("0.0.2")
    elif args.comando is None:
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
