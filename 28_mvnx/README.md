# mvnx

Un **CLI mejorado para Maven**, hecho en Python con
[Typer](https://typer.tiangolo.com/) y [Rich](https://rich.readthedocs.io/).
Diseñado para simplificar comandos comunes de Maven y ofrecer una experiencia
más limpia, rápida y moderna desde la terminal.

---

## 🧩 Problema

Trabajar con Maven desde la línea de comandos puede ser tedioso:

- Los comandos son largos (`mvn exec:java -Dexec.mainClass=...`).
- La salida está saturada de texto irrelevante.
- Repetir tareas comunes requiere escribir demasiado.

---

## 💡 Solución

`mvnx` es un CLI liviano que simplifica Maven con una interfaz más intuitiva y
colorida.

Ejemplo:

```bash
mvnx run
```

en lugar de:

```bash
mvn exec:java -Dexec.mainClass="com.example.App"
```

Incluye:

- Comandos abreviados para las tareas más usadas (run, build, test, clean,
  etc.).

- Salidas limpias y legibles con colores.

- Ayuda integrada con --help.

## ⚙️ Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/angelcgar/snacks.git
cd 28_mvnx
```

2. Crear el ejecutable

Usa PyInstaller para generar un binario:

```bash
pip install -r requirements.txt
pyinstaller --onefile main.py --name mvnx
```

El binario aparecerá en dist/mvnx.

3. Instalar globalmente

```bash
mv dist/mvnx ~/.local/bin/
```

Luego podrás usarlo desde cualquier lugar:

```bash
mvnx --help
```

## Uso

```bash
mvnx run         # Ejecuta la app principal
mvnx build       # Construye el proyecto
mvnx test        # Ejecuta pruebas
mvnx clean       # Limpia el proyecto
mvnx --help      # Muestra ayuda general
```

## 🧱 Tecnologías

- Python 3.10+

- Typer (para CLI)

- Rich (para formato de salida)

- PyInstaller (para empaquetado)

## 🧑‍💻 Autor

**Angel Contreras**

💼 Desarrollador de software

🖤 Proyecto personal para mejorar productividad en Maven

## 📜 Licencia

MIT License — libre para usar, modificar y compartir.
