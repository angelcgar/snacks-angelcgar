# Harbor CLI

## Problema

Ya estoy cansado de estar dando permisos a carpetas de imágenes al lado de mis proyectos backend.
El típico:

```bash
sudo chmod +x postgres/ mysql/ mongo/ etc...
```

😫 Termina siendo un desorden y un dolor de cabeza.

Claro, está la opción de usar un hosting remoto, pero en testing hago muchas peticiones “a lo tonto” y no quiero gastar dinero en eso.

## Solucion

Este CLI simplifica la creación y manejo de contenedores de bases de datos con Docker Compose:

- Crea un proyecto en su propia carpeta.

- Genera automáticamente el docker-compose.yml.

- Te da credenciales listas para copiar/pegar en tu cliente SQL.

- Levanta, baja y limpia contenedores con comandos simples.

Pensado especialmente para Linux (porque este problema de permisos no existe igual en Windows/MacOS).

## Caso de uso

Crear un nuevo contenedor de MySQL:

```bash
harbor new mydb --image mysql --version-image 8.0.36
```

Levantar un contenedor existente, debes de estar en un directorio con el docker-compose.yml:

```bash
harbor get-up mydb
```

Limpiar todos los contenedores:

```bash
harbor clean
```
