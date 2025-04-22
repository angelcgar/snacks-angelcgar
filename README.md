# 📓 Today.sh - Gestor Inteligente de Diarios

## 🚀 Instalación Rápida

```bash
./install.sh
```

## ✨ Características Principales

| Función                     | Descripción                              |
| --------------------------- | ---------------------------------------- |
| 📅 Generación automática    | Crea archivos diarios con fecha          |
| 🎨 Sistema de templates     | Plantillas personalizables con variables |
| 🗂 Organización inteligente | Estructura automática por meses          |
| ⚡ Acceso rápido            | Atajos para diferentes tipos de entradas |

## Variables Disponibles en Templates

### Diario de {{fecha}} ({{dia_semana}})

**Semana {{semana}} del {{año}}**  
Registro creado a las {{hora}}

## 📌 Prioridades del día

1. [ ]
2. [ ]

## 🌱 Agradecimientos

-

## Estructura de Directorios

~/Documentos/diario/
├── 25-03-marzo/
│ ├── 29-03-2025.md
│ └── 30-03-2025.md
├── 25-04-abril/
└── plantillas/
├── diario.md
├── trabajo.md
└── fitness.md

## Uso Avanzado

Crear nueva plantilla

```bash
today add-template finanzas
```

## Usar plantilla específica

```bash
today finanzas
```

## Comandos especiales

```bash
today directorio   # Crea solo estructura de carpetas
today list        # Muestra todas las plantillas
```

## Ejemplo Completo

Plantilla salud.md:

```markdown
# {{fecha}} - Registro de Salud

## 💪 Actividad Física

- Tipo:
- Duración:
- Intensidad: ⭐⭐⭐⭐⭐

## 🥗 Alimentación

Desayuno:
Almuerzo:
Cena:

## 😴 Sueño

Calidad:
Horas:
```

## Requisitos

- Bash 4.0+

- Coreutils (date, sed)

- Editor de texto preferido (opcional)
