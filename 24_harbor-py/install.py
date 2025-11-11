#!/usr/bin/env python3

import sys
import os
import subprocess
import shutil
from pathlib import Path

def check_virtual_env():
    """Verifica si el entorno virtual está activado."""
    print("🔍 Verificando entorno virtual...")

    # Verificar si estamos en un entorno virtual
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        print("❌ Error: No hay un entorno virtual activado.")
        print("💡 Activa tu entorno virtual con: source venv/bin/activate")
        sys.exit(1)

    print("✅ Entorno virtual detectado correctamente")

def install_dependencies():
    """Instala las dependencias necesarias."""
    print("\n📦 Instalando dependencias...")

    dependencies = ["pyinstaller", "typer", "rich"]

    for dep in dependencies:
        try:
            print(f"  Installing {dep}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], check=True, capture_output=True)

        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {dep}: {e}")
            return False

    print("✅ Dependencias instaladas correctamente")
    return True

def build_executable():
    """Ejecuta PyInstaller para crear el ejecutable."""
    print("\n🔨 Construyendo ejecutable con PyInstaller...")

    try:
        result = subprocess.run([
            "pyinstaller",
            "--onefile",
            "--name", "harbor",
            "harbor.py"
        ], check=True, capture_output=True, text=True)

        print("✅ Ejecutable creado exitosamente")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar PyInstaller: {e}")
        print(f"Salida del error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Error: PyInstaller no está disponible.")
        print("💡 Reinstalando PyInstaller...")
        return False

def set_executable_permissions():
    """Establece permisos de ejecución en el binario."""
    print("\n🔐 Estableciendo permisos de ejecución...")

    executable_path = Path("dist/harbor")

    if not executable_path.exists():
        print(f"❌ Error: No se encontró el ejecutable en {executable_path}")
        return False

    try:
        # Dar permisos de ejecución (rwxr-xr-x)
        os.chmod(executable_path, 0o755)
        print("✅ Permisos de ejecución establecidos")
        return True

    except Exception as e:
        print(f"❌ Error al establecer permisos: {e}")
        return False

def install_to_user_bin():
    """Mueve el ejecutable a ~/.local/bin/"""
    print("\n📦 Instalando en ~/.local/bin/...")

    # Rutas de origen y destino
    source_path = Path("dist/harbor")
    dest_dir = Path.home() / ".local" / "bin"
    dest_path = dest_dir / "harbor"

    # Verificar que el ejecutable existe
    if not source_path.exists():
        print(f"❌ Error: No se encontró el ejecutable en {source_path}")
        return False

    try:
        # Crear el directorio de destino si no existe
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Copiar el ejecutable al destino
        shutil.copy2(source_path, dest_path)

        # Asegurar permisos de ejecución en el destino
        os.chmod(dest_path, 0o755)

        print(f"✅ harbor instalado exitosamente en {dest_path}")
        print(f"\n🎉 Instalación completa!")
        print(f"💡 Asegúrate de que ~/.local/bin esté en tu PATH")
        print(f"   Puedes agregarlo con: echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.bashrc")
        print(f"   O para Fish shell: echo 'set -gx PATH $HOME/.local/bin $PATH' >> ~/.config/fish/config.fish")

        return True

    except Exception as e:
        print(f"❌ Error al instalar: {e}")
        return False

def main():
    """Función principal del instalador."""
    print("🐳 Instalador de Harbor - Docker DB Manager")
    print("=" * 50)

    # Paso 1: Verificar entorno virtual
    check_virtual_env()

    # Paso 2: Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error al instalar dependencias. Abortando instalación.")
        sys.exit(1)

    # Paso 3: Construir ejecutable
    if not build_executable():
        print("\n❌ La construcción del ejecutable falló. Abortando instalación.")
        sys.exit(1)

    # Paso 4: Establecer permisos
    if not set_executable_permissions():
        print("\n❌ Error al establecer permisos. Abortando instalación.")
        sys.exit(1)

    # Paso 5: Instalar en ~/.local/bin/
    if not install_to_user_bin():
        print("\n❌ Error en la instalación final. Abortando.")
        sys.exit(1)

    print("\n🎯 ¡Harbor está listo para usar!")
    print("   Prueba ejecutando: harbor --help")
    print("   Crea tu primer contenedor: harbor new mi-db --image postgres")

if __name__ == "__main__":
    main()
