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

# ---- Punto de entrada ----
if __name__ == "__main__":
    app()
