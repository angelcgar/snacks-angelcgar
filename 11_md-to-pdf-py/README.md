# README

## Problema

## Solución

## Instalación

```python
# Clonar el repositorio
git clone

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Compilar el CLI
pyinstaller --onefile mdtool/cli.py -n mdtool

# Copiar el CLI al PATH
cp dist/mdtool /usr/local/bin/

# O al usuario
cp dist/mdtool ~/.local/bin/
```

## Uso

mdtool es una herramienta que te permite crear archivos pdf a travez de archivos markdown
