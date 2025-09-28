#!/usr/bin/env python3
import argparse
import os
import json
import subprocess

# Mapeo de imágenes comunes y sus puertos por defecto
IMAGE_PORTS = {
    "mysql": "3306:3306",
    "postgres": "5432:5432",
    "mongo": "27017:27017",
    "redis": "6379:6379",
    "mariadb": "3307:3306"
}

def create_project(project_name, image, version):
    # --- Obtener usuario del sistema ---
    try:
        system_user = os.getlogin()
    except Exception:
        system_user = "joedoe"

    # --- Pedir contraseña del usuario ---
    user_password = input("👉 Ingresa la contraseña para el usuario (default: password): ").strip()
    if not user_password:
        user_password = "password"

    # --- Pedir descripción ---
    description = input("👉 Ingresa una descripción opcional: ").strip()
    if not description:
        description = "No description"

    # --- Determinar puerto ---
    if image in IMAGE_PORTS:
        port_mapping = IMAGE_PORTS[image]
    else:
        port_input = input(f"👉 No conozco la imagen '{image}'. Ingresa un puerto (ej. 1234:1234): ").strip()
        port_mapping = port_input if port_input else "8080:8080"

    # --- Crear carpeta ---
    project_dir = f"contenedor_{project_name}"
    os.makedirs(project_dir, exist_ok=True)

    # --- Contenido del docker-compose.yml ---
    compose_content = f"""version: "3.9"
services:
  db:
    image: {image}:{version}
    container_name: {project_name}_container
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 123456789
      MYSQL_DATABASE: {project_name}_db
      MYSQL_USER: {system_user}
      MYSQL_PASSWORD: {user_password}
    ports:
      - "{port_mapping}"
    volumes:
      - {project_name}_data:/var/lib/mysql

volumes:
  {project_name}_data:
"""

    compose_path = os.path.join(project_dir, "docker-compose.yml")
    with open(compose_path, "w") as f:
        f.write(compose_content)

    # --- Guardar info en JSON ---
    info = {
        "project_name": project_name,
        "image": image,
        "version": version,
        "system_user": system_user,
        "user_password": user_password,
        "root_password": "123456789",
        "database": f"{project_name}_db",
        "description": description,
        "volume": f"{project_name}_data",
        "container_name": f"{project_name}_container",
        "ports": port_mapping
    }

    info_path = os.path.join(project_dir, f"{project_name}_info.json")
    with open(info_path, "w") as f:
        json.dump(info, f, indent=4)

    print(f"✅ Proyecto creado en {project_dir}")
    print(f"📦 Configuración guardada en {info_path}")

    # --- Levantar contenedor ---
    try:
        subprocess.run(["docker", "compose", "-f", compose_path, "up", "-d"], check=True)
        print("🚀 Contenedor levantado en segundo plano (modo -d)")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al levantar el contenedor: {e}")

def get_up(project_name):
    project_dir = f"contenedor_{project_name}"
    compose_path = os.path.join(project_dir, "docker-compose.yml")

    if not os.path.exists(compose_path):
        print(f"❌ No se encontró {compose_path}. ¿Creaste el proyecto antes?")
        return

    try:
        subprocess.run(["docker", "compose", "-f", compose_path, "up", "-d"], check=True)
        print(f"🚀 Proyecto '{project_name}' levantado con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al levantar el proyecto: {e}")

def clean_all():
    try:
        # Detener todos los contenedores en ejecución
        running = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
        if running.stdout.strip():
            subprocess.run(["docker", "stop"] + running.stdout.split(), check=True)
            print("🛑 Todos los contenedores detenidos.")
        else:
            print("ℹ️ No había contenedores en ejecución.")

        # Eliminar todos los contenedores (detenidos + corriendo)
        all_containers = subprocess.run(["docker", "ps", "-aq"], capture_output=True, text=True)
        if all_containers.stdout.strip():
            subprocess.run(["docker", "rm"] + all_containers.stdout.split(), check=True)
            print("🧹 Todos los contenedores eliminados.")
        else:
            print("ℹ️ No había contenedores para eliminar.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al limpiar contenedores: {e}")

def main():
    parser = argparse.ArgumentParser(description="Helper CLI para contenedores Docker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Subcomando: new ---
    new_parser = subparsers.add_parser("new", help="Crear un nuevo contenedor con docker-compose")
    new_parser.add_argument("project_name", help="Nombre del proyecto")
    new_parser.add_argument("--image", required=True, help="Nombre de la imagen en Docker Hub (ej: mysql)")
    new_parser.add_argument("--version-image", default="latest", help="Versión de la imagen (default: latest)")

    # --- Subcomando: get-up ---
    up_parser = subparsers.add_parser("get-up", help="Levantar un proyecto existente con docker-compose")
    up_parser.add_argument("project_name", help="Nombre del proyecto a levantar")

    # --- Subcomando: clean ---
    subparsers.add_parser("clean", help="Detener y eliminar todos los contenedores")

    args = parser.parse_args()

    if args.command == "new":
        create_project(args.project_name, args.image, args.version_image)
    elif args.command == "get-up":
        get_up(args.project_name)
    elif args.command == "clean":
        clean_all()

if __name__ == "__main__":
    main()
