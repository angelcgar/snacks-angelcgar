#!/usr/bin/env python3

import os
import argparse
from datetime import datetime
import getpass
import json

# Configuración
HOME_USER = os.path.expanduser("~")
SYSTEM_USER = getpass.getuser()
BITACORAS_DIR = os.path.join(HOME_USER, "bitacoras_diarias")
CONFIG_FILE_PATH = os.path.join(HOME_USER, ".config", "bitacora_cli_config", "bitacora_cli_config.json")

DEFAULT_TEMPLATE = """# Bitácora - {fecha}

## Objetivo
Describir el objetivo de esta sesión de trabajo.

## Tareas realizadas
- [ ] Tarea 1
- [ ] Tarea 2

## Problemas encontrados
- Ninguno por ahora

## Soluciones implementadas
- Ninguna por ahora

## Notas adicionales
- ...

## Próximos pasos
- [ ] Siguiente tarea 1
- [ ] Siguiente tarea 2
"""

def cargar_configuracion() -> dict[str, str]:
    with open(CONFIG_FILE_PATH, "r", encoding='utf-8') as archivo:
        datos = json.load(archivo)

    # print(datos['name'])
    return {
        "log_directory": datos['configuration']['paths']['log_directory'],
        "log_config_directory": datos['configuration']['paths']['log_config_directory'],
    }

def cargar_plantillas() -> dict[str, str]:
    """Carga las plantillas desde el directorio de configuración"""
    plantillas: dict[str, str] = {
        "default": DEFAULT_TEMPLATE
    }

    configuration_directory = cargar_configuracion()['log_config_directory']

    if os.path.exists(configuration_directory):
        for file in os.listdir(configuration_directory):
            if file.endswith(".md"):
                name = os.path.splitext(file)[0]
                with open(os.path.join(configuration_directory, file), 'r') as f:
                    plantillas[name] = f.read()

    return plantillas

def verificar_directorio():
    """Verifica si el directorio de bitácoras existe, si no, lo crea."""
    if not os.path.exists(BITACORAS_DIR):
        os.makedirs(BITACORAS_DIR)
        print(f"Directorio creado: {BITACORAS_DIR}")

def crear_bitacora(nombre: str | None = None, plantilla: str | None = None):
    """Crea una nueva bitácora con la plantilla predeterminada."""
    verificar_directorio()

    plantillas = cargar_plantillas()
    if plantilla is None:
        template = DEFAULT_TEMPLATE
    else:
        template = plantillas.get(plantilla.lower(), DEFAULT_TEMPLATE)

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    if nombre:
        nombre_archivo = f"bitacora_{nombre}_{fecha_actual}.md"
    else:
        nombre_archivo = f"bitacora_{fecha_actual}.md"

    ruta_completa = os.path.join(BITACORAS_DIR, nombre_archivo)

    if os.path.exists(ruta_completa):
        print(f"¡Advertencia: El archivo {nombre_archivo} ya existe!")
        return


    with open(ruta_completa, 'w') as f:
        f.write(template.format(fecha_actual=fecha_actual))

    print(f"Bitácora creada exitosamente: {ruta_completa}")

def listar_plantillas(show_details: str | None = None):
    """Muestra las plantillas disponibles"""
    plantillas = cargar_plantillas()

    configuration_directory = cargar_configuracion()['log_config_directory']

    if show_details:
        ruta_p = os.path.join(configuration_directory, show_details)
        if not ruta_p.endswith('.md'):
            ruta_p += '.md'

        with open(ruta_p, 'r') as f:
            print(f.read())

        return

    print("Plantillas disponibles".center(50, '-'))
    for name in plantillas.keys():
        print(f"  - {name}")

def listar_bitacoras():
    """Lista todas las bitácoras existentes en el directorio."""
    verificar_directorio()

    print("\nBitácoras disponibles:")
    bitacoras = [f for f in os.listdir(BITACORAS_DIR) if f.startswith('bitacora_') and f.endswith('.md')]

    if not bitacoras:
        print("No hay bitácoras existentes.")
        return

    for i, bitacora in enumerate(sorted(bitacoras), 1):
        print(f"{i}. {bitacora}")

def main():
    plantillas = cargar_plantillas()

    parser = argparse.ArgumentParser(
        description='Gestor de Bitácoras - Sistema para crear y administrar registros de actividades diarias',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos de uso:
        %(prog)s crear -n "proyecto_alpha"  Crea bitácora con nombre descriptivo
        %(prog)s crear                      Crea bitácora con fecha automática
        %(prog)s listar                     Muestra todas las bitácoras disponibles
        %(prog)s plantillas                 Muestra todas las plantillas disponibles

        Las bitácoras se guardan en: {}/""".format(BITACORAS_DIR)
    )

    subparsers = parser.add_subparsers(
        title='comandos',
        dest='comando',
        description='Operaciones disponibles',
        metavar='COMANDO'
    )

    # Comando para crear nueva bitácora
    crear_parser = subparsers.add_parser(
        'crear',
        help='Genera una nueva plantilla de bitácora',
        description='Crea un nuevo archivo de bitácora con estructura predefinida'
    )
    crear_parser.add_argument(
        '-n', '--nombre',
        help='Identificador opcional para la bitácora (ej: nombre_proyecto)',
        metavar='NOMBRE',
        default=None,
        type=str,
        nargs='?'  # Permite que el argumento sea opcional
    )
    crear_parser.add_argument(
        '-p', '--plantilla',
        help='Nombre de la plantilla a usar para la bitácora (default: "default")',
        metavar='PLANTILLA',
        choices=list(plantillas.keys()),
        default='default',
        type=str,
    )

    # Comando para listar bitácoras
    listar_parser = subparsers.add_parser(
        'listar',
        help='Muestra el listado de bitácoras',
        description='Enumera todas las bitácoras existentes con su fecha de creación'
    )
    # FIXME: Añadir argumento para mostrar detalles de las bitácoras
    listar_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra detalles adicionales de las bitácoras'
    )

    # Comando para listar plantillas
    plantillas_parser = subparsers.add_parser( # type: ignore
        'plantillas',
        help='Lista las plantillas disponibles',
        description='Muestra las plantillas de bitácoras que se pueden usar al crear nuevas bitácoras'
    )
    plantillas_parser.add_argument(
        '-s', '--show-details',
        help='Muestra detalles adicionales de las plantillas',
        choices=list(plantillas.keys()),
        default=None,
        type=str,
        nargs="?"
    )

    args = parser.parse_args()

    if args.comando == 'crear':
        crear_bitacora(args.nombre, args.plantilla)
    elif args.comando == 'listar':
        listar_bitacoras()
    elif args.comando == 'plantillas':
        listar_plantillas(args.show_details)
    elif args.comando is None:
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
