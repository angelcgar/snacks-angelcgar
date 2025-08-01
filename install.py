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
CONFIGURATION_DIRECTORY = os.path.join(HOME_USER, ".config", "biblioteca_cli_config")
USER_EXECUTABLE_PATH = os.path.join(HOME_USER, ".local", "bin")
CONFIG_FILE_PATH = os.path.join(CONFIGURATION_DIRECTORY,"biblioteca_cli_config.json")
BIBLIOTECA_JSON = os.path.join(HOME_USER, ".config", "biblioteca_cli_config", "biblioteca_cli.json")

def load_config():
    print("Cargando configuración...")
    config_data: Dict[str, Any] = {
        "name": "bitacora_cli",
        "version": "1.1.0",
        "configuration": {
            "user": SYSTEM_USER,
            "paths": {
                "log_config_directory": CONFIGURATION_DIRECTORY,
                "log_config_file": CONFIG_FILE_PATH,
                "user_executable_path": USER_EXECUTABLE_PATH,
            },
            "dates": {
                "date_format": "%Y-%m-%d",
                "date_format_default": "%Y-%m-%d",
                "datetime_format": "%Y-%m-%d %H:%M:%S",
            }
        },
    }

    # Guardar datos en un archivo JSON
    with open(CONFIG_FILE_PATH, "w", encoding='utf-8') as f:
        json.dump(config_data, f, indent=4)
    print("Datos guardados en datos.json")

    with open(BIBLIOTECA_JSON, "w", encoding='utf-8') as f:
        tem_var = []
        json.dump(tem_var, f, indent=4)

def install_cli():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cli_source = os.path.join(current_dir, "app.py")  # Ahora apunta a app.py

    if os.path.exists(CONFIGURATION_DIRECTORY):
        print(f"El directorio de configuración ya existe: {CONFIGURATION_DIRECTORY}")
        print("Se eliminará y se volverá a instalar el CLI.")
        shutil.rmtree(CONFIGURATION_DIRECTORY)

    # Crear directorios
    Path(USER_EXECUTABLE_PATH).mkdir(parents=True, exist_ok=True)
    Path(CONFIGURATION_DIRECTORY).mkdir(parents=True, exist_ok=True)

    # Copiar el CLI (app.py) con nombre 'biblioteca'
    cli_path = os.path.join(USER_EXECUTABLE_PATH, "biblioteca")
    try:
        shutil.copy(cli_source, cli_path)
        os.chmod(cli_path, 0o755)
        print(f"✓ CLI instalado en: {cli_path}")
    except Exception as e:
        print(f"⚠ Error al instalar CLI: {e}")
        if not os.path.exists(cli_source):
            print(f"Error: No se encontró el archivo app.py en {current_dir}")

    load_config()

    print(f"\nInstalación completada {SYSTEM_USER}. Puedes usar el comando 'biblioteca' desde cualquier lugar")

if __name__ == "__main__":
    install_cli()
    # load_config()
