#!/usr/bin/env python3

import os
import json
import subprocess
import argparse
from pathlib import Path
from enum import Enum

HOME_USER = os.path.expanduser("~")
BIBLIOTECA_JSON = os.path.join(HOME_USER, ".config", "biblioteca_cli_config", "biblioteca_cli.json")
CONFIG_FILE_PATH = os.path.join(HOME_USER, ".config", "biblioteca_cli_config", "biblioteca_cli_config.json")

class EstadoLibro(Enum):
    LEIDO = "leido"
    LEYENDO = "leyendo"
    NO_LEIDO = "no leido"

class Prioridad(Enum):
    IMPORTANTE = "importante"
    MEDIA = "media"
    BAJA = "baja"

class Libro:
    # Crear un id para cada libro
    def __init__(self, titulo: str, autor: str, genero: str, anio_publicacion: str, path_absoluto: str, idioma: str, estado: EstadoLibro, descripcion: str, lo_leo_por: str, prioridad: Prioridad):
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._anio_publicacion = anio_publicacion
        self._path_absoluto = path_absoluto
        self._idioma = idioma
        self._estado = estado
        self._descripcion = descripcion
        self._lo_leo_por = lo_leo_por
        self._prioridad = prioridad

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

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def prioridad(self):
        return self._prioridad


    def convertir_a_dict(self) -> dict[str, str]:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "anio_publicacion": self.anio_publicacion,
            "idioma": self.idioma,
            "estado": self.estado.value,
            "abspath": self._path_absoluto,
            "descripcion": self.descripcion,
            "lo_leo_por": self._lo_leo_por,
            "prioridad": self.prioridad.value
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

    def mostrar_todos_los_libros_disponibles(self):
        print(f'Libros disponibles en la biblioteca {self._nombre}'.center(70, "="))
        for libro in self._libros:
            self.mostrar_libros(libro)

    def mostrar_todos_los_libros_no_leidos(self):
        print(f'Libros disponibles en la biblioteca {self._nombre}'.center(70, "="))
        for libro in self._libros:
            if libro.get("estado") == EstadoLibro.NO_LEIDO.value:
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

def cargar_configuracion() -> dict[str, str]:
    with open(CONFIG_FILE_PATH, "r", encoding='utf-8') as archivo:
        datos = json.load(archivo)

    return {
        "version": datos['version'],
    }

BIBLIOTECA_PRINCIPAL = Biblioteca("biblioteca_inicial")

def agregar_libro(file: str | None = None, titulo: str | None = None, autor: str | None = None, genero: str | None = None, anio_publicacion: str | None = None, idioma: str | None = None, estado: EstadoLibro | None = None, descripcion: str | None = None, lo_leo_por: str | None = None, prioridad: Prioridad | None = None):
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
        estado = EstadoLibro.NO_LEIDO
    else:
        try:
            estado = EstadoLibro(estado.value.lower())
        except ValueError:
            print(f"Error: El estado del libro debe ser uno de los siguientes: {', '.join([e.value for e in EstadoLibro])}")
            return

    if descripcion is None:
        descripcion = "Libro sin descripción"

    if lo_leo_por is None:
        lo_leo_por = "Interés personal"

    if prioridad is None:
        prioridad = Prioridad.BAJA
    else:
        try:
            prioridad = Prioridad(prioridad.value.lower())
        except ValueError:
            print(f"Error: La prioridad del libro debe ser una de los siguientes: {', '.join([p.value for p in Prioridad])}")
            return

    if file:
        if titulo is None:
            titulo = file[:-4]

        titulo = titulo.strip().lower().replace(" ", "_")

        current_path = str(Path.cwd())
        path_libro = os.path.join(current_path, file)

        current_libro = Libro(titulo=titulo, autor=autor, genero=genero, anio_publicacion=anio_publicacion, path_absoluto=path_libro, idioma=idioma, estado=estado, descripcion=descripcion, lo_leo_por=lo_leo_por, prioridad=prioridad)
        BIBLIOTECA_PRINCIPAL.guardar_libro(current_libro.convertir_a_dict())

def abrir_libro(libro: str):
    if libro:
        current_libro = BIBLIOTECA_PRINCIPAL.buscar_libros_por_titulo(libro)
        if not current_libro:
            print(f"No se encontró el libro: {libro}")

        subprocess.run(["zathura", str(current_libro)], check=True)

def listar_libros(autor: str | None = None, genero: str | None = None, estado: str | None = None, prioridad: str | None = None, ordenar_por_prioridad: bool = False):
    """
    Lista los libros de la biblioteca.
    - Por defecto, lista todos los libros disponibles.
    - Permite filtrar por autor, género o estado.
    """
    libros = BIBLIOTECA_PRINCIPAL.cargar_libros()
    if not libros:
        print("No hay libros en la biblioteca.")
        return

    # Comportamiento por defecto: listar libros disponibles si no hay filtros
    if autor is None and genero is None and estado is None and prioridad is None:
        BIBLIOTECA_PRINCIPAL.mostrar_todos_los_libros_disponibles()
        return

    # Aplicar filtros si se proporcionan
    libros_a_mostrar = libros

    if autor:
        libros_a_mostrar = [libro for libro in libros_a_mostrar if libro.get("autor", "").lower() == autor.lower()]

    if genero:
        libros_a_mostrar = [libro for libro in libros_a_mostrar if libro.get("genero", "").lower() == genero.lower()]

    if estado:
        libros_a_mostrar = [libro for libro in libros_a_mostrar if libro.get("estado", "").lower() == estado.lower()]

    if prioridad:
        libros_a_mostrar = [libro for libro in libros_a_mostrar if libro.get("prioridad", "").lower() == prioridad.lower()]

    if ordenar_por_prioridad:
        prioridad_orden = {p.value: i for i, p in enumerate(Prioridad)}
        libros_a_mostrar = sorted(libros_a_mostrar, key=lambda x: prioridad_orden.get(x.get("prioridad"), len(prioridad_orden))) # type: ignore

    if not libros_a_mostrar:
        print("No se encontraron libros con los criterios especificados.")
    else:
        print(f"Resultados de la búsqueda".center(70, "="))
        for libro in libros_a_mostrar:
            BIBLIOTECA_PRINCIPAL.mostrar_libros(libro)

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

def modificar_libro(titulo_actual: str, nuevo_titulo: str | None = None, nuevo_autor: str | None = None, nuevo_genero: str | None = None, nuevo_anio: str | None = None, nuevo_idioma: str | None = None, nuevo_estado: str | None = None, nueva_descripcion: str | None = None, lo_leo_por: str | None = None, nueva_prioridad: str | None = None):
    """ Modifica los atributos de un libro existente. """
    libros = BIBLIOTECA_PRINCIPAL.cargar_libros()
    libro_encontrado = None
    libro_modificado = False

    for libro in libros:
        if libro["titulo"].lower() == titulo_actual.lower():
            libro_encontrado = libro
            print(f"Libro encontrado: '{libro['titulo']}'. Modificando atributos...")
            if nuevo_titulo:
                libro["titulo"] = nuevo_titulo
                libro_modificado = True
            if nuevo_autor:
                libro["autor"] = nuevo_autor
                libro_modificado = True
            if nuevo_anio:
                libro["anio_publicacion"] = nuevo_anio
                libro_modificado = True
            if nueva_descripcion:
                libro["descripcion"] = nueva_descripcion
                libro_modificado = True
            if nuevo_genero:
                libro["genero"] = nuevo_genero
                libro_modificado = True
            if nuevo_estado:
                try:
                    estado = EstadoLibro(nuevo_estado.lower())
                    libro["estado"] = estado.value
                    libro_modificado = True
                except ValueError:
                    print(f"Error: El estado del libro debe ser uno de los siguientes: {', '.join([e.value for e in EstadoLibro])}")
                    return
            if nueva_prioridad:
                try:
                    prioridad = Prioridad(nueva_prioridad.lower())
                    libro["prioridad"] = prioridad.value
                    libro_modificado = True
                except ValueError:
                    print(f"Error: La prioridad del libro debe ser una de las siguientes: {', '.join([p.value for p in Prioridad])}")
                    return
            break

    if not libro_encontrado:
        print(f"Error: No se encontró el libro con el título '{titulo_actual}'.")
        return

    if libro_modificado:
        BIBLIOTECA_PRINCIPAL.guardar_libros(libros)
        print(f"El libro '{titulo_actual}' ha sido modificado exitosamente.")
    else:
        print("No se especificó ningún atributo para modificar.")

def mostrar_version():
    """ Muestra la versión del CLI. """
    version_actual = cargar_configuracion()['version']
    print(f"Versión del CLI: {version_actual}")

def mostrar_info_libro(titulo: str):
    """ Muestra la información detallada de un libro. """
    libros = BIBLIOTECA_PRINCIPAL.cargar_libros()
    libro_encontrado = None
    for libro in libros:
        if libro["titulo"].lower() == titulo.lower():
            libro_encontrado = libro
            break

    if libro_encontrado:
        print(f"Información de '{libro_encontrado['titulo']}'".center(70, '='))
        print(f"- Título: {libro_encontrado['titulo']}")
        print(f"- Autor: {libro_encontrado['autor']}")
        print(f"- Género: {libro_encontrado['genero']}")
        print(f"- Año de publicación: {libro_encontrado['anio_publicacion']}")
        print(f"- Idioma: {libro_encontrado['idioma']}")
        print(f"- Estado: {libro_encontrado['estado']}")
        print(f"- Prioridad: {libro_encontrado.get('prioridad', 'No especificada')}")
        print(f"- Path: {libro_encontrado['abspath']}")
        print(f"- Descripción: {libro_encontrado['descripcion']}")
        print(f"- Lo leo por: {libro_encontrado['lo_leo_por']}")
    else:
        print(f"Error: No se encontró el libro con el título '{titulo}'.")


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
        '-f', '--file',
        help='Dirección relativa para el libro (ej: nombre_del_libro.pdf)',
        metavar='ARCHIVO',
        default=None,
        type=str,
        nargs='?'  # Permite que el argumento sea opcional
    )
    agregar_parser.add_argument(
        '-t', '--titulo',
        help='Identificador único para cada libro (ej: nombre_del_libro)',
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
    agregar_parser.add_argument(
        '--lo_leo_por',
        help='Espacio para determinar el por que leo este libro',
        metavar='LO_LEO_POR',
        default=None,
        nargs='?',
        type=str
    )
    agregar_parser.add_argument(
        '--descripcion',
        help='Descripción del libro',
        metavar='DESCRIPCION',
        default=None,
        nargs='?',
        type=str
    )
    agregar_parser.add_argument(
        '-p', '--prioridad',
        help='Prioridad del libro (alta, media, baja)',
        metavar='PRIORIDAD',
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
    listar_parser = subparsers.add_parser(
        "listar",
        help='Lista todos los libros en la biblioteca, con filtros opcionales.',
        description='Lista todos los libros. Por defecto, muestra los disponibles. Permite filtrar por autor, género o estado.'
    )
    listar_parser.add_argument(
        '-a', '--autor',
        help='Filtra los libros por autor',
        metavar='AUTOR',
        default=None,
        type=str
    )
    listar_parser.add_argument(
        '-g', '--genero',
        help='Filtra los libros por género',
        metavar='GENERO',
        default=None,
        type=str
    )
    listar_parser.add_argument(
        '-e', '--estado',
        help='Filtra los libros por estado (ej: disponible, prestado)',
        metavar='ESTADO',
        default=None,
        type=str
    )
    listar_parser.add_argument(
        '-p', '--prioridad',
        help='Filtra los libros por prioridad',
        metavar='PRIORIDAD',
        default=None,
        type=str
    )
    listar_parser.add_argument(
        '--ordenar_por_prioridad',
        help='Ordena los libros por prioridad (ascendente)',
        action='store_true'
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

     # Comando para modificar un libro existente
    modificar_parser = subparsers.add_parser(
        "modificar",
        help='Modifica un libro existente en la biblioteca',
        description='Modifica los atributos de un libro existente'
    )
    modificar_parser.add_argument(
        'titulo',
        help='Título actual del libro a modificar',
        metavar='TITULO_ACTUAL',
        type=str
    )
    modificar_parser.add_argument(
        '-n', '--nombre',
        help='Nuevo título para el libro',
        metavar='NUEVO_NOMBRE',
        default=None,
        type=str
    )
    modificar_parser.add_argument(
        '-a', '--autor',
        help='Nuevo autor del libro',
        metavar='NUEVO_AUTOR',
        default=None,
        type=str
    )
    modificar_parser.add_argument(
        '-y', '--anio_publicacion',
        help='Nuevo año de publicación del libro',
        metavar='NUEVO_AÑO',
        default=None,
        type=str
    )
    modificar_parser.add_argument(
        '-i', '--idioma',
        help='Cambiar el idioma del libro',
        metavar='IDIOMA',
        default=None,
        type=str
    )
    modificar_parser.add_argument(
        '-g', '--genero',
        help='Nuevo genero para el libro',
        metavar='GENERO',
        default=None,
        type=str
    )
    modificar_parser.add_argument(
        '--descripcion',
        help='Nueva descripción para el libro',
        metavar='DESCRIPCION',
        default=None,
        type=str
    )
    modificar_parser.add_argument(
        '--lo_leo_por',
        help='Nuevo argumento del por que estoy leyendo este libro',
        metavar='LO LEO POR',
        default=None,
        type=str
    )

    modificar_parser.add_argument(
        '-e', '--estado',
        help='Nuevo estado para el libro',
        metavar='ESTADO',
        default=None,
        type=str
    )

    modificar_parser.add_argument(
        '-p', '--prioridad',
        help='Nueva prioridad para el libro',
        metavar='PRIORIDAD',
        default=None,
        type=str
    )

    # Comando para mostrar informacion de un libro
    info_parser = subparsers.add_parser(
        "info",
        help='Muestra la información detallada de un libro',
        description='Muestra toda la información de un libro específico'
    )
    info_parser.add_argument(
        'titulo',
        help='Título del libro a mostrar',
        metavar='TITULO',
        type=str
    )

    args = parser.parse_args()

    if args.comando == "agregar":
        agregar_libro(args.file, args.titulo, args.autor, args.genero, args.anio_publicacion, args.idioma, args.estado, args.descripcion, args.lo_leo_por, args.prioridad)
    elif args.comando == "leer":
        abrir_libro(args.libro)
    elif args.comando == "listar":
        listar_libros(args.autor, args.genero, args.estado, args.prioridad, args.ordenar_por_prioridad)
    elif args.comando == "eliminar":
        eliminar_libro(args.libro)
    elif args.comando == "modificar":
        modificar_libro(args.titulo, args.nombre, args.autor, args.genero, args.anio_publicacion, args.idioma, args.estado, args.descripcion, args.lo_leo_por, args.prioridad)
    elif args.comando == "info":
        mostrar_info_libro(args.titulo)
    elif args.comando == "version":
        mostrar_version()
    elif args.comando is None:
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
