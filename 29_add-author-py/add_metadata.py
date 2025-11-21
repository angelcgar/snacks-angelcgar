#!/usr/bin/env python3
"""
CLI para agregar metadatos ID3 (Artist/Album) a archivos de audio sin renombrarlos.
Utiliza ExifTool para escribir metadatos de manera confiable.
"""

import argparse
import subprocess
import sys
import re
from pathlib import Path
from typing import List, Optional


def parse_arguments() -> argparse.Namespace:
    """
    Configura y parsea los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description="Actualiza metadatos ID3 (Artist/Album) en archivos de audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Procesar múltiples archivos con patrón
  %(prog)s --artist "Led Zeppelin" --album "IV" --pattern ".*\\.mp3$"
  %(prog)s --artist "Pink Floyd" --pattern "track.*\\.m4a$" --path /music

  # Procesar un solo archivo (modo debugging)
  %(prog)s --artist "The Beatles" --album "Abbey Road" --file "song.mp3"
  %(prog)s --artist "Queen" --file "bohemian.mp3"
        """
    )

    parser.add_argument(
        '--artist',
        type=str,
        required=True,
        help='Artista a escribir en los metadatos del archivo'
    )

    parser.add_argument(
        '--album',
        type=str,
        required=False,
        default=None,
        help='Álbum a escribir en los metadatos del archivo (opcional)'
    )

    parser.add_argument(
        '--pattern',
        type=str,
        required=False,
        help='Expresión regular para seleccionar archivos objetivo'
    )

    parser.add_argument(
        '--file',
        type=str,
        required=False,
        help='Archivo único a procesar (para debugging)'
    )

    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Directorio donde buscar archivos (por defecto: directorio actual)'
    )

    return parser.parse_args()


def check_exiftool_installed() -> bool:
    """
    Verifica si ExifTool está instalado y disponible en el sistema.

    Returns:
        bool: True si ExifTool está disponible, False en caso contrario
    """
    try:
        result = subprocess.run(
            ['exiftool', '-ver'],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def find_matching_files(directory: str, pattern: str) -> List[Path]:
    """
    Busca archivos que coincidan con el patrón regex en el directorio especificado.

    Args:
        directory: Ruta del directorio donde buscar
        pattern: Expresión regular para filtrar archivos

    Returns:
        List[Path]: Lista de rutas de archivos que coinciden con el patrón
    """
    # Compilar el patrón regex para validación
    try:
        regex = re.compile(pattern)
    except re.error as e:
        print(f"❌ Error: Patrón regex inválido: {e}", file=sys.stderr)
        sys.exit(1)

    directory_path = Path(directory)

    # Verificar que el directorio existe
    if not directory_path.exists():
        print(f"❌ Error: El directorio '{directory}' no existe", file=sys.stderr)
        sys.exit(1)

    if not directory_path.is_dir():
        print(f"❌ Error: '{directory}' no es un directorio", file=sys.stderr)
        sys.exit(1)

    # Buscar archivos que coincidan con el patrón
    matching_files = []

    for file_path in directory_path.rglob('*'):
        # Solo procesar archivos (no directorios)
        if file_path.is_file() and regex.search(file_path.name):
            matching_files.append(file_path)

    return matching_files


def update_file_metadata(file_path: Path, artist: str, album: Optional[str] = None) -> bool:
    """
    Actualiza los metadatos Artist y Album de un archivo usando ExifTool.

    Args:
        file_path: Ruta del archivo a actualizar
        artist: Valor para el campo Artist
        album: Valor para el campo Album (opcional)

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    try:
        # Comando ExifTool para actualizar metadatos sin modificar el nombre del archivo
        # -overwrite_original: No crear archivo de respaldo
        # -Artist: Establecer artista
        # -Album: Establecer álbum (si se proporciona)
        command = [
            'exiftool',
            '-overwrite_original',
            f'-Artist={artist}',
        ]

        # Solo agregar Album si se proporcionó
        if album:
            command.append(f'-Album={album}')

        command.append(str(file_path))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error al actualizar '{file_path.name}': {e.stderr.strip()}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"⚠️  Error inesperado al procesar '{file_path.name}': {e}", file=sys.stderr)
        return False


def process_files(files: List[Path], artist: str, album: Optional[str] = None) -> dict:
    """
    Procesa múltiples archivos y actualiza sus metadatos.

    Args:
        files: Lista de archivos a procesar
        artist: Valor para el campo Artist
        album: Valor para el campo Album (opcional)

    Returns:
        dict: Estadísticas de procesamiento (success, failed, total)
    """
    stats = {
        'success': 0,
        'failed': 0,
        'total': len(files)
    }

    print(f"\n🎵 Procesando {stats['total']} archivo(s)...\n")

    for file_path in files:
        print(f"📝 Actualizando: {file_path.name}")

        if update_file_metadata(file_path, artist, album):
            stats['success'] += 1
            print(f"   ✅ Éxito")
        else:
            stats['failed'] += 1
            print(f"   ❌ Falló")

        print()  # Línea en blanco para separación

    return stats


def print_summary(stats: dict, artist: str, album: Optional[str] = None):
    """
    Muestra un resumen del procesamiento de archivos.

    Args:
        stats: Diccionario con estadísticas de procesamiento
        artist: Artista aplicado
        album: Álbum aplicado (opcional)
    """
    print("=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    print(f"Artista aplicado:  {artist}")
    if album:
        print(f"Álbum aplicado:    {album}")
    else:
        print(f"Álbum aplicado:    (no especificado)")
    print(f"\nArchivos procesados: {stats['total']}")
    print(f"  ✅ Exitosos:       {stats['success']}")
    print(f"  ❌ Fallidos:       {stats['failed']}")
    print("=" * 60)


def main():
    """
    Función principal que coordina la ejecución del CLI.
    """
    # Parsear argumentos
    args = parse_arguments()

    # Validar que se proporcione --pattern o --file
    if not args.pattern and not args.file:
        print("❌ Error: Debes proporcionar --pattern o --file", file=sys.stderr)
        sys.exit(1)

    if args.pattern and args.file:
        print("❌ Error: No puedes usar --pattern y --file al mismo tiempo", file=sys.stderr)
        sys.exit(1)

    # Verificar que ExifTool está instalado
    if not check_exiftool_installed():
        print("❌ Error: ExifTool no está instalado o no está en PATH", file=sys.stderr)
        print("\n💡 Instalación:", file=sys.stderr)
        print("   Ubuntu/Debian: sudo apt-get install libimage-exiftool-perl", file=sys.stderr)
        print("   macOS:         brew install exiftool", file=sys.stderr)
        print("   Windows:       Descargar desde https://exiftool.org", file=sys.stderr)
        sys.exit(1)

    # Modo: archivo único (para debugging)
    if args.file:
        file_path = Path(args.file)

        if not file_path.exists():
            print(f"❌ Error: El archivo '{args.file}' no existe", file=sys.stderr)
            sys.exit(1)

        if not file_path.is_file():
            print(f"❌ Error: '{args.file}' no es un archivo", file=sys.stderr)
            sys.exit(1)

        print(f"🎯 Modo debugging: procesando archivo único")
        print(f"📝 Archivo: {file_path.name}")
        print(f"👤 Artista: {args.artist}")
        if args.album:
            print(f"💿 Álbum: {args.album}")
        print()

        # Procesar archivo único
        success = update_file_metadata(file_path, args.artist, args.album)

        if success:
            print("✅ Metadatos actualizados exitosamente")
            sys.exit(0)
        else:
            print("❌ Error al actualizar metadatos")
            sys.exit(1)

    # Modo: búsqueda por patrón (modo normal)
    print(f"🔍 Buscando archivos en '{args.path}' con patrón: {args.pattern}")
    matching_files = find_matching_files(args.path, args.pattern)

    # Verificar que se encontraron archivos
    if not matching_files:
        print(f"\n⚠️  No se encontraron archivos que coincidan con el patrón '{args.pattern}'")
        sys.exit(0)

    print(f"✅ Encontrados {len(matching_files)} archivo(s)")

    # Procesar archivos
    stats = process_files(matching_files, args.artist, args.album)

    # Mostrar resumen
    print_summary(stats, args.artist, args.album)

    # Código de salida basado en resultados
    if stats['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
