#!/usr/bin/env python3
"""
Simple console tool to register scanned documents.
- English names for variables/functions.
- Saves registry as JSON.
- Lists files under ~/Descargas/carpeta_de_enbudo/** for selection and copies chosen file to
  ~/Documentos/archivos_personales_fisicos (creates folder if needed).
"""

from __future__ import annotations
import os
import sys
import json
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Try to use ZoneInfo for Mexico time; fallback to system local time if unavailable.
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
    MX_ZONE = ZoneInfo("America/Mexico_City")
except Exception:
    MX_ZONE = None  # fallback


# Configuration (adjust if you want)
SOURCE_GLOB_DIR = Path.home() / "Descargas" / "carpeta_de_enbudo"
DEST_DIR = Path.home() / "Documentos" / "archivos_personales_fisicos"
REGISTRY_PATH = DEST_DIR / "registry.json"


# ---------- Basic JSON DB helpers ----------
def load_db(registry_path: Path = REGISTRY_PATH) -> List[Dict]:
    if registry_path.exists():
        try:
            return json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_db(entries: List[Dict], registry_path: Path = REGISTRY_PATH) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_id(entries: List[Dict]) -> int:
    if not entries:
        return 1
    max_id = max((e.get("id", 0) for e in entries))
    return int(max_id) + 1


def current_mx_datetime_iso() -> str:
    now = datetime.now(MX_ZONE) if MX_ZONE else datetime.now()
    # ISO format without microseconds
    return now.replace(microsecond=0).isoformat()


# ---------- File utilities ----------
def list_source_files(source_dir: Path = SOURCE_GLOB_DIR) -> List[Path]:
    if not source_dir.exists():
        return []
    # List files recursively
    return sorted([p for p in source_dir.rglob("*") if p.is_file()])


def copy_file_to_dest(src: Path, dest_dir: Path = DEST_DIR) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src.name
    # If filename already exists, avoid overwrite by adding a numeric suffix
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


# ---------- Core: create an entry ----------
def create_entry_interactive() -> Optional[Dict]:
    print("\n--- Create new document entry ---")

    name: str = input("Name (title): ").strip()
    if not name:
        print("Name is required. Aborting create.")
        return None

    category: str = input("Category (text): ").strip()

    physical_location: str = input("Physical location (text): ").strip()
    if not physical_location:
        physical_location = "Unknown"

    # List available files to pick as digital_file
    files = list_source_files()
    digital_file_path: Optional[Path] = None
    if files:
        print(f"\nFound {len(files)} file(s) in: {SOURCE_GLOB_DIR}")
        for idx, p in enumerate(files, start=1):
            print(f"  {idx}) {p.relative_to(Path.home())}")
        print("  0) No digital file / skip")
        try:
            choice = input("Select file number to attach as digital_file (0 to skip): ").strip()
            sel = int(choice) if choice else 0
        except ValueError:
            sel = 0
        if sel > 0 and 1 <= sel <= len(files):
            digital_file_path = files[sel - 1]
            try:
                copied = copy_file_to_dest(digital_file_path)
                print(f"Copied to: {copied}")
                digital_file_rel = str(copied)
            except Exception as e:
                print(f"Error copying file: {e}")
                digital_file_rel = ""
        else:
            digital_file_rel = ""
    else:
        print(f"No files found under {SOURCE_GLOB_DIR} (or folder missing).")
        digital_file_rel = ""

    # Prepare entry
    entries = load_db()
    new_id = generate_id(entries)
    new_uuid = str(uuid.uuid4())

    date_iso: str = current_mx_datetime_iso()

    entry: Dict = {
        "id": int(new_id),                # basic int id
        "uuid": new_uuid,                 # unique uuid
        "name": name,                     # user provided
        "category": category,             # user provided
        "date": date_iso,                 # iso datetime
        "physical_location": physical_location,  # text
        "digital_file": digital_file_rel, # path or empty string
    }

    entries.append(entry)
    save_db(entries)
    print(f"\nSaved entry id={new_id}, uuid={new_uuid}\n")
    return entry


# ---------- Simple list and search ----------
def list_all_entries() -> None:
    entries = load_db()
    if not entries:
        print("\nNo entries saved yet.")
        return
    print(f"\nRegistry entries ({len(entries)}):")
    for e in entries:
        print(f" - [{e.get('id')}] {e.get('name')}  | category: {e.get('category') or '-'}  | digital: {bool(e.get('digital_file'))}")


def filter_documents_by_name(term: str) -> None:
    term_lower = term.lower()
    entries = load_db()
    found = [e for e in entries if term_lower in (e.get("name", "").lower() + " " + (e.get("category") or "").lower())]
    if not found:
        print("\nNo matching documents.")
        return
    print(f"\nFound {len(found)} result(s):")
    for e in found:
        print(f" - [{e.get('id')}] {e.get('name')}  | physical: {e.get('physical_location')}  | digital: {e.get('digital_file') or '—'}")


# ---------- Console menu ----------
def print_menu() -> None:
    print("\n=== Document Manager ===")
    print("1) Create new entry")
    print("2) List all entries")
    print("3) Search by name/category (filter_documents_by_name)")
    print("0) Exit")


def main() -> None:
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            create_entry_interactive()
        elif choice == "2":
            list_all_entries()
        elif choice == "3":
            term = input("Search term: ").strip()
            if term:
                filter_documents_by_name(term)
            else:
                print("Empty search term.")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
