#!/usr/bin/env python3

import subprocess
import typer
import os
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(add_completion=False)
console = Console()

# Variable global para controlar el modo verbose
verbose_mode = False

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mostrar salida detallada de Maven")
):
    """mvnx — Maven CLI mejorado"""
    global verbose_mode
    verbose_mode = verbose

# ---- Banner inicial ----
def show_banner():
    console.print(Panel.fit("[bold blue]mvnx[/bold blue] — Maven CLI mejorado\n[dim]Por Angel Contreras[/dim]"))

# ---- Función de verificación de pom.xml ----
def check_pom():
    """Verifica si existe el archivo pom.xml en el directorio actual."""
    if not os.path.exists("pom.xml"):
        console.print("[bold red]⚠️ No se encontró pom.xml en el directorio actual.[/bold red]")
        raise typer.Exit(1)

# ---- Función para ejecutar comandos Maven con manejo de errores ----
def run_maven_command(command: list, description: str = "comando Maven"):
    """Ejecuta un comando Maven con manejo de errores y modo verbose."""
    # Agregar -q si no está en modo verbose y no está ya presente
    if not verbose_mode and "-q" not in command:
        command.insert(1, "-q")

    result = subprocess.run(command)

    if result.returncode != 0:
        console.print(f"[bold red]❌ Error: el comando de Maven falló.[/bold red]")
        raise typer.Exit(1)

# ---- Comandos principales ----
@app.command()
def run(main: str = typer.Argument(..., help="Clase principal a ejecutar, ej. com.gm.App")):
    """Ejecuta una clase principal de Maven."""
    check_pom()
    show_banner()
    console.print(f"[cyan]Ejecutando clase:[/cyan] {main}\n")
    run_maven_command(["mvn", "exec:java", f"-Dexec.mainClass={main}"])

@app.command()
def clean():
    """Limpia el proyecto Maven (equivale a 'mvn clean')."""
    check_pom()
    show_banner()
    console.print("[yellow]Limpiando proyecto...[/yellow]\n")
    run_maven_command(["mvn", "clean"])

@app.command()
def build():
    """Compila el proyecto Maven (equivale a 'mvn compile')."""
    check_pom()
    show_banner()
    console.print("[green]Compilando proyecto...[/green]\n")
    run_maven_command(["mvn", "compile"])

@app.command()
def info():
    """Muestra información básica del proyecto Maven."""
    check_pom()
    show_banner()
    run_maven_command(["mvn", "help:effective-pom"])

@app.command()
def test():
    """Ejecuta las pruebas del proyecto Maven (equivale a 'mvn test')."""
    check_pom()
    show_banner()
    console.print("[magenta]Ejecutando pruebas...[/magenta]\n")
    run_maven_command(["mvn", "test"])

@app.command()
def create(
    group_id: str = typer.Argument(..., help="Group ID del proyecto, ej. com.gm"),
    project_name: str = typer.Argument(..., help="Nombre del proyecto (artifactId)")
):
    """Crea un nuevo proyecto Maven con Java 23."""
    show_banner()
    console.print(f"[green]Creando proyecto Maven:[/green] {project_name}")
    console.print(f"[cyan]Group ID:[/cyan] {group_id}\n")

    command = [
        "mvn", "archetype:generate",
        f"-DgroupId={group_id}",
        f"-DartifactId={project_name}",
        "-DarchetypeArtifactId=maven-archetype-quickstart",
        "-DinteractiveMode=false",
        "-Dmaven.compiler.source=23",
        "-Dmaven.compiler.target=23"
    ]

    run_maven_command(command)
    console.print(f"\n[bold green]✓[/bold green] Proyecto '{project_name}' creado exitosamente")

# Comandos comunes de Maven
@app.command()
def install():
    """Instala el artefacto en el repositorio local."""
    check_pom()
    show_banner()
    console.print("[cyan]Instalando artefacto localmente...[/cyan]\n")
    run_maven_command(["mvn", "install"])

@app.command()
def package():
    """Empaqueta el proyecto en un .jar hola mundo (equivale a 'mvn package')."""
    check_pom()
    show_banner()
    console.print("[green]Empaquetando proyecto...[/green]\n")
    run_maven_command(["mvn", "package"])

# ---- Punto de entrada ----
if __name__ == "__main__":
    app()
