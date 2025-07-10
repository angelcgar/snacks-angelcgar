#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import shutil
import getpass

def install_cli():
    user = getpass.getuser()

    local_bin = os.path.join(os.path.expanduser("~"), ".local", "bin")
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "bitacora_cli_config")

    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cli_source = os.path.join(current_dir, "app.py")  # Ahora apunta a app.py

    # Crear directorios si no existen
    Path(local_bin).mkdir(parents=True, exist_ok=True)
    Path(config_dir).mkdir(parents=True, exist_ok=True)

    # Clonar repositorio de plantillas
    # TODO: Cambiar la URL del repositorio a tu repositorio real
    print("Clonando repositorio de plantillas...")
    repo_url = "https://github.com/angelcgar/bitacoras_diarias_templates.git"

    try:
        if os.path.exists(config_dir):
            print(f"El directorio de configuración ya existe: {config_dir}")
            print("Se eliminará y se volverá a clonar el repositorio.")
            shutil.rmtree(config_dir)

        subprocess.run(["git", "clone", repo_url, config_dir], check=True)
        # Eliminar .git
        git_dir = os.path.join(config_dir, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir)
        print("✓ Plantillas descargadas correctamente")
    except Exception as e:
        print(f"⚠ Error al clonar repositorio: {e}")
        print("Se usará la plantilla por defecto")

    # Copiar el CLI (app.py) con nombre 'bitacora'
    cli_path = os.path.join(local_bin, "bitacora")
    try:
        shutil.copy(cli_source, cli_path)
        os.chmod(cli_path, 0o755)
        print(f"✓ CLI instalado en: {cli_path}")
    except Exception as e:
        print(f"⚠ Error al instalar CLI: {e}")
        if not os.path.exists(cli_source):
            print(f"Error: No se encontró el archivo app.py en {current_dir}")

    print(f"\nInstalación completada {user}. Puedes usar el comando 'bitacora' desde cualquier lugar")

if __name__ == "__main__":
    install_cli()
