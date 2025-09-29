#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import getpass

HOME_USER = os.path.expanduser("~")
SYSTEM_USER = getpass.getuser()
USER_EXECUTABLE_PATH = os.path.join(HOME_USER, ".local", "bin")


def install_cli():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cli_source = os.path.join(current_dir, "actualizar-cv.py")

    # Crear directorios si no existen
    Path(USER_EXECUTABLE_PATH).mkdir(parents=True, exist_ok=True)

    # Copiar el CLI (harbor.py) con nombre 'harbor'
    cli_path = os.path.join(USER_EXECUTABLE_PATH, "acv")
    try:
        shutil.copy(cli_source, cli_path)
        os.chmod(cli_path, 0o755)
        print(f"✓ CLI instalado en: {cli_path}")
    except Exception as e:
        print(f"⚠ Error al instalar CLI: {e}")
        if not os.path.exists(cli_source):
            print(f"Error: No se encontró el archivo harbor.py en {current_dir}")

    print(f"\nInstalación completada {SYSTEM_USER}. Puedes usar el comando 'acv' desde cualquier lugar")

if __name__ == "__main__":
    install_cli()
