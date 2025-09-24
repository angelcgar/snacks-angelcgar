#!/usr/bin/env python3

import argparse
import os
import sys
import json
import subprocess
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

# Ruta para guardar la mini base de datos local
DB_PATH = Path.home() / ".local" / "share" / "md-notes" / "db.json"


# -------------------------
# Función: convertir md a pdf
# -------------------------
def md_to_pdf(md_file: str):
    # Verificar que el archivo existe
    if not os.path.exists(md_file):
        print(f"Error: el archivo '{md_file}' no existe.")
        sys.exit(1)

    if not md_file.endswith(".md"):
        print("Error: el archivo debe tener extensión .md")
        sys.exit(1)

    # Leer contenido del archivo .md
    with open(md_file, encoding="utf-8") as f:
        text = f.read()

    # Crear PDF
    pdf = MarkdownPdf(toc_level=2, optimize=True)

    # CSS genérico estilo Google Docs
    css = """
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 2cm;
    }
    h1, h2, h3, h4 {
        text-align: center;
        font-weight: bold;
    }
    p {
        text-align: justify;
    }
    """

    pdf.add_section(Section(text, paper_size="A4"), user_css=css)

    output_file = os.path.splitext(md_file)[0] + ".pdf"
    pdf.save(output_file)
    print(f"✅ Convertido: {output_file}")


# -------------------------
# Funciones para "note"
# -------------------------
def load_db():
    """Carga la base de datos desde disco"""
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"notes": []}


def save_db(db):
    """Guarda la base de datos en disco"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def add_note(path: str):
    """Agrega una nota .md a la base de datos"""
    abs_path = str(Path(path).resolve())
    if not abs_path.endswith(".md"):
        print("Error: solo se permiten archivos con extensión .md")
        sys.exit(1)

    db = load_db()
    if abs_path not in db["notes"]:
        db["notes"].append(abs_path)
        save_db(db)
        print(f"✅ Nota añadida: {abs_path}")
    else:
        print("La nota ya estaba en la base de datos.")


def list_notes():
    """Lista las notas guardadas"""
    db = load_db()
    if not db["notes"]:
        print("No hay notas guardadas.")
        return

    for i, note in enumerate(db["notes"], start=1):
        name = Path(note).name
        if not name.endswith(".md"):
            print(f"⚠️ Archivo inválido en DB: {note}")
            continue
        print(f"{i}. {name}")


def view_note(note_name: str):
    """Ejecuta mdcat sobre una nota específica"""
    db = load_db()
    for note in db["notes"]:
        if Path(note).name == note_name:
            subprocess.run(["mdcat", note])
            return
    print(f"❌ Nota '{note_name}' no encontrada en la base de datos.")


# -------------------------
# CLI principal
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Markdown CLI utility")
    subparsers = parser.add_subparsers(dest="command")

    # Subcomando para convertir md a pdf
    parser_pdf = subparsers.add_parser("pdf", help="Convertir archivo .md a .pdf")
    parser_pdf.add_argument("file", help="Archivo .md a convertir")

    # Subcomando "note"
    parser_note = subparsers.add_parser("note", help="Gestionar notas")
    parser_note.add_argument("--add", help="Añadir nota (.md)")
    parser_note.add_argument("--list", action="store_true", help="Listar notas")
    parser_note.add_argument("--view", help="Ver nota con mdcat (usar nombre del archivo)")

    args = parser.parse_args()

    if args.command == "pdf":
        md_to_pdf(args.file)

    elif args.command == "note":
        if args.add:
            add_note(args.add)
        elif args.list:
            list_notes()
        elif args.view:
            view_note(args.view)
        else:
            parser_note.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
