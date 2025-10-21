#!/usr/bin/env python3
import os
import json
import uuid
from PIL import Image
import instaloader

# Configuración
OUTPUT_DIR = "img"
DB_FILE = "imagenes-db.json"

def descargar_fotos(usuario: str):
    """Descarga todas las fotos de un perfil de IG y devuelve la lista de rutas"""
    L = instaloader.Instaloader(dirname_pattern=OUTPUT_DIR, download_videos=False, save_metadata=False, post_metadata_txt_pattern="")
    profile = instaloader.Profile.from_username(L.context, usuario)

    rutas = []
    for post in profile.get_posts():
        # Descargar post (solo imagen principal, no galería completa)
        L.download_post(post, target=usuario)
        for file in os.listdir(os.path.join(OUTPUT_DIR, usuario)):
            if file.endswith((".jpg", ".jpeg", ".png")):
                rutas.append(os.path.join(OUTPUT_DIR, usuario, file))
    return rutas


def generar_json(rutas: list[str]):
    """Genera un JSON con los datos de cada imagen"""
    data = []
    for path in rutas:
        try:
            with Image.open(path) as img:
                width, height = img.size

            data.append({
                "id": str(uuid.uuid4())[:8].upper(),   # ID único corto
                "title": os.path.splitext(os.path.basename(path))[0].upper(),
                "image": path,
                "width": width,
                "height": height
            })
        except Exception as e:
            print(f"⚠ No se pudo procesar {path}: {e}")

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✔ JSON generado en {DB_FILE}")


def main():
    usuario = input("Introduce tu usuario de Instagram: ").strip()
    rutas = descargar_fotos(usuario)
    generar_json(rutas)


if __name__ == "__main__":
    main()
