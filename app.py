#!/usr/bin/env python3

import os
import argparse
from datetime import datetime
import getpass

# Configuración
user = getpass.getuser()
BITACORAS_DIR = os.path.join(os.path.expanduser("~"), "bitacoras_diarias")
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "bitacoras_diarias")
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

def cargar_plantillas() -> dict[str, str]:
    """Carga las plantillas desde el directorio de configuración"""
    plantillas: dict[str, str] = {
        "default": DEFAULT_TEMPLATE
    }

    if os.path.exists(CONFIG_DIR):
        for file in os.listdir(CONFIG_DIR):
            if file.endswith(".md"):
                name = os.path.splitext(file)[0]
                with open(os.path.join(CONFIG_DIR, file), 'r') as f:
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

def listar_plantillas(valor: str | None = None):
    """Muestra las plantillas disponibles"""
    plantillas = cargar_plantillas()
    if valor:
        print("Parámetro 'valor' no implementado en esta versión.")
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
        metavar='NOMBRE'
    )
    crear_parser.add_argument('-p', '--plantilla',
        help='Plantilla a usar',
        choices=list(plantillas.keys()),
        default='default'
    )

    # Comando para listar bitácoras
    listar_parser = subparsers.add_parser(
        'listar',
        help='Muestra el listado de bitácoras',
        description='Enumera todas las bitácoras existentes con su fecha de creación'
    )
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
        '-n', '--nombre',
        action='store_true',
        help='Muestra detalles adicionales de las plantillas'
    )

    args = parser.parse_args()

    if args.comando == 'crear':
        # print("Creando bitácora...")
        crear_bitacora(args.nombre, args.plantilla)
    elif args.comando == 'listar':
        listar_bitacoras()
    elif args.comando == 'plantillas':
        listar_plantillas(args.nombre)
    elif args.comando is None:
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
