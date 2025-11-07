#!/usr/bin/env python3

import subprocess
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(add_completion=False)
console = Console()

# ---- Banner inicial ----
def show_banner():
    console.print(Panel.fit("[bold blue]mvnx[/bold blue] — Maven CLI mejorado\n[dim]Por Angel Contreras[/dim]"))

# ---- Comandos principales ----
@app.command()
def run(main: str = typer.Argument(..., help="Clase principal a ejecutar, ej. com.gm.App")):
    """Ejecuta una clase principal de Maven."""
    show_banner()
    console.print(f"[cyan]Ejecutando clase:[/cyan] {main}\n")
    subprocess.run(["mvn", "-q", "exec:java", f"-Dexec.mainClass={main}"])

@app.command()
def clean():
    """Limpia el proyecto Maven (equivale a 'mvn clean')."""
    show_banner()
    console.print("[yellow]Limpiando proyecto...[/yellow]\n")
    subprocess.run(["mvn", "clean"])

@app.command()
def build():
    """Compila el proyecto Maven (equivale a 'mvn compile')."""
    show_banner()
    console.print("[green]Compilando proyecto...[/green]\n")
    subprocess.run(["mvn", "compile"])

@app.command()
def info():
    """Muestra información básica del proyecto Maven."""
    show_banner()
    subprocess.run(["mvn", "-q", "help:effective-pom"])

@app.command()
def test():
    """Ejecuta las pruebas del proyecto Maven (equivale a 'mvn test')."""
    show_banner()
    console.print("[magenta]Ejecutando pruebas...[/magenta]\n")
    subprocess.run(["mvn", "test"])

@app.command()
def create(
    group_id: str = typer.Argument(..., help="Group ID del proyecto, ej. com.gm"),
    project_name: str = typer.Argument(..., help="Nombre del proyecto (artifactId)")
):
    """Crea un nuevo proyecto Maven con Java 23."""
    show_banner()
    console.print(f"[green]Creando proyecto Maven:[/green] {project_name}")
    console.print(f"[cyan]Group ID:[/cyan] {group_id}\n")

    subprocess.run([
        "mvn", "archetype:generate",
        f"-DgroupId={group_id}",
        f"-DartifactId={project_name}",
        "-DarchetypeArtifactId=maven-archetype-quickstart",
        "-DinteractiveMode=false",
        "-Dmaven.compiler.source=23",
        "-Dmaven.compiler.target=23"
    ])

    console.print(f"\n[bold green]✓[/bold green] Proyecto '{project_name}' creado exitosamente")

# Comandos comunes de Maven
@app.command()
def install():
    """Instala el artefacto en el repositorio local."""
    show_banner()
    console.print("[cyan]Instalando artefacto localmente...[/cyan]\n")
    subprocess.run(["mvn", "install"])

@app.command()
def package():
    """Empaqueta el proyecto en un .jar (equivale a 'mvn package')."""
    show_banner()
    console.print("[green]Empaquetando proyecto...[/green]\n")
    subprocess.run(["mvn", "package"])

# ---- Punto de entrada ----
if __name__ == "__main__":
    app()
