# Biblioteca CLI

Biblioteca CLI es una herramienta de línea de comandos escrita en Python que te permite administrar tu colección de libros directamente desde la terminal. Puedes agregar, listar, leer y eliminar libros de manera sencilla y rápida.

## Características

- **Agregar libros** a tu biblioteca.
- **Listar** todos los libros registrados.
- **Abrir libros** (PDF) con tu lector predeterminado (por defecto usa `zathura`).
- **Eliminar libros** de la biblioteca.
- Configuración y almacenamiento de datos en archivos JSON en tu directorio personal.

## Instalación

1. Clona este repositorio o descarga los archivos `app.py` e `install.py`.
2. Ejecuta el script de instalación:

   ```sh
   python3 install.py
   ```

   Esto instalará el comando `biblioteca` en tu sistema.

## Instalación rápida

Si prefieres una instalación rápida, puedes ejecutar el siguiente comando directamente en tu terminal:

```sh
chmod +x app.py          # Permisos de ejecución
sudo ln -s "$(pwd)/app.py" /usr/local/bin/pdfcli   # Alias global (opcional)
```

## Uso

Ejecuta el comando `biblioteca` seguido de la acción que desees realizar:

- **Agregar un libro** (desde el directorio donde está el PDF):

  ```sh
  biblioteca agregar -n NombreDelLibro.pdf
  ```

- **Listar todos los libros**:

  ```sh
  biblioteca listar
  ```

- **Leer un libro**:

  ```sh
  biblioteca leer NombreDelLibro
  ```

- **Eliminar un libro**:

  ```sh
  biblioteca eliminar NombreDelLibro
  ```

- **Ver la versión**:

  ```sh
  biblioteca version
  ```

## Requisitos

- Python 3.x
- Lector de PDF instalado (por defecto usa `zathura`, puedes modificarlo en el código si prefieres otro lector)

## Estructura del proyecto

- [`app.py`](app.py): Código principal de la aplicación CLI.
- [`install.py`](install.py): Script para instalar el comando en tu sistema.
- `.config/biblioteca_cli_config/`: Carpeta donde se almacenan los datos y configuraciones.

## Licencia

MIT

---

¡Disfruta gestionando tu biblioteca desde la terminal!
