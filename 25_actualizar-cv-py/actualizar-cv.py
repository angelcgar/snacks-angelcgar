#!/usr/bin/env python3
"""
Script para organizar CVs por tecnología e idioma.
Toma un PDF y lo copia al directorio correspondiente basado en patrones del nombre.
"""

import os
import shutil
import sys
import re
from pathlib import Path
from typing import Dict, Optional


class CVOrganizer:
    """Organizador de CVs por tecnología e idioma."""

    def __init__(self, base_dir: str = None, name_prefix: str = "AngelContreras_Resumen"):
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
            "en": r"IN|in|EN|en|English|english|ING|ing"  # Corregido: 'en' en lugar de 'in'
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
        print("📋 Uso: python cv_organizer.py <archivo.pdf>")
        print("")
        print("Organiza CVs por tecnología e idioma:")
        print(f"  - Tecnologías detectadas: {', '.join(self.tech_patterns.keys())}")
        print("  - Idiomas: es (español), en (inglés)")
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

    def process_cv(self, file_path: str) -> None:
        """
        Procesa un CV: lo analiza y lo organiza.

        Args:
            file_path: Ruta del archivo CV a procesar
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


def main() -> None:
    """Función principal del programa."""
    # Verificar argumentos
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help', 'help']:
        organizer = CVOrganizer()
        organizer.show_help()
        sys.exit(0 if len(sys.argv) == 2 else 1)

    # Procesar CV
    organizer = CVOrganizer()
    organizer.process_cv(sys.argv[1])


if __name__ == "__main__":
    main()
