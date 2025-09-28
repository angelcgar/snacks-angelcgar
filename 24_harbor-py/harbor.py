#!/usr/bin/env python3
import argparse
import os
import json
import subprocess

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
      - "3306:3306"
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
        "container_name": f"{project_name}_container"
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

def main():
    parser = argparse.ArgumentParser(description="Helper CLI para contenedores Docker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Subcomando: new ---
    new_parser = subparsers.add_parser("new", help="Crear un nuevo contenedor con docker-compose")
    new_parser.add_argument("project_name", help="Nombre del proyecto")
    new_parser.add_argument("--image", required=True, help="Nombre de la imagen en Docker Hub (ej: mysql)")
    new_parser.add_argument("--version-image", default="latest", help="Versión de la imagen (default: latest)")

    args = parser.parse_args()

    if args.command == "new":
        create_project(args.project_name, args.image, args.version_image)

if __name__ == "__main__":
    main()
