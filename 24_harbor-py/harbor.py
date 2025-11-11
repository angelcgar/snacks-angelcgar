#!/usr/bin/env python3

import os
import json
import subprocess
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import track

# Configuración inicial
app = typer.Typer(
    name="harbor",
    help="🐳 CLI para administrar bases de datos temporales con Docker",
    add_completion=False
)
console = Console()

# Mapeo de imágenes comunes y sus puertos por defecto
IMAGE_PORTS = {
    "mysql": 3306,
    "postgres": 5432,
    "mongo": 27017,
    "redis": 6379,
    "mariadb": 3307
}

def show_banner():
    """Muestra el banner principal de Harbor."""
    console.print(Panel.fit(
        "[bold blue]🐳 Harbor[/bold blue] — Docker DB Manager\n"
        "[dim]Administrador de bases de datos temporales[/dim]",
        border_style="blue"
    ))

def get_system_user() -> str:
    """Obtiene el usuario del sistema."""
    try:
        return os.getlogin()
    except Exception:
        return "joedoe"

def get_user_input(prompt_text: str, default: str = None) -> str:
    """Obtiene entrada del usuario con Rich prompt."""
    if default:
        result = Prompt.ask(f"👉 {prompt_text}", default=default)
    else:
        result = Prompt.ask(f"👉 {prompt_text}")
    return result.strip()

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
    """Genera el contenido del docker-compose.yml."""

    # Configuración específica por imagen
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
    """Genera las URLs de conexión según el tipo de imagen."""
    urls = {}

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

def create_seed_file(project_dir: str):
    """Crea el archivo seed.sql con ejemplos."""
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

    seed_path = os.path.join(project_dir, "seed.sql")
    with open(seed_path, "w") as f:
        f.write(seed_content)

    return seed_path

@app.command("new")
def create_project(
    project_name: str = typer.Argument(..., help="Nombre del proyecto"),
    image: str = typer.Option(..., "--image", help="Nombre de la imagen en Docker Hub (ej: mysql)"),
    version: str = typer.Option("latest", "--version-image", help="Versión de la imagen")
):
    """🚀 Crear un nuevo contenedor de base de datos con docker-compose."""
    show_banner()

    console.print(f"\n[bold green]Creando proyecto:[/bold green] [cyan]{project_name}[/cyan]")
    console.print(f"[bold blue]Imagen:[/bold blue] {image}:{version}\n")

    # Obtener datos del usuario
    system_user = get_system_user()
    user_password = get_user_input("Ingresa la contraseña para el usuario", "password")
    description = get_user_input("Ingresa una descripción opcional", "No description")

    # Crear directorio del proyecto
    project_dir = f"contenedor_{project_name}"
    os.makedirs(project_dir, exist_ok=True)

    # Variables del proyecto
    root_password = "123456789"
    db_name = f"{project_name}_db"
    container_name = f"{project_name}_container"
    volume_name = f"{project_name}_data"

    # Determinar puerto
    if image in IMAGE_PORTS:
        port = IMAGE_PORTS[image]
        console.print(f"[dim]Usando puerto predeterminado: {port}[/dim]")
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

            compose_path = os.path.join(project_dir, "docker-compose.yml")
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

            info_path = os.path.join(project_dir, f"{project_name}_info.json")
            with open(info_path, "w") as f:
                json.dump(info, f, indent=4)

        elif task == "Generando seed.sql":
            seed_path = create_seed_file(project_dir)

        elif task == "Levantando contenedor":
            # Levantar contenedor
            try:
                subprocess.run(
                    ["docker", "compose", "-f", compose_path, "up", "-d"],
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

    table.add_row("📁 Directorio", project_dir)
    table.add_row("🐳 Imagen", f"{image}:{version}")
    table.add_row("📦 Contenedor", container_name)
    table.add_row("🔌 Puerto", str(port))
    table.add_row("🗄️ Base de datos", db_name)
    table.add_row("📝 Configuración", info_path)
    table.add_row("🌱 Seed file", seed_path)

    console.print(table)
    console.print(f"\n[bold yellow]🚀 Contenedor levantado en segundo plano (modo -d)[/bold yellow]")

@app.command("get-up")
def start_project(
    project_name: str = typer.Argument(..., help="Nombre del proyecto a levantar")
):
    """🚀 Levantar un proyecto existente con docker-compose."""
    show_banner()

    project_dir = f"contenedor_{project_name}"
    compose_path = os.path.join(project_dir, "docker-compose.yml")

    if not os.path.exists(compose_path):
        console.print(f"[bold red]❌ No se encontró {compose_path}[/bold red]")
        console.print("¿Creaste el proyecto antes con [cyan]harbor new[/cyan]?")
        raise typer.Exit(1)

    console.print(f"[cyan]Levantando proyecto:[/cyan] [bold]{project_name}[/bold]")

    try:
        with console.status("[bold green]Iniciando contenedor...") as status:
            subprocess.run(
                ["docker", "compose", "-f", compose_path, "up", "-d"],
                check=True,
                capture_output=True
            )

        console.print(f"[bold green]🚀 Proyecto '{project_name}' levantado con éxito[/bold green]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error al levantar el proyecto: {e}[/bold red]")
        raise typer.Exit(1)

@app.command("clean")
def clean_all():
    """🧹 Detener y eliminar todos los contenedores."""
    show_banner()

    if not Confirm.ask("🗑️ ¿Estás seguro de que quieres detener y eliminar TODOS los contenedores?"):
        console.print("[yellow]Operación cancelada[/yellow]")
        raise typer.Exit()

    console.print("[bold yellow]🧹 Limpiando todos los contenedores...[/bold yellow]")

    try:
        # Detener todos los contenedores en ejecución
        with console.status("[bold yellow]Deteniendo contenedores...") as status:
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
        with console.status("[bold red]Eliminando contenedores...") as status:
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

def main():
    """Punto de entrada principal."""
    app()

if __name__ == "__main__":
    main()
