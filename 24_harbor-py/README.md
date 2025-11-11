# 🐳 Harbor CLI - Docker Database Manager

> **CLI moderno para administrar bases de datos temporales con Docker**

## 🚀 Características

- ✅ **Interfaz moderna** con Typer + Rich para mejor UX
- 🎨 **Componentes visuales elegantes**: tablas, paneles, barras de progreso
- 📦 **Gestión automatizada** de docker-compose.yml
- 🔗 **URLs de conexión automáticas** para tus clientes SQL
- 🌱 **Archivos seed.sql** incluidos con ejemplos
- 🧹 **Limpieza masiva** de contenedores con confirmación
- 🔧 **Configuración JSON** detallada por proyecto
- 🐋 **Soporte amplio**: MySQL, PostgreSQL, MongoDB, Redis, MariaDB

## 📝 Problema que resuelve

¿Cansado de lidiar con permisos de Docker y carpetas desordenadas?

```bash
# El viejo flujo tedioso:
sudo chmod +x postgres/ mysql/ mongo/
docker run -d --name mysql1...
docker run -d --name postgres2...
# ¿Qué puerto usé? ¿Cuál era la contraseña?
```

Harbor automatiza todo esto con **comandos simples** y **configuración clara**.

## 🛠️ Instalación

### Opción 1: Instalación rápida (recomendada)

```bash
# Clona el proyecto
git clone https://github.com/usuario/harbor-cli
cd harbor-cli

# Activa entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instala y construye ejecutable
python install.py

# ¡Listo! Ahora puedes usar 'harbor' globalmente
harbor --help
```

### Opción 2: Uso directo con Python

```bash
pip install typer rich
python harbor.py --help
```

## 🎯 Uso

### Crear nuevo proyecto de base de datos

```bash
# MySQL con configuración automática
harbor new mi-mysql --image mysql --version-image 8.0

# PostgreSQL
harbor new mi-postgres --image postgres --version-image 15

# MongoDB
harbor new mi-mongo --image mongo --version-image 7.0

# Imagen personalizada (te pide el puerto)
harbor new mi-redis --image redis --version-image alpine
```

### Levantar proyecto existente

```bash
harbor get-up mi-mysql
```

### Limpiar todos los contenedores

```bash
harbor clean
# Te pide confirmación antes de eliminar TODO
```

## 📁 Estructura generada

Cada proyecto crea una carpeta organizada:

```
contenedor_mi-mysql/
├── docker-compose.yml       # Configuración Docker Compose
├── mi-mysql_info.json      # Credenciales y URLs de conexión
└── seed.sql                # Ejemplos SQL listos para usar
```

## 📊 Información del proyecto

Después de crear un proyecto, Harbor muestra una tabla elegante con toda la
información:

```
┌─────────────────────────────────────────────────────────┐
│                  Información del Proyecto              │
├────────────────┬────────────────────────────────────────┤
│ 📁 Directorio  │ contenedor_mi-mysql                    │
│ 🐳 Imagen      │ mysql:8.0                              │
│ 📦 Contenedor  │ mi-mysql_container                     │
│ 🔌 Puerto      │ 3306                                   │
│ 🗄️ Base datos  │ mi-mysql_db                            │
│ 📝 Config      │ mi-mysql_info.json                     │
│ 🌱 Seed file   │ seed.sql                               │
└────────────────┴────────────────────────────────────────┘
```

## 🔗 URLs de conexión automáticas

Harbor genera URLs listas para usar en tus clientes SQL:

**MySQL:**

```bash
# Usuario root
mysql://root:123456789@localhost:3306/mi-mysql_db

# Usuario personalizado
mysql://angel:mipassword@localhost:3306/mi-mysql_db
```

**PostgreSQL:**

```bash
postgresql://postgres:123456789@localhost:5432/mi-postgres_db
postgresql://angel:mipassword@localhost:5432/mi-postgres_db
```

**MongoDB:**

```bash
mongodb://root:123456789@localhost:27017/mi-mongo_db
```

## 🌱 Archivo seed.sql

Cada proyecto incluye un `seed.sql` con ejemplos para PostgreSQL, MySQL y
SQLite:

```sql
-- POSTGRESQL EJEMPLO
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (username) VALUES ('alice'), ('bob');
```

## ⚙️ Puertos predeterminados

Harbor conoce los puertos estándar:

- **MySQL**: 3306
- **PostgreSQL**: 5432
- **MongoDB**: 27017
- **Redis**: 6379
- **MariaDB**: 3307

Para otras imágenes, te pregunta el puerto interactivamente.

## 🎨 Interfaz visual

### Banner elegante

```
┌────────────────────────────────────────┐
│ 🐳 Harbor — Docker DB Manager         │
│ Administrador de bases de datos        │
│ temporales                             │
└────────────────────────────────────────┘
```

### Progreso visual

```
🔄 Configurando proyecto... ████████████ 100%
✅ Proyecto creado exitosamente
```

### Confirmaciones seguras

```
🗑️ ¿Estás seguro de que quieres detener y eliminar
   TODOS los contenedores? [y/N]:
```

## 🔧 Configuración avanzada

### Variables de entorno automáticas

Harbor configura automáticamente las variables según la imagen:

**MySQL:**

- `MYSQL_ROOT_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

**PostgreSQL:**

- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_USER`

**MongoDB:**

- `MONGO_INITDB_ROOT_PASSWORD`
- `MONGO_INITDB_DATABASE`
- `MONGO_INITDB_ROOT_USERNAME`

## 🐛 Solución de problemas

### Error: "No se encontró pom.xml"

```bash
# Harbor busca el docker-compose.yml en la carpeta del proyecto
cd contenedor_mi-mysql/
harbor get-up mi-mysql
```

### Error: "Puerto en uso"

```bash
# Limpia contenedores existentes
harbor clean

# O cambia el puerto en docker-compose.yml
```

### Error: "Docker no disponible"

```bash
# Verifica que Docker esté corriendo
docker --version
sudo systemctl start docker  # Linux
```

## 💡 Tips y trucos

1. **Usa nombres descriptivos**: `harbor new test-auth --image postgres`
2. **Agrupa por proyecto**: `harbor new myapp-db --image mysql`
3. **Versiones específicas**: `--version-image 13.2` para control preciso
4. **Backup fácil**: Los archivos JSON contienen toda la configuración

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Add: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📜 Licencia

MIT License - ve [LICENSE](LICENSE) para más detalles.

---

**Hecho con ❤️ para developers que odian configurar Docker manualmente**
