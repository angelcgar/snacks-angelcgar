#!/usr/bin/env python3
"""
Script de instalación para add-metadata CLI.
Verifica dependencias y crea un ejecutable en ~/.local/bin
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """
    Verifica que la versión de Python sea >= 3.7
    """
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")


def check_exiftool():
    """
    Verifica si ExifTool está instalado en el sistema.
    """
    try:
        result = subprocess.run(
            ['exiftool', '-ver'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✅ ExifTool {version} detectado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ExifTool no está instalado")
        print("\n💡 Instalación de ExifTool:")
        print("   Ubuntu/Debian: sudo apt-get install libimage-exiftool-perl")
        print("   macOS:         brew install exiftool")
        print("   Windows:       Descargar desde https://exiftool.org")
        print("\n❗ Instala ExifTool antes de usar el CLI\n")
        return False


def create_executable():
    """
    Crea un script ejecutable en ~/.local/bin
    """
    # Ruta del script fuente
    script_path = Path(__file__).parent / "add_metadata.py"

    if not script_path.exists():
        print(f"❌ Error: No se encuentra {script_path}")
        sys.exit(1)

    # Crear directorio ~/.local/bin si no existe
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)

    # Ruta de destino
    dest_path = local_bin / "add-metadata"

    # Copiar el script
    shutil.copy2(script_path, dest_path)

    # Hacer ejecutable
    os.chmod(dest_path, 0o755)

    print(f"✅ Instalado en: {dest_path}")

    # Verificar si ~/.local/bin está en PATH
    local_bin_str = str(local_bin)
    path_env = os.environ.get('PATH', '')

    if local_bin_str not in path_env:
        print("\n⚠️  IMPORTANTE: Agrega ~/.local/bin a tu PATH")
        print("\nPara Fish shell, ejecuta:")
        print(f'   fish_add_path {local_bin_str}')
        print("\nPara Bash/Zsh, agrega a ~/.bashrc o ~/.zshrc:")
        print(f'   export PATH="{local_bin_str}:$PATH"')
    else:
        print("✅ ~/.local/bin ya está en PATH")


def main():
    """
    Función principal de instalación.
    """
    print("=" * 60)
    print("🎵 Instalador de add-metadata CLI")
    print("=" * 60)
    print()

    # Verificar versión de Python
    check_python_version()

    # Verificar ExifTool (no es bloqueante)
    check_exiftool()

    print()
    print("📦 Instalando add-metadata...")
    print()

    # Crear ejecutable
    create_executable()

    print()
    print("=" * 60)
    print("✅ Instalación completada")
    print("=" * 60)
    print()
    print("🚀 Uso:")
    print('   add-metadata --artist "Artist" --album "Album" --pattern ".*\\.mp3$"')
    print()
    print("📖 Ayuda:")
    print("   add-metadata --help")
    print()


if __name__ == '__main__':
    main()
