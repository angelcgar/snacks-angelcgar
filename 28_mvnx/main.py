#!/usr/bin/env python3

import subprocess
import typer
import os
import glob
import threading
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

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

# ---- Función auxiliar para buscar clases Java ----
def find_java_class(class_name: str) -> str:
    """Busca un archivo Java por nombre y devuelve el nombre completo de la clase."""
    try:
        # Buscar archivos .java que coincidan con el nombre
        result = subprocess.run(
            ["find", ".", "-name", f"{class_name}.java", "-type", "f"],
            capture_output=True,
            text=True,
            check=True
        )

        files = result.stdout.strip().split('\n')
        files = [f for f in files if f]  # Filtrar líneas vacías

        if not files:
            console.print(f"[bold red]❌ No se encontró ninguna clase con ese nombre[/bold red]")
            raise typer.Exit(1)

        # Tomar el primer archivo encontrado
        java_file = files[0]

        # Convertir path a nombre de clase Java
        # Ejemplo: ./src/main/java/com/gm/App.java -> com.gm.App
        class_path = java_file.replace("./", "").replace(".java", "")

        # Remover src/main/java del path si está presente
        if "src/main/java/" in class_path:
            class_path = class_path.replace("src/main/java/", "")

        # Convertir separadores de directorio a puntos
        class_path = class_path.replace("/", ".")

        return class_path

    except subprocess.CalledProcessError:
        console.print(f"[bold red]❌ No se encontró ninguna clase con ese nombre[/bold red]")
        raise typer.Exit(1)

# ---- Función de verificación de pom.xml ----
def check_pom():
    """Verifica si existe el archivo pom.xml en el directorio actual."""
    if not os.path.exists("pom.xml"):
        console.print("[bold red]⚠️ No se encontró pom.xml en el directorio actual.[/bold red]")
        raise typer.Exit(1)

# ---- Función para ejecutar comandos Maven con manejo de errores y barra de progreso ----
def run_maven_command(command: list, description: str = "comando Maven", show_progress: bool = True):
    """Ejecuta un comando Maven con manejo de errores, modo verbose y barra de progreso."""
    # Agregar -q si no está en modo verbose y no está ya presente
    if not verbose_mode and "-q" not in command:
        command.insert(1, "-q")

    if show_progress and not verbose_mode:
        # Ejecutar con barra de progreso
        _run_with_progress(command, description)
    else:
        # Ejecutar sin barra de progreso (modo verbose o sin progreso)
        result = subprocess.run(command)
        if result.returncode != 0:
            console.print(f"[bold red]❌ Error: el comando de Maven falló.[/bold red]")
            raise typer.Exit(1)

def _run_with_progress(command: list, description: str):
    """Ejecuta un comando con barra de progreso animada."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=False,
    ) as progress:

        # Crear tarea de progreso
        task = progress.add_task(f"[cyan]{description}[/cyan]", total=100)

        # Variables compartidas entre hilos
        process_result = {"returncode": 0}
        process_finished = threading.Event()

        def run_process():
            """Ejecuta el proceso en un hilo separado."""
            result = subprocess.run(command, capture_output=not verbose_mode)
            process_result["returncode"] = result.returncode
            process_finished.set()

        # Iniciar el proceso en un hilo separado
        process_thread = threading.Thread(target=run_process)
        process_thread.start()

        # Animar la barra de progreso mientras el proceso se ejecuta
        progress_value = 0
        while not process_finished.is_set():
            if progress_value < 90:
                progress_value += 2
                progress.update(task, completed=progress_value)
            time.sleep(0.1)

        # Esperar a que el proceso termine completamente
        process_thread.join()

        # Actualizar la barra según el resultado
        if process_result["returncode"] == 0:
            progress.update(task, completed=100, description="[green]✅ Tarea completada[/green]")
            time.sleep(0.5)  # Mostrar el éxito brevemente
        else:
            progress.update(task, completed=progress_value, description="[red]❌ Error durante la ejecución[/red]")
            time.sleep(1)  # Mostrar el error un poco más tiempo
            console.print(f"[bold red]❌ Error: el comando de Maven falló.[/bold red]")
            raise typer.Exit(1)

# ---- Comandos principales ----
@app.command()
def run(main: str = typer.Argument(..., help="Clase principal a ejecutar, ej. com.gm.App")):
    """Ejecuta una clase principal de Maven."""
    check_pom()
    show_banner()
    console.print(f"[cyan]Ejecutando clase:[/cyan] {main}\n")
    run_maven_command(["mvn", "exec:java", f"-Dexec.mainClass={main}"], f"Ejecutando {main}", False)

@app.command()
def clean():
    """Limpia el proyecto Maven (equivale a 'mvn clean')."""
    check_pom()
    show_banner()
    console.print("[yellow]Limpiando proyecto...[/yellow]\n")
    run_maven_command(["mvn", "clean"], "Limpiando archivos generados")

@app.command()
def build():
    """Compila el proyecto Maven (equivale a 'mvn compile')."""
    check_pom()
    show_banner()
    console.print("[green]Compilando proyecto...[/green]\n")
    run_maven_command(["mvn", "compile"], "Compilando código fuente")
# BUG: Este comando no muestra la info del proyecto
@app.command()
def info():
    """Muestra información básica del proyecto Maven."""
    check_pom()
    show_banner()
    run_maven_command(["mvn", "help:effective-pom"], "Obteniendo información del proyecto", False)
# Comando por probar
@app.command()
def test():
    """Ejecuta las pruebas del proyecto Maven (equivale a 'mvn test')."""
    check_pom()
    show_banner()
    console.print("[magenta]Ejecutando pruebas...[/magenta]\n")
    run_maven_command(["mvn", "test"], "Ejecutando suite de pruebas")

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

    run_maven_command(command, "Generando estructura del proyecto")
    console.print(f"\n[bold green]✓[/bold green] Proyecto '{project_name}' creado exitosamente")

# Comandos comunes de Maven
@app.command()
def install():
    """Instala el artefacto en el repositorio local."""
    check_pom()
    show_banner()
    console.print("[cyan]Instalando artefacto localmente...[/cyan]\n")
    run_maven_command(["mvn", "install"], "Instalando en repositorio local")

@app.command()
def package():
    """Empaqueta el proyecto en un .jar hola mundo (equivale a 'mvn package')."""
    check_pom()
    show_banner()
    console.print("[green]Empaquetando proyecto...[/green]\n")
    run_maven_command(["mvn", "package"], "Empaquetando en archivo JAR")

@app.command()
def status():
    """Muestra versiones y entorno Maven/Java."""
    show_banner()
    console.print("[cyan]Versión de Maven:[/cyan]")
    subprocess.run(["mvn", "-v"])
    console.print("\n[cyan]Versión de Java:[/cyan]")
    subprocess.run(["java", "-version"])

# ---- Alias de comandos (versiones cortas) ----
@app.command("c")
def build_alias():
    """Alias para 'build': Compila el proyecto Maven."""
    build()

@app.command("r")
def run_alias(class_name: str = typer.Argument(..., help="Nombre de la clase a ejecutar, ej. App")):
    """Alias para 'run': Ejecuta una clase principal buscándola automáticamente."""
    check_pom()

    # Buscar y obtener el nombre completo de la clase
    full_class_name = find_java_class(class_name)

    # Ejecutar la clase encontrada
    show_banner()
    console.print(f"[cyan]Ejecutando clase:[/cyan] {full_class_name}\n")
    run_maven_command(["mvn", "exec:java", f"-Dexec.mainClass={full_class_name}"], f"Ejecutando {class_name}", False)

@app.command("t")
def test_alias():
    """Alias para 'test': Ejecuta las pruebas del proyecto."""
    test()

@app.command("cl")
def clean_alias():
    """Alias para 'clean': Limpia el proyecto Maven."""
    clean()

@app.command("p")
def package_alias():
    """Alias para 'package': Empaqueta el proyecto en un JAR."""
    package()

@app.command("i")
def install_alias():
    """Alias para 'install': Instala el artefacto en el repositorio local."""
    install()


# ---- Punto de entrada ----
if __name__ == "__main__":
    app()
