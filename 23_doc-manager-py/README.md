# README

## Resumen
Herramienta de consola en **Python** para organizar y registrar documentos físicos y digitales.
Permite crear entradas con nombre, categoría, ubicación física y archivo digital asociado, usando una base de datos SQLite local sin dependencias externas.

---

## Problema
Organizar documentos físicos suele ser lento y caótico.
Encontrar un archivo específico implica revisar cajas, carpetas o montones de papeles, lo cual consume tiempo y genera frustración.

---

## Solución
Esta herramienta permite:
- Registrar documentos en una base local (SQLite).
- Asignarles una categoría y ubicación física.
- Adjuntar archivos digitales escaneados.
- Buscar rápidamente por nombre o categoría.
- Mantener todo en un sistema **simple, local y sin conexión a internet**.

---

## Instalación
```bash
git clone <tu-repo>
cd <tu-repo>
python3 doc_manager.py
```

## Caso de uso

1. Escanea un documento físico y guárdalo en la carpeta ~/Descargas/carpeta_de_enbudo/.

2. Ejecuta la herramienta y crea una nueva entrada.

3. Selecciona la categoría y la ubicación física del documento.

4. La herramienta copiará automáticamente el archivo digital a ~/Documentos/archivos_personales_fisicos/carpeta_{categoria}.

5. Ahora podrás buscar y administrar fácilmente tus documentos desde un solo lugar.
