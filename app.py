#!/usr/bin/env python3

import os
import argparse
from datetime import datetime

# Configuración
BITACORAS_DIR = "/home/user/Documentos/bitacoras"
PLANTILLA = """# Bitácora - {fecha}

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

def verificar_directorio():
    """Verifica si el directorio de bitácoras existe, si no, lo crea."""
    if not os.path.exists(BITACORAS_DIR):
        os.makedirs(BITACORAS_DIR)
        print(f"Directorio creado: {BITACORAS_DIR}")

def crear_bitacora(nombre: str | None = None):
    """Crea una nueva bitácora con la plantilla predeterminada."""
    verificar_directorio()

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    if nombre:
        nombre_archivo = f"bitacora_{nombre}_{fecha_actual}.md"
    else:
        nombre_archivo = f"bitacora_{fecha_actual}.md"

    ruta_completa = os.path.join(BITACORAS_DIR, nombre_archivo)

    if os.path.exists(ruta_completa):
        print(f"¡Advertencia: El archivo {nombre_archivo} ya existe!")
        return

    contenido = PLANTILLA.format(fecha=fecha_actual)

    with open(ruta_completa, 'w') as f:
        f.write(contenido)

    print(f"Bitácora creada exitosamente: {ruta_completa}")

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
    parser = argparse.ArgumentParser(description='Gestor de Bitácoras - Crea y administra plantillas de bitácoras')
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')

    # Comando para crear nueva bitácora
    crear_parser = subparsers.add_parser('crear', help='Crear una nueva bitácora')
    crear_parser.add_argument('-n', '--nombre', help='Nombre descriptivo para la bitácora (opcional)')

    # Comando para listar bitácoras
    listar_parser = subparsers.add_parser('listar', help='Listar todas las bitácoras existentes')

    args = parser.parse_args()

    if args.comando == 'crear':
        crear_bitacora(args.nombre)
    elif args.comando == 'listar':
        listar_bitacoras()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
