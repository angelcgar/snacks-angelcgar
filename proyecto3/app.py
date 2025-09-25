#!/usr/bin/env python3

import os
from pathlib import Path
import argparse
from datetime import datetime
import getpass
import json

# Configuración
HOME_USER = os.path.expanduser("~")
SYSTEM_USER = getpass.getuser()
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
        "work_space_directory": datos['configuration']['paths']['work_space_directory'],
        "log_config_directory": datos['configuration']['paths']['log_config_directory'],
        "log_config_file": datos['configuration']['paths']['log_config_file'],
        "user_executable_path": datos['configuration']['paths']['user_executable_path'],
        "user": datos['configuration']['user'],
        "name": datos['name'],
        "version": datos['version'],
        "date_format": datos['configuration']['dates']['date_format'],
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

def formatos_fechas() -> dict[str, str]:
    return {
        "default": "%Y-%m-%d",
        "iso": "%Y-%m-%d",             # 2025-07-19
        "latino": "%d-%m-%Y",          # 19-07-2025
        "mx": "%d-%m-%Y",
        "us": "%m-%d-%Y",              # 07-19-2025
        "completo": "%A, %d de %B de %Y", # sábado, 19 de julio de 2025
        "compacto": "%Y%m%d",          # 20250719
        "hora_fecha": "%Y-%m-%d %H:%M",# 2025-07-19 14:30
    }

def verificar_directorio():
    """Verifica si el directorio de bitácoras existe, si no, lo crea."""

    bitacoras_dir = cargar_configuracion()['log_directory']

    if not os.path.exists(bitacoras_dir):
        os.makedirs(bitacoras_dir)
        print(f"Directorio creado: {bitacoras_dir}")

def crear_bitacora(nombre: str | None = None, plantilla: str | None = None):
    """Crea una nueva bitácora con la plantilla predeterminada."""
    verificar_directorio()

    bitacoras_dir = cargar_configuracion()['log_directory']
    date_format = cargar_configuracion()['date_format']

    plantillas = cargar_plantillas()
    if plantilla is None:
        template = DEFAULT_TEMPLATE
    else:
        template = plantillas.get(plantilla.lower(), DEFAULT_TEMPLATE)

    fecha_actual = datetime.now().strftime(date_format)
    if nombre:
        nombre_archivo = f"{fecha_actual}_{nombre}.md"
    else:
        nombre_archivo = f"{fecha_actual}.md"

    ruta_completa = os.path.join(bitacoras_dir, nombre_archivo)

    if os.path.exists(ruta_completa):
        print(f"¡Advertencia: El archivo {nombre_archivo} ya existe!")
        return


    with open(ruta_completa, 'w') as f:
        f.write(template.format(fecha=fecha_actual))

    print(f"Bitácora creada exitosamente: {ruta_completa}")

    return str(ruta_completa)

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

    bitacoras_dir = cargar_configuracion()['log_directory']

    print("\nBitácoras disponibles:")
    bitacoras = [f for f in os.listdir(bitacoras_dir) if f.startswith('bitacora_') and f.endswith('.md')]

    if not bitacoras:
        print("No hay bitácoras existentes.")
        return

    for i, bitacora in enumerate(sorted(bitacoras), 1):
        print(f"{i}. {bitacora}")

def modificar_configuracion(path: str | None = None, date_format: str | None = None):
    """Modifica la configuración del sistema."""
    configuracion = cargar_configuracion()

    # Todo: Hacer validaciones robustas para date_format
    if date_format:
        print("Modificando el formato de fecha...")

        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        datos['configuration']['dates']['date_format'] = formatos_fechas()[date_format]

        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return

    # Todo: Mejorar la validación del path
    if path:
        if path == "this":
            # Directorio desde donde se ejecutó el comando
            ruta_ejecucion = Path.cwd()
            print(f"Directorio de trabajo actual: {ruta_ejecucion}")
            path = str(ruta_ejecucion)

        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        datos['configuration']['paths']['log_directory'] = path

        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        return

    # Mostrar la configuración actual
    print("Configuración actual:".center(50, '-'))
    print()
    for key, value in configuracion.items():
        print(f"{key}: {value}")

def crear_directorio():
    anio = datetime.now().year
    mes_nombre = datetime.now().strftime("%B").lower()
    mes_numero = datetime.now().strftime("%m")
    nombre_directorio = f"{str(anio)[2:]}-{mes_numero}-{mes_nombre}"

    print(f"Creando directorio para {nombre_directorio}...")

    if os.path.exists(nombre_directorio):
        print(f"El directorio '{nombre_directorio}' ya existe. No se creará uno nuevo.")
        return

    print(f"Directorio '{nombre_directorio}' no existe. Creando...")
    os.mkdir(nombre_directorio)

def formatear_archivo(archivo_md: str):
    current_file = crear_bitacora()

    if os.path.exists(str(current_file)):
        print(f"Archivo {current_file} creado correctamente.")

        try:
            with open(str(current_file), "r", encoding="utf-8") as f:
                lineas = f.readlines()
        except FileNotFoundError:
            print(f"Error: el archivo '{current_file}' no existe.")
            return

        # Extraer título
        titulo = lineas[0].strip()

        # Procesar contenido
        with open(archivo_md, 'r', encoding='utf-8') as f:
            archivo_md_contenido = f.read()
        nuevo_contenido = titulo + archivo_md_contenido

        with open(str(current_file), "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print(f"Archivo '{archivo_md}' formateado y guardado en '{current_file}'.")

def mostrar_version():
    """Muestra la versión del sistema."""
    configuracion = cargar_configuracion()
    print(f"{configuracion['name']} - Versión {configuracion['version']}")
    print(f"Usuario: {configuracion['user']}")
    print(f"Directorio de bitácoras: {configuracion['log_directory']}")
    print(f"Formato de fecha: {configuracion['date_format']}")

def fecha_actual():
    return datetime.now().strftime("%d-%m-%Y")

def crear_commit(message: str | None):
    current_log_directory = cargar_configuracion()['log_directory']
    work_space_directory = cargar_configuracion()['work_space_directory']

    current_directory_executable = Path.cwd()

    if (message is None):
        message = fecha_actual()

    if (current_directory_executable == current_log_directory or current_directory_executable == work_space_directory):
        import subprocess
        subprocess.run(["git", "add", ".", message], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)

def main():
    plantillas = cargar_plantillas()

    bitacoras_dir = cargar_configuracion()['log_directory']

    formatos_fecha = formatos_fechas()

    parser = argparse.ArgumentParser(
        description='Gestor de Bitácoras - Sistema para crear y administrar registros de actividades diarias',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos de uso:
        %(prog)s crear -n "proyecto_alpha"  Crea bitácora con nombre descriptivo
        %(prog)s crear                      Crea bitácora con fecha automática
        %(prog)s listar                     Muestra todas las bitácoras disponibles
        %(prog)s plantillas                 Muestra todas las plantillas disponibles

        Las bitácoras se guardan en: {}/""".format(bitacoras_dir)
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

    # Comando fuera de uso
    subparsers.add_parser(
        'cargar',
        help='Carga la configuracion',
        description='Carga la configuracion del sistema'
    )

    # Comando para manejar la configuración
    config_parser = subparsers.add_parser(
        'config',
        help='Muestra la configuración actual del sistema',
        description='Muestra la configuración actual del sistema'
    )
    config_parser.add_argument(
        '-p', '--path',
        help='Cambia el directorio en la configuración',
        choices=['this'] + [str],
        metavar='DIRECTORIO',
        type=str,
        default='this',
        nargs='?'
    )
    config_parser.add_argument(
        '-d', '--date_format',
        help='Cambia el formato de las fechas',
        choices=list(formatos_fecha.keys()),
        metavar='FORMATO_FECHA',
        default=None,
        type=str,
        nargs='?'
    )

    # Comando para crear un nuevo directorio
    subparsers.add_parser(
        'directorio',
        help='Crea un nuevo directorio',
        description='Crea un nuevo directorio llamado "carpeta_nueva" en el directorio actual'
    )

    # Comando para mostrar la versión del sistema
    subparsers.add_parser(
        'version',
        help='Muestra la versión del sistema',
        description='Muestra la versión actual del sistema y detalles de configuración'
    )

    # Comando para agregar una bitacora formateada
    format_parser = subparsers.add_parser(
        'formatear',
        help='Agregar una bitacora formateada',
        description='Este comando permitirá agregar una bitácora con formato específico (en desarrollo)'
    )
    format_parser.add_argument(
        '-f', '--file',
        help='Archivo de bitácora a formatear',
        metavar='ARCHIVO',
        type=str,
        required=True
    )

    # Comando crear un commit dinámico
    commit_parser = subparsers.add_parser(
        'commit',
        help='Crear un commit',
        description='Crear un commit de forma dinámica'
    )
    commit_parser.add_argument(
        '-m', '--mensaje',
        help='Agregar un mensaje opcional',
        metavar='MENSAJE',
        default=None,
        type=str,
        nargs='?'
    )

    args = parser.parse_args()

    if args.comando == 'crear':
        crear_bitacora(args.nombre, args.plantilla)
    elif args.comando == 'listar':
        listar_bitacoras()
    elif args.comando == 'plantillas':
        listar_plantillas(args.show_details)
    elif args.comando == 'cargar':
        print("pass")
    elif args.comando == 'config':
        modificar_configuracion(args.path, args.date_format)
    elif args.comando == 'directorio':
        crear_directorio()
    elif args.comando == 'version':
        mostrar_version()
    elif args.comando == 'formatear':
        formatear_archivo(args.file)
    elif args.comando == 'commit':
        crear_commit(args.mensaje)
    elif args.comando is None:
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
