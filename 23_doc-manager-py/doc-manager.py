#!/usr/bin/env python3
"""
Document Manager with SQLite backend.
- Keeps same logic as JSON version.
- Uses sqlite3 (stdlib, no dependencies).
"""

import os
import sys
import sqlite3
import uuid
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
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            date TEXT,
            physical_location TEXT,
            digital_file TEXT
        )
    """)
    conn.commit()

def create_entry(conn: sqlite3.Connection):
    print("\n--- Create new document entry ---")
    name = input("Name (title): ").strip()
    if not name:
        print("Name is required.")
        return

    category = input("Category: ").strip()
    physical_location = input("Physical location: ").strip() or "Unknown"

    # skip file selection for brevity
    digital_file = input("Digital file path (optional, leave empty if none): ").strip()

    new_uuid = str(uuid.uuid4())
    date_iso = current_mx_datetime_iso()

    conn.execute("""
        INSERT INTO documents (uuid, name, category, date, physical_location, digital_file)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (new_uuid, name, category, date_iso, physical_location, digital_file))
    conn.commit()

    print(f"Saved entry with uuid={new_uuid}")

def list_all(conn: sqlite3.Connection):
    rows = conn.execute("SELECT id, name, category, digital_file FROM documents").fetchall()
    if not rows:
        print("\nNo entries yet.")
        return
    print(f"\nEntries ({len(rows)}):")
    for r in rows:
        print(f" - [{r[0]}] {r[1]} | category: {r[2] or '-'} | digital: {bool(r[3])}")

def search_by_name(conn: sqlite3.Connection, term: str):
    term = f"%{term.lower()}%"
    rows = conn.execute("""
        SELECT id, name, physical_location, digital_file
        FROM documents
        WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ?
    """, (term, term)).fetchall()
    if not rows:
        print("\nNo matches.")
        return
    print(f"\nFound {len(rows)} result(s):")
    for r in rows:
        print(f" - [{r[0]}] {r[1]} | physical: {r[2]} | digital: {r[3] or '—'}")

def print_menu():
    print("\n=== Document Manager (SQLite) ===")
    print("1) Create new entry")
    print("2) List all entries")
    print("3) Search by name/category")
    print("0) Exit")

def main():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    while True:
        print_menu()
        choice = input("Choose option: ").strip()
        if choice == "1":
            create_entry(conn)
        elif choice == "2":
            list_all(conn)
        elif choice == "3":
            term = input("Search term: ").strip()
            if term:
                search_by_name(conn, term)
        elif choice == "0":
            print("\nGoodbye.")
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
