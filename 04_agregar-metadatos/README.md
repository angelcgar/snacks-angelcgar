# CLI para agregar metadatos a archivos Markdown

Este es un CLI para agregar metadatos a archivos `.md` en formato YAML.

## Instalación

Clona el repositorio y ejecuta el script de instalación:

```bash
python install.py
```

## Uso

El script se puede ejecutar con el siguiente comando:

```bash
python app.py <comando> [opciones]
```

### Comandos

*   `version`: Muestra la versión del programa.
*   `hola`: Saluda a una persona.
    *   `--nombre`: Nombre de la persona a saludar.
*   `basico`: Agrega frontmatter a un archivo Markdown.
    *   `-a`, `--agregar`: Ruta del archivo Markdown a modificar.
    *   `-d`, `--description`: Descripción personalizada para el frontmatter.
    *   `--renombrar`: Renombrar el archivo usando el slug generado.
    *   `--guardar`: Guardar el archivo en `~/Descargas/md_con_metadatos/`.
*   `guardar`: Mueve un archivo directamente a `~/Descargas/md_con_metadatos/`.
    *   `archivo`: Ruta del archivo a mover.
*   `actualizar`: Actualiza la fecha de modificación de un archivo Markdown.
    *   `archivo`: Ruta del archivo a actualizar.
