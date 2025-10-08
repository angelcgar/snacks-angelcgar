#!/usr/bin/env python3
"""
Script para organizar CVs por tecnología e idioma.
Toma un PDF y lo copia al directorio correspondiente basado en patrones del nombre.
"""

import os
import shutil
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, Optional


class CVOrganizer:
    """Organizador de CVs por tecnología e idioma."""

    def __init__(self, base_dir: str | None = None, name_prefix: str = "AngelContreras_Resumen"):
        """
        Inicializa el organizador de CVs.

        Args:
            base_dir: Directorio base donde organizar los CVs
            name_prefix: Prefijo para el nombre final del archivo
        """
        self.base_dir: Path = Path(base_dir or os.path.expanduser("~/Documentos/CVs"))
        self.name_prefix: str = name_prefix

        # Tecnologías y sus patrones de búsqueda
        self.tech_patterns: Dict[str, str] = {
            "react": r"react|React|jsx|JSX",
            "angular": r"angular|Angular|ng|NG",
            "vue": r"vue|Vue|vite|Vite",
            "python": r"python|Python|django|Django|flask|Flask",
            "java": r"java|Java|spring|Spring",
            "node": r"node|Node|express|Express",
            "php": r"php|PHP|laravel|Laravel",
            "net": r"net|NET|asp|ASP|csharp|CSharp"
        }

        # Patrones de idiomas mejorados
        self.language_patterns: Dict[str, str] = {
            "es": r"ES|es|Español|español|ESP|esp",
            "en": r"IN|in|EN|en|English|english|ING|ing"
        }

    def check_pdf_file(self, file_path: str) -> Path:
        """
        Verifica que el archivo exista y sea PDF.

        Args:
            file_path: Ruta del archivo a verificar

        Returns:
            Path del archivo verificado

        Raises:
            SystemExit: Si el archivo no existe o no es PDF
        """
        if not file_path:
            print("❌ Error: No se pasó ningún archivo.")
            sys.exit(1)

        path = Path(file_path)

        if not path.exists():
            print(f"❌ Error: El archivo '{file_path}' no existe.")
            sys.exit(1)

        if path.suffix.lower() != '.pdf':
            print(f"❌ Error: El archivo '{file_path}' no es un PDF.")
            sys.exit(1)

        return path

    def detect_technology(self, filename: str) -> str:
        """
        Detecta la tecnología basada en el nombre del archivo.

        Args:
            filename: Nombre del archivo a analizar

        Returns:
            Tecnología detectada o 'general' si no se encuentra ninguna
        """
        filename_lower = filename.lower()

        for tech, pattern in self.tech_patterns.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return tech

        return "general"

    def detect_language(self, filename: str) -> str:
        """
        Detecta el idioma basado en el nombre del archivo.

        Args:
            filename: Nombre del archivo a analizar

        Returns:
            Código de idioma detectado ('es' o 'en')

        Raises:
            SystemExit: Si no se puede detectar el idioma
        """
        for lang, pattern in self.language_patterns.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return lang

        print("❌ Error: No se pudo detectar el idioma.")
        print("💡 Usa 'ES', 'EN', 'español', 'english', etc. en el nombre del archivo.")
        sys.exit(1)

    def archive_file(self, source_file: Path) -> None:
        """
        Archiva el archivo original moviéndolo a ~/Documentos/archivos.

        Args:
            source_file: Archivo fuente a archivar
        """
        archive_dir = Path(os.path.expanduser("~/Dev/freelancer/programming/CVs/frontend"))
        archive_dir.mkdir(parents=True, exist_ok=True)

        archive_path = archive_dir / source_file.name

        # Si ya existe un archivo con el mismo nombre, añadir contador
        counter = 1
        original_archive_path = archive_path
        while archive_path.exists():
            stem = original_archive_path.stem
            suffix = original_archive_path.suffix
            archive_path = archive_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        try:
            shutil.move(str(source_file), str(archive_path))
            print(f"📦 Archivo archivado en: {archive_path}")
        except Exception as e:
            print(f"❌ Error al archivar el archivo: {e}")
            sys.exit(1)

    def copy_cv(self, source_file: Path, technology: str, language: str) -> None:
        """
        Copia el CV al directorio correspondiente.

        Args:
            source_file: Archivo fuente a copiar
            technology: Tecnología detectada
            language: Idioma detectado
        """
        # Crear directorio destino
        target_dir = self.base_dir / technology / language
        target_dir.mkdir(parents=True, exist_ok=True)

        # Nuevo nombre del archivo
        new_filename = f"{self.name_prefix}.pdf"
        target_path = target_dir / new_filename

        try:
            # Copiar archivo
            shutil.copy2(source_file, target_path)

            print("✅ Copiado exitosamente!")
            print(f"📁 Destino: {target_path}")
            print(f"💻 Tecnología: {technology} | 🌐 Idioma: {language}")

        except Exception as e:
            print(f"❌ Error al copiar el archivo: {e}")
            sys.exit(1)

    def show_help(self) -> None:
        """Muestra la ayuda del programa."""
        print("📋 Uso: python cv_organizer.py <archivo.pdf> [--archivar]")
        print("")
        print("Organiza CVs por tecnología e idioma:")
        print(f"  - Tecnologías detectadas: {', '.join(self.tech_patterns.keys())}")
        print("  - Idiomas: es (español), en (inglés)")
        print("")
        print("Opciones:")
        print("  --archivar    Mueve el archivo original a ~/Documentos/archivos")
        print("")
        print("Ejemplos de nombres:")
        print("  - CV_React_ES.pdf → ~/Documentos/CVs/react/es/")
        print("  - Resume_Angular_EN.pdf → ~/Documentos/CVs/angular/en/")
        print("  - Angel_Java_ESP.pdf → ~/Documentos/CVs/java/es/")
        print("")
        print("Patrones de detección de tecnologías:")
        for tech, pattern in self.tech_patterns.items():
            print(f"  - {tech}: {pattern}")
        print("")
        print("Patrones de detección de idiomas:")
        for lang, pattern in self.language_patterns.items():
            print(f"  - {lang}: {pattern}")

    def process_cv(self, file_path: str, archive: bool = False) -> None:
        """
        Procesa un CV: lo analiza y lo organiza.

        Args:
            file_path: Ruta del archivo CV a procesar
            archive: Si True, archiva el archivo original después del procesamiento
        """
        # Verificar archivo
        cv_file = self.check_pdf_file(file_path)

        # Detectar tecnología e idioma
        filename = cv_file.name
        technology = self.detect_technology(filename)
        language = self.detect_language(filename)

        print(f"🔍 Analizando: {filename}")
        print(f"💻 Tecnología detectada: {technology}")
        print(f"🌐 Idioma detectado: {language}")
        print("")

        # Copiar archivo
        self.copy_cv(cv_file, technology, language)

        # Archivar si se solicita
        if archive:
            print("")
            self.archive_file(cv_file)


def main() -> None:
    """Función principal del programa."""
    parser = argparse.ArgumentParser(
        description="Organiza CVs por tecnología e idioma",
        add_help=False
    )

    parser.add_argument('archivo', nargs='?', help='Archivo PDF a procesar')
    parser.add_argument('--archivar', action='store_true',
                       help='Mueve el archivo original a ~/Documentos/archivos')
    parser.add_argument('-h', '--help', action='store_true',
                       help='Muestra esta ayuda')

    # Manejo especial para mostrar ayuda personalizada
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help', 'help']):
        organizer = CVOrganizer()
        organizer.show_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.help:
        organizer = CVOrganizer()
        organizer.show_help()
        sys.exit(0)

    if not args.archivo:
        print("❌ Error: Debes especificar un archivo PDF.")
        organizer = CVOrganizer()
        organizer.show_help()
        sys.exit(1)

    # Procesar CV
    organizer = CVOrganizer()
    organizer.process_cv(args.archivo, args.archivar)


if __name__ == "__main__":
    main()
