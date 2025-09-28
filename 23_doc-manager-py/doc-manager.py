#!/usr/bin/env python3
"""
Document Manager with SQLite
- Documents table + Categories table
- File selection and copy by category
- CRUD for categories
- Update/Delete for documents
"""

import os
import sys
import sqlite3
import uuid
import shutil
from pathlib import Path
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
    MX_ZONE = ZoneInfo("America/Mexico_City")
except Exception:
    MX_ZONE = None

# Paths
DEST_DIR = Path.home() / "Documentos" / "archivos_personales_fisicos"
DB_PATH = DEST_DIR / "registry.db"
SOURCE_GLOB_DIR = Path.home() / "Descargas" / "carpeta_de_enbudo"


# ---------- Helpers ----------
def current_mx_datetime_iso() -> str:
    now = datetime.now(MX_ZONE) if MX_ZONE else datetime.now()
    return now.replace(microsecond=0).isoformat()


def init_db(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL,
            name TEXT NOT NULL,
            category_id INTEGER,
            date TEXT,
            physical_location TEXT,
            digital_file TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    # insert default categories if table empty
    cur = conn.execute("SELECT COUNT(*) FROM categories")
    count = cur.fetchone()[0]
    if count == 0:
        conn.executemany("INSERT INTO categories (name) VALUES (?)", [("Personal",), ("Trabajo",)])
    conn.commit()


def list_source_files(source_dir: Path = SOURCE_GLOB_DIR):
    if not source_dir.exists():
        return []
    return sorted([p for p in source_dir.rglob("*") if p.is_file()])


def copy_file_to_category(src: Path, category_name: str) -> Path:
    dest_dir = DEST_DIR / f"carpeta_{category_name}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src.name
    if dest_path.exists():
        base = dest_path.stem
        ext = dest_path.suffix
        i = 1
        while True:
            candidate = dest_dir / f"{base}_{i}{ext}"
            if not candidate.exists():
                dest_path = candidate
                break
            i += 1
    shutil.copy2(src, dest_path)
    return dest_path


# ---------- Category CRUD ----------
def list_categories(conn: sqlite3.Connection):
    rows = conn.execute("SELECT id, name FROM categories ORDER BY id").fetchall()
    return rows


def create_category(conn: sqlite3.Connection):
    name = input("New category name: ").strip()
    if not name:
        print("Category name required.")
        return
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Category '{name}' created.")
    except sqlite3.IntegrityError:
        print("Category already exists.")


def update_category(conn: sqlite3.Connection):
    rows = list_categories(conn)
    if not rows:
        print("No categories.")
        return
    for idx, r in enumerate(rows):
        print(f"[{idx}] {r[1]}")
    try:
        sel = int(input("Select category to update: "))
        if sel < 0 or sel >= len(rows):
            print("Invalid choice.")
            return
    except ValueError:
        return
    new_name = input("New name: ").strip()
    if not new_name:
        print("Empty name not allowed.")
        return
    conn.execute("UPDATE categories SET name=? WHERE id=?", (new_name, rows[sel][0]))
    conn.commit()
    print("Category updated.")


def delete_category(conn: sqlite3.Connection):
    rows = list_categories(conn)
    if not rows:
        print("No categories.")
        return
    for idx, r in enumerate(rows):
        print(f"[{idx}] {r[1]}")
    try:
        sel = int(input("Select category to delete: "))
        if sel < 0 or sel >= len(rows):
            print("Invalid choice.")
            return
    except ValueError:
        return
    conn.execute("DELETE FROM categories WHERE id=?", (rows[sel][0],))
    conn.commit()
    print("Category deleted.")


# ---------- Document CRUD ----------
def create_entry(conn: sqlite3.Connection):
    print("\n--- Create new document entry ---")
    name = input("Name (title): ").strip()
    if not name:
        print("Name is required.")
        return

    # choose category
    cats = list_categories(conn)
    if not cats:
        print("No categories available.")
        return
    for idx, c in enumerate(cats):
        print(f"[{idx}] {c[1]}")
    try:
        cat_sel = int(input("Select category: "))
        if cat_sel < 0 or cat_sel >= len(cats):
            print("Invalid category.")
            return
    except ValueError:
        return
    category_id, category_name = cats[cat_sel]

    physical_location = input("Physical location: ").strip() or "Unknown"

    # select file
    files = list_source_files()
    digital_file_rel = ""
    if files:
        for idx, f in enumerate(files, start=1):
            print(f"{idx}) {f.relative_to(Path.home())}")
        print("0) No digital file")
        try:
            sel = int(input("Select file number: "))
        except ValueError:
            sel = 0
        if sel > 0 and 1 <= sel <= len(files):
            src = files[sel - 1]
            copied = copy_file_to_category(src, category_name)
            digital_file_rel = str(copied)
            print(f"Copied to: {digital_file_rel}")

    new_uuid = str(uuid.uuid4())
    date_iso = current_mx_datetime_iso()

    # BUG: category_id is not defined
    conn.execute("""
        INSERT INTO documents (uuid, name, category_id, date, physical_location, digital_file)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (new_uuid, name, category_id, date_iso, physical_location, digital_file_rel))
    conn.commit()
    print(f"Saved entry with uuid={new_uuid}")


def list_all(conn: sqlite3.Connection):
    rows = conn.execute("""
        SELECT d.id, d.name, c.name, d.digital_file
        FROM documents d LEFT JOIN categories c ON d.category_id = c.id
    """).fetchall()
    if not rows:
        print("\nNo entries.")
        return
    print(f"\nEntries ({len(rows)}):")
    for r in rows:
        print(f" - [{r[0]}] {r[1]} | category: {r[2] or '-'} | digital: {bool(r[3])}")


def search_by_name(conn: sqlite3.Connection, term: str):
    term = f"%{term.lower()}%"
    rows = conn.execute("""
        SELECT d.id, d.name, d.physical_location, d.digital_file
        FROM documents d
        LEFT JOIN categories c ON d.category_id = c.id
        WHERE LOWER(d.name) LIKE ? OR LOWER(c.name) LIKE ?
    """, (term, term)).fetchall()
    if not rows:
        print("No matches.")
        return
    for r in rows:
        print(f"[{r[0]}] {r[1]} | physical: {r[2]} | digital: {r[3] or '—'}")


def update_entry(conn: sqlite3.Connection):
    list_all(conn)
    try:
        doc_id = int(input("Document id to update: "))
    except ValueError:
        return
    row = conn.execute("SELECT id, name, physical_location FROM documents WHERE id=?", (doc_id,)).fetchone()
    if not row:
        print("Not found.")
        return
    new_name = input(f"New name (leave empty to keep '{row[1]}'): ").strip() or row[1]
    new_phys = input(f"New physical location (leave empty to keep '{row[2]}'): ").strip() or row[2]
    conn.execute("UPDATE documents SET name=?, physical_location=? WHERE id=?", (new_name, new_phys, doc_id))
    conn.commit()
    print("Document updated.")


def delete_entry(conn: sqlite3.Connection):
    list_all(conn)
    try:
        doc_id = int(input("Document id to delete: "))
    except ValueError:
        return
    conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
    conn.commit()
    print("Document deleted.")


# ---------- Menu ----------
def print_menu():
    print(" Document Manager (SQLite) ".center(80, "="))
    print("1) Create new document")
    print("2) List all documents")
    print("3) Search documents")
    print("4) Update document")
    print("5) Delete document")
    print("--- Categories ---")
    print("6) List categories")
    print("7) Create category")
    print("8) Update category")
    print("9) Delete category")
    print("0) Exit")


def main():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    while True:
        print_menu()
        choice = input("Choose: ").strip()
        if choice == "1":
            create_entry(conn)
        elif choice == "2":
            list_all(conn)
        elif choice == "3":
            term = input("Search term: ").strip()
            if term:
                search_by_name(conn, term)
        elif choice == "4":
            update_entry(conn)
        elif choice == "5":
            delete_entry(conn)
        elif choice == "6":
            for c in list_categories(conn):
                print(f"[{c[0]}] {c[1]}")
        elif choice == "7":
            create_category(conn)
        elif choice == "8":
            update_category(conn)
        elif choice == "9":
            delete_category(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option.")

    conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
