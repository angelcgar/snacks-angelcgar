#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import shutil
import getpass
import json
from typing import Dict, Any

HOME_USER = os.path.expanduser("~")
SYSTEM_USER = getpass.getuser()
USER_EXECUTABLE_PATH = os.path.join(HOME_USER, ".local", "bin")

NOMBRE_CLI = "agregar_metadatos"

def install_cli():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cli_source = os.path.join(current_dir, "app.py")  # Ahora apunta a app.py

    # Crear directorios
    Path(USER_EXECUTABLE_PATH).mkdir(parents=True, exist_ok=True)

    # Copiar el CLI (app.py) con nombre NOMBRE_CLI
    cli_path = os.path.join(USER_EXECUTABLE_PATH, f"{NOMBRE_CLI}")
    try:
        shutil.copy(cli_source, cli_path)
        os.chmod(cli_path, 0o755)
        print(f"✓ CLI instalado en: {cli_path}")
    except Exception as e:
        print(f"⚠ Error al instalar CLI: {e}")
        if not os.path.exists(cli_source):
            print(f"Error: No se encontró el archivo app.py en {current_dir}")


    print(f"\nInstalación completada {SYSTEM_USER}. Puedes usar el comando '{NOMBRE_CLI}' desde cualquier lugar")

if __name__ == "__main__":
    install_cli()
