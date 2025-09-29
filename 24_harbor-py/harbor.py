#!/usr/bin/env python3
import argparse
import os
import json
import subprocess

# Mapeo de imágenes comunes y sus puertos por defecto
IMAGE_PORTS = {
    "mysql": 3306,
    "postgres": 5432,
    "mongo": 27017,
    "redis": 6379,
    "mariadb": 3307
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

    # --- Crear carpeta ---
    project_dir = f"contenedor_{project_name}"
    os.makedirs(project_dir, exist_ok=True)

    # --- Variables base ---
    root_password = "123456789"
    db_name = f"{project_name}_db"
    container_name = f"{project_name}_container"
    volume_name = f"{project_name}_data"

    if image in IMAGE_PORTS:
        port = IMAGE_PORTS[image]
    else:
        try:
            port = int(input(f"👉 Ingresa el puerto a mapear para {image}: ").strip())
        except ValueError:
            raise SystemExit("❌ Debes ingresar un número de puerto válido")

    # --- docker-compose.yml ---
    compose_content = f"""version: "3.9"
services:
  db:
    image: {image}:{version}
    container_name: {container_name}
    restart: always
    environment:
      {"MYSQL_ROOT_PASSWORD" if image=="mysql" else "POSTGRES_PASSWORD" if image=="postgres" else "MONGO_INITDB_ROOT_PASSWORD"}: {root_password}
      {"MYSQL_DATABASE" if image=="mysql" else "POSTGRES_DB" if image=="postgres" else "MONGO_INITDB_DATABASE"}: {db_name}
      {"MYSQL_USER" if image=="mysql" else "POSTGRES_USER" if image=="postgres" else "MONGO_INITDB_ROOT_USERNAME"}: {system_user}
      {"MYSQL_PASSWORD" if image=="mysql" else "POSTGRES_PASSWORD" if image=="postgres" else "MONGO_INITDB_ROOT_PASSWORD"}: {user_password}
    ports:
      - "{port}:{port}"
    volumes:
      - {volume_name}:/var/lib/{image}
volumes:
  {volume_name}:
    name: {volume_name}
"""

    compose_path = os.path.join(project_dir, "docker-compose.yml")
    with open(compose_path, "w") as f:
        f.write(compose_content)

    # --- URLs de conexión ---
    connection_urls = {}
    if image == "mysql":
        connection_urls["root"] = f"mysql://root:{root_password}@localhost:{port}/{db_name}"
        connection_urls["user"] = f"mysql://{system_user}:{user_password}@localhost:{port}/{db_name}"
    elif image == "postgres":
        connection_urls["root"] = f"postgresql://postgres:{root_password}@localhost:{port}/{db_name}"
        connection_urls["user"] = f"postgresql://{system_user}:{user_password}@localhost:{port}/{db_name}"
    elif image == "mongo":
        connection_urls["root"] = f"mongodb://root:{root_password}@localhost:{port}/{db_name}"
        connection_urls["user"] = f"mongodb://{system_user}:{user_password}@localhost:{port}/{db_name}"
    else:
        connection_urls["info"] = f"{image} no soportado aún para URLs automáticas."

    # --- Guardar info en JSON ---
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

    print(f"✅ Proyecto creado en {project_dir}")
    print(f"📦 Configuración guardada en {info_path}")

    # --- Levantar contenedor ---
    try:
        subprocess.run(["docker", "compose", "-f", compose_path, "up", "-d"], check=True)
        print("🚀 Contenedor levantado en segundo plano (modo -d)")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al levantar el contenedor: {e}")

    # --- Crear archivo seed.sql ---
    seed_path = os.path.join(project_dir, "seed.sql")
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
    with open(seed_path, "w") as f:
        f.write(seed_content)

    print(f"📝 Archivo seed.sql creado en {seed_path}")


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
