#!/usr/bin/env python3
"""
Harbor CLI - Administrador de bases de datos temporales con Docker

Un CLI moderno para crear y gestionar contenedores de bases de datos
de forma rápida y organizada para desarrollo y testing.
"""

import os
import json
import subprocess
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import track

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================

# Información de la aplicación
__version__ = "2.0.0"

# Configuración principal del CLI
app = typer.Typer(
    name="harbor",
    help="🐳 CLI para administrar bases de datos temporales con Docker",
    add_completion=False
)
console = Console()

# Directorio centralizado donde se almacenan todos los proyectos
HARBOR_VOLUMES_DIR = Path.home() / "Documentos" / "harbor_volumenes"

# Mapeo de puertos estándar para imágenes populares
IMAGE_PORTS = {
    "mysql": 3306,
    "postgres": 5432,
    "mongo": 27017,
    "redis": 6379,
    "mariadb": 3307
}

# =============================================================================
# FUNCIONES UTILITARIAS SIMPLES
# =============================================================================

def show_banner():
    """Muestra el banner visual principal de Harbor con Rich."""
    console.print(Panel.fit(
        "[bold blue]🐳 Harbor[/bold blue] — Docker DB Manager\n"
        "[dim]Administrador de bases de datos temporales[/dim]",
        border_style="blue"
    ))

def get_system_user() -> str:
    """Obtiene el nombre del usuario actual del sistema operativo."""
    try:
        return os.getlogin()
    except Exception:
        return "joedoe"  # Fallback por si falla getlogin()

def get_user_input(prompt_text: str, default: Optional[str] = None) -> str:
    """Solicita entrada del usuario con Rich prompt y valor por defecto."""
    if default:
        result = Prompt.ask(f"👉 {prompt_text}", default=default)
    else:
        result = Prompt.ask(f"👉 {prompt_text}")
    return result.strip()

# Fix: Revisa el commit 21-11-25_10:30, donde se añadió esta función.
def check_port_conflict(port: int) -> bool:
    """
    Verifica si un puerto está siendo usado por Docker.

    Args:
        port: Puerto a verificar

    Returns:
        bool: True si hay conflicto, False si está libre
    """
    try:
        result = subprocess.run([
            "docker", "ps", "--format", "{{.Ports}}"
        ], capture_output=True, text=True, check=True)

        # Buscar el puerto en la lista de puertos usados
        for line in result.stdout.strip().split('\n'):
            if f":{port}->" in line or f"{port}/tcp" in line:
                return True
        return False

    except (subprocess.CalledProcessError, FileNotFoundError):
        # Si no se puede verificar, asumir que está libre
        return False

def get_available_port(base_port: int, image: str) -> int:
    """
    Encuentra un puerto disponible basado en un puerto base.

    Args:
        base_port: Puerto preferido a verificar
        image: Tipo de imagen para mostrar información

    Returns:
        int: Puerto disponible
    """
    current_port = base_port

    # Verificar puerto base
    if not check_port_conflict(current_port):
        return current_port

    console.print(f"[yellow]⚠️ Puerto {base_port} ya está en uso[/yellow]")

    # Buscar puerto alternativo (incrementar de 1 en 1 hasta encontrar uno libre)
    for i in range(1, 100):  # Buscar en un rango razonable
        test_port = base_port + i
        if not check_port_conflict(test_port):
            console.print(f"[green]✅ Usando puerto alternativo: {test_port}[/green]")
            return test_port

    # Si no encuentra uno libre, preguntar al usuario
    console.print(f"[red]❌ No se encontró puerto libre automáticamente[/red]")
    port_input = get_user_input(f"Ingresa un puerto manual para {image}")
    try:
        return int(port_input)
    except ValueError:
        console.print("[bold red]❌ Puerto inválido[/bold red]")
        raise typer.Exit(1)

# =============================================================================
# FUNCIONES DE GENERACIÓN DE CONTENIDO
# =============================================================================

def create_docker_compose_content(
    image: str,
    version: str,
    container_name: str,
    root_password: str,
    db_name: str,
    system_user: str,
    user_password: str,
    port: int,
    volume_name: str
) -> str:
    """
    Genera el contenido del archivo docker-compose.yml basado en la imagen seleccionada.

    Configura automáticamente las variables de entorno específicas para cada tipo
    de base de datos (MySQL, PostgreSQL, MongoDB) con los puertos y credenciales correctos.
    """

    # Configuración de variables de entorno por tipo de imagen
    env_config = {
        "mysql": {
            "root_pass": "MYSQL_ROOT_PASSWORD",
            "db": "MYSQL_DATABASE",
            "user": "MYSQL_USER",
            "user_pass": "MYSQL_PASSWORD"
        },
        "postgres": {
            "root_pass": "POSTGRES_PASSWORD",
            "db": "POSTGRES_DB",
            "user": "POSTGRES_USER",
            "user_pass": "POSTGRES_PASSWORD"
        },
        "mongo": {
            "root_pass": "MONGO_INITDB_ROOT_PASSWORD",
            "db": "MONGO_INITDB_DATABASE",
            "user": "MONGO_INITDB_ROOT_USERNAME",
            "user_pass": "MONGO_INITDB_ROOT_PASSWORD"
        }
    }

    # Usar configuración específica o generar nombres para imágenes no estándar
    env_vars = env_config.get(image, {
        "root_pass": f"{image.upper()}_ROOT_PASSWORD",
        "db": f"{image.upper()}_DATABASE",
        "user": f"{image.upper()}_USER",
        "user_pass": f"{image.upper()}_PASSWORD"
    })

    return f"""version: "3.9"
services:
  db:
    image: {image}:{version}
    container_name: {container_name}
    restart: always
    environment:
      {env_vars["root_pass"]}: {root_password}
      {env_vars["db"]}: {db_name}
      {env_vars["user"]}: {system_user}
      {env_vars["user_pass"]}: {user_password}
    ports:
      - "{port}:{port}"
    volumes:
      - {volume_name}:/var/lib/{image}
volumes:
  {volume_name}:
    name: {volume_name}
"""

def get_connection_urls(image: str, system_user: str, user_password: str, root_password: str, port: int, db_name: str) -> dict:
    """
    Genera URLs de conexión listas para usar según el tipo de imagen de base de datos.

    Crea cadenas de conexión estándar para clientes SQL populares como DBeaver,
    pgAdmin, MySQL Workbench, etc. Incluye tanto credenciales root como de usuario.

    Args:
        image: Tipo de imagen (mysql, postgres, mongo, etc.)
        system_user: Nombre del usuario del sistema
        user_password: Contraseña del usuario personalizado
        root_password: Contraseña del usuario root/admin
        port: Puerto donde escucha la base de datos
        db_name: Nombre de la base de datos creada

    Returns:
        dict: URLs de conexión categorizadas por tipo de usuario
    """
    urls = {}

    # Generar URLs específicas para cada tipo de base de datos
    if image == "mysql":
        urls["root"] = f"mysql://root:{root_password}@localhost:{port}/{db_name}"
        urls["user"] = f"mysql://{system_user}:{user_password}@localhost:{port}/{db_name}"
    elif image == "postgres":
        urls["root"] = f"postgresql://postgres:{root_password}@localhost:{port}/{db_name}"
        urls["user"] = f"postgresql://{system_user}:{user_password}@localhost:{port}/{db_name}"
    elif image == "mongo":
        urls["root"] = f"mongodb://root:{root_password}@localhost:{port}/{db_name}"
        urls["user"] = f"mongodb://{system_user}:{user_password}@localhost:{port}/{db_name}"
    else:
        urls["info"] = f"{image} no soportado aún para URLs automáticas."

    return urls

def create_seed_file(project_dir) -> str:
    """
    Crea el archivo seed.sql con ejemplos para diferentes bases de datos.

    Genera un archivo con plantillas SQL comentadas para PostgreSQL, MySQL y SQLite
    que el desarrollador puede usar como punto de partida para sus datos de prueba.

    Args:
        project_dir: Ruta del directorio del proyecto (str o Path)

    Returns:
        str: Ruta completa al archivo seed.sql creado
    """
    seed_content = """-- ======================================================
-- SEED.SQL – Archivo de ejemplo para pruebas y demos
-- Aquí puedes escribir tus queries iniciales.
-- Este archivo NO se ejecuta automáticamente por Docker.
-- ======================================================

-- =====================
-- POSTGRESQL EJEMPLO
-- =====================
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username TEXT NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW()
-- );
--
-- INSERT INTO users (username) VALUES ('alice'), ('bob');



-- =====================
-- MYSQL EJEMPLO
-- =====================
-- CREATE TABLE users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(50) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
--
-- INSERT INTO users (username) VALUES ('alice'), ('bob');



-- =====================
-- SQLITE EJEMPLO
-- =====================
-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT NOT NULL,
--     created_at TEXT DEFAULT CURRENT_TIMESTAMP
-- );
--
-- INSERT INTO users (username) VALUES ('alice'), ('bob');

-- ======================================================
-- NOTA:
-- - Para usar este archivo, copia el bloque que necesites
--   y ejecútalo con el cliente SQL correspondiente.
-- - Ejemplo en Postgres:
--   docker exec -i <container> psql -U <user> -d <db> -f /path/seed.sql
-- - Ejemplo en MySQL:
--   docker exec -i <container> mysql -u <user> -p<password> <db> < seed.sql
-- ======================================================
"""

    seed_path = Path(project_dir) / "seed.sql"
    with open(seed_path, "w") as f:
        f.write(seed_content)

    return str(seed_path)# =============================================================================
# CALLBACK GLOBAL Y COMANDOS PRINCIPALES
# =============================================================================

@app.callback()
def version_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Mostrar la versión de Harbor CLI"
    )
):
    """
    Callback global que maneja la flag de versión.

    Se ejecuta antes que cualquier comando y permite mostrar la versión
    del CLI cuando se usa --version o -v.
    """
    if version:
        console.print(f"[bold blue]🐳 Harbor CLI[/bold blue] versión [green]{__version__}[/green]")
        console.print("[dim]Administrador de bases de datos temporales con Docker[/dim]")
        raise typer.Exit()

@app.command("new")
def create_project(
    project_name: str = typer.Argument(..., help="Nombre del proyecto"),
    image: str = typer.Option(..., "--image", help="Nombre de la imagen en Docker Hub (ej: mysql)"),
    version: str = typer.Option("latest", "--version-image", help="Versión de la imagen")
):
    """
    Crear un nuevo contenedor de base de datos con docker-compose.

    Genera automáticamente:
    - docker-compose.yml configurado
    - Archivo JSON con credenciales y URLs de conexión
    - seed.sql con ejemplos para testing
    - Levanta el contenedor en segundo plano
    """
    show_banner()

    console.print(f"\n[bold green]Creando proyecto:[/bold green] [cyan]{project_name}[/cyan]")
    console.print(f"[bold blue]Imagen:[/bold blue] {image}:{version}\n")

    # Obtener datos del usuario
    system_user = get_system_user()
    user_password = get_user_input("Ingresa la contraseña para el usuario", "password")
    description = get_user_input("Ingresa una descripción opcional", "No description")

    # Crear directorio de Harbor si no existe
    HARBOR_VOLUMES_DIR.mkdir(parents=True, exist_ok=True)

    # Crear directorio del proyecto dentro de harbor_volumenes
    project_dir = HARBOR_VOLUMES_DIR / f"contenedor_{project_name}"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Variables del proyecto
    root_password = "123456789"
    db_name = f"{project_name}_db"
    container_name = f"{project_name}_container"
    volume_name = f"{project_name}_data"

    # Determinar puerto con detección de conflictos
    if image in IMAGE_PORTS:
        base_port = IMAGE_PORTS[image]
        port = get_available_port(base_port, image)
    else:
        port_input = get_user_input(f"Ingresa el puerto a mapear para {image}")
        try:
            port = int(port_input)
        except ValueError:
            console.print("[bold red]❌ Debes ingresar un número de puerto válido[/bold red]")
            raise typer.Exit(1)

    # Crear archivos del proyecto
    tasks = [
        "Generando docker-compose.yml",
        "Creando archivo de configuración",
        "Generando seed.sql",
        "Levantando contenedor"
    ]

    for task in track(tasks, description="[cyan]Configurando proyecto..."):
        if task == "Generando docker-compose.yml":
            # Crear docker-compose.yml
            compose_content = create_docker_compose_content(
                image, version, container_name, root_password,
                db_name, system_user, user_password, port, volume_name
            )

            compose_path = project_dir / "docker-compose.yml"
            with open(compose_path, "w") as f:
                f.write(compose_content)

        elif task == "Creando archivo de configuración":
            # Crear archivo de información JSON
            connection_urls = get_connection_urls(image, system_user, user_password, root_password, port, db_name)

            info = {
                "project_name": project_name,
                "image": image,
                "version": version,
                "system_user": system_user,
                "user_password": user_password,
                "root_password": root_password,
                "database": db_name,
                "description": description,
                "volume": volume_name,
                "container_name": container_name,
                "port": port,
                "connection_urls": connection_urls
            }

            info_path = project_dir / f"{project_name}_info.json"
            with open(info_path, "w") as f:
                json.dump(info, f, indent=4)

        elif task == "Generando seed.sql":
            seed_path = create_seed_file(project_dir)

        elif task == "Levantando contenedor":
            # Levantar contenedor
            try:
                subprocess.run(
                    ["docker", "compose", "-f", str(compose_path), "up", "-d"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]❌ Error al levantar el contenedor: {e}[/bold red]")
                raise typer.Exit(1)

    # Mostrar resumen
    console.print("\n[bold green]✅ Proyecto creado exitosamente[/bold green]")

    # Tabla de información
    table = Table(title="Información del Proyecto", show_header=True, header_style="bold blue")
    table.add_column("Campo", style="cyan", no_wrap=True)
    table.add_column("Valor", style="green")

    table.add_row("📁 Directorio", str(project_dir))
    table.add_row("🐳 Imagen", f"{image}:{version}")
    table.add_row("📦 Contenedor", container_name)
    table.add_row("🔌 Puerto", str(port))
    table.add_row("🗄️ Base de datos", db_name)
    table.add_row("📝 Configuración", str(info_path))
    table.add_row("🌱 Seed file", seed_path)

    console.print(table)
    console.print(f"\n[bold yellow]🚀 Contenedor levantado en segundo plano (modo -d)[/bold yellow]")

@app.command("get-up")
def start_project(
    project_name: str = typer.Argument(..., help="Nombre del proyecto a levantar")
):
    """
    Levantar un proyecto existente con docker-compose.

    Busca el proyecto en la carpeta harbor_volumenes y ejecuta 'docker-compose up -d'
    para iniciarlo en segundo plano. Valida que existan los archivos necesarios.
    """
    show_banner()

    # Construir ruta al proyecto en el directorio centralizado
    project_dir = HARBOR_VOLUMES_DIR / f"contenedor_{project_name}"
    compose_path = project_dir / "docker-compose.yml"

    # Verificar que el proyecto existe
    if not compose_path.exists():
        console.print(f"[bold red]❌ No se encontró {compose_path}[/bold red]")
        console.print("¿Creaste el proyecto antes con [cyan]harbor new[/cyan]?")
        raise typer.Exit(1)

    console.print(f"[cyan]Levantando proyecto:[/cyan] [bold]{project_name}[/bold]")

    try:
        with console.status("[bold green]Iniciando contenedor..."):
            subprocess.run(
                ["docker", "compose", "-f", str(compose_path), "up", "-d"],
                check=True,
                capture_output=True
            )

        console.print(f"[bold green]🚀 Proyecto '{project_name}' levantado con éxito[/bold green]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error al levantar el proyecto: {e}[/bold red]")
        raise typer.Exit(1)

@app.command("list")
def list_containers():
    """
    Listar todos los contenedores Docker con información detallada.

    Muestra:
    - Contenedores activos con tabla formateada (nombres, imagen, estado, puertos)
    - Contador de contenedores detenidos
    - Lista específica de proyectos Harbor creados
    - Estado de archivos docker-compose.yml por proyecto
    """
    show_banner()

    console.print("[bold blue]📋 Estado de contenedores Docker[/bold blue]\n")

    try:
        # Obtener información detallada de contenedores activos
        result = subprocess.run([
            "docker", "ps", "--format",
            "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.CreatedAt}}"
        ], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            console.print("[bold green]🟢 Contenedores activos:[/bold green]")
            console.print(result.stdout)
        else:
            console.print("[yellow]ℹ️ No hay contenedores activos en este momento[/yellow]")

        # Obtener todos los contenedores (incluidos los detenidos)
        all_result = subprocess.run([
            "docker", "ps", "-a", "--format",
            "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.CreatedAt}}"
        ], capture_output=True, text=True, check=True)

        # Contar contenedores detenidos
        all_containers = all_result.stdout.strip().split('\n')[1:]  # Quitar header
        active_containers = result.stdout.strip().split('\n')[1:] if result.stdout.strip() else []

        stopped_count = len(all_containers) - len(active_containers)

        if stopped_count > 0:
            console.print(f"\n[dim]🔴 {stopped_count} contenedor(es) detenido(s)[/dim]")

        # Mostrar información de proyectos Harbor
        console.print(f"\n[bold cyan]📁 Proyectos Harbor en {HARBOR_VOLUMES_DIR}:[/bold cyan]")

        if HARBOR_VOLUMES_DIR.exists():
            harbor_projects = [d for d in HARBOR_VOLUMES_DIR.iterdir()
                             if d.is_dir() and d.name.startswith('contenedor_')]

            if harbor_projects:
                table = Table(show_header=True, header_style="bold blue")
                table.add_column("🚀 Proyecto", style="cyan", no_wrap=True)
                table.add_column("📁 Directorio", style="green")
                table.add_column("📄 Compose", style="yellow")

                for project in harbor_projects:
                    project_name = project.name.replace('contenedor_', '')
                    compose_exists = "✅" if (project / "docker-compose.yml").exists() else "❌"
                    table.add_row(project_name, str(project.name), compose_exists)

                console.print(table)
            else:
                console.print("[dim]No hay proyectos Harbor creados aún[/dim]")
        else:
            console.print("[dim]Directorio Harbor no encontrado[/dim]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error al listar contenedores: {e}[/bold red]")
        console.print("[dim]¿Está Docker ejecutándose?[/dim]")
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print("[bold red]❌ Docker no está instalado o no está en PATH[/bold red]")
        raise typer.Exit(1)

@app.command("clean")
def clean_all():
    """
    Detener y eliminar todos los contenedores Docker del sistema.

    Operación destructiva que:
    1. Solicita confirmación al usuario
    2. Detiene todos los contenedores activos
    3. Elimina todos los contenedores (activos + detenidos)

    ⚠️ ADVERTENCIA: Esta acción no se puede deshacer
    """
    show_banner()

    # Solicitar confirmación antes de proceder con la operación destructiva
    if not Confirm.ask("🗑️ ¿Estás seguro de que quieres detener y eliminar TODOS los contenedores?"):
        console.print("[yellow]Operación cancelada[/yellow]")
        raise typer.Exit()

    console.print("[bold yellow]🧹 Limpiando todos los contenedores...[/bold yellow]")

    try:
        # Detener todos los contenedores en ejecución
        with console.status("[bold yellow]Deteniendo contenedores..."):
            running = subprocess.run(
                ["docker", "ps", "-q"],
                capture_output=True,
                text=True,
                check=True
            )

            if running.stdout.strip():
                subprocess.run(
                    ["docker", "stop"] + running.stdout.split(),
                    check=True,
                    capture_output=True
                )
                console.print("🛑 Todos los contenedores detenidos")
            else:
                console.print("ℹ️ No había contenedores en ejecución")

        # Eliminar todos los contenedores
        with console.status("[bold red]Eliminando contenedores..."):
            all_containers = subprocess.run(
                ["docker", "ps", "-aq"],
                capture_output=True,
                text=True,
                check=True
            )

            if all_containers.stdout.strip():
                subprocess.run(
                    ["docker", "rm"] + all_containers.stdout.split(),
                    check=True,
                    capture_output=True
                )
                console.print("🧹 Todos los contenedores eliminados")
            else:
                console.print("ℹ️ No había contenedores para eliminar")

        console.print("\n[bold green]✅ Limpieza completada[/bold green]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error al limpiar contenedores: {e}[/bold red]")
        raise typer.Exit(1)

# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

def main():
    """
    Función principal que inicializa la aplicación Harbor CLI.

    Punto de entrada que lanza Typer con todos los comandos registrados
    y maneja la configuración global de la aplicación.
    """
    app()

if __name__ == "__main__":
    main()
