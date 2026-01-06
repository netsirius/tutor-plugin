# Tutor Plugin para Claude Code

Un plugin de tutor personal adaptativo para aprender lenguajes de programación con Claude Code.

## Características

- **Aprendizaje progresivo**: Lecciones estructuradas desde básico a avanzado
- **Ejercicios interactivos**: Problemas con tests automáticos y validación
- **Seguimiento de progreso**: Tracking de módulos, ejercicios, y métricas
- **Curriculum flexible**: Genera uno automáticamente o importa uno existente (Coursera, libros, etc.)
- **Feedback educativo**: Revisión de código con explicaciones constructivas
- **Múltiples agentes especializados**: Tutor, evaluador, y coach de práctica

---

## Instalación

### Requisitos Previos

- **Claude Code CLI** instalado
- **Python 3.8+** con FastMCP instalado:
  ```bash
  pip install fastmcp
  ```
- **Rust** (solo si vas a aprender Rust):
  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```

> **Nota sobre el servidor MCP**: No necesitas iniciarlo manualmente. Claude Code lo inicia automáticamente al cargar el plugin. Solo asegúrate de tener `fastmcp` instalado.

### Método 1: Instalar desde GitHub (Recomendado)

#### Paso 1: Añadir el marketplace

Abre Claude Code y ejecuta:

```
/plugin marketplace add hsantos/tutor-plugin
```

> Reemplaza `hsantos/tutor-plugin` con el usuario/repo real de GitHub.

#### Paso 2: Instalar el plugin

```
/plugin install tutor@hsantos-tutor-plugin
```

#### Paso 3: Verificar

```
/tutor:progress
```

### Método 2: Instalación interactiva

```
/plugin
```

Esto abre una UI interactiva donde puedes:
1. Ir a la pestaña **Marketplaces**
2. Añadir `hsantos/tutor-plugin`
3. Ir a **Discover** e instalar "tutor"

### Método 3: Desarrollo local

```bash
# Clonar el repositorio
git clone https://github.com/hsantos/tutor-plugin.git
cd tutor-plugin

# Instalar dependencias del MCP
pip install -r server/requirements.txt

# Ejecutar Claude Code con el plugin
claude --plugin-dir .
```

---

## Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/tutor:init` | Inicializar proyecto de tutoría | `/tutor:init` |
| `/tutor:learn [tema]` | Aprender un tema o continuar | `/tutor:learn ownership` |
| `/tutor:exercise [nivel]` | Obtener ejercicio de práctica | `/tutor:exercise intermedio` |
| `/tutor:progress` | Ver tu progreso | `/tutor:progress` |
| `/tutor:review [archivo]` | Revisar código con feedback | `/tutor:review src/main.rs` |
| `/tutor:curriculum` | Ver/generar/importar curriculum | `/tutor:curriculum generar rust` |

---

## Guía Rápida

### 1. Crear espacio de aprendizaje e inicializar

```bash
mkdir ~/aprendiendo-rust && cd ~/aprendiendo-rust
claude
```

```
/tutor:init
```

El tutor preguntará: lenguaje, nivel, objetivos, y tipo de curriculum.

### 2. Configurar plan de estudios

**Generar automáticamente:**
```
/tutor:curriculum generar rust
```

**Importar de Coursera/libro:**
```
/tutor:curriculum importar
```

### 3. Aprender

```
/tutor:learn              # Continuar donde lo dejaste
/tutor:learn ownership    # Tema específico
```

### 4. Practicar

```
/tutor:exercise           # Ejercicio del tema actual
/tutor:exercise avanzado  # Ejercicio de nivel específico
```

### 5. Revisar código

```
/tutor:review src/main.rs
```

### 6. Ver progreso

```
/tutor:progress
```

---

## Estructura del Proyecto de Aprendizaje

Cuando ejecutes `/tutor:init`, se creará:

```
~/aprendiendo-rust/
├── .tutor/
│   ├── config.json       # Configuración
│   ├── progress.json     # Tu progreso
│   ├── curriculum.json   # Plan de estudios
│   └── sessions/         # Historial
│
├── lessons/              # Lecciones generadas
│   ├── 01-basics/
│   │   ├── README.md
│   │   ├── examples/
│   │   └── exercises/
│   │       └── ex01_hello/
│   │           ├── Cargo.toml
│   │           └── src/main.rs
│   └── 02-ownership/
│
└── projects/             # Mini-proyectos
```

---

## Flujo de Trabajo Diario

```bash
# Día 1
claude
/tutor:init
/tutor:curriculum generar rust
/tutor:learn

# Días siguientes
claude
/tutor:learn                   # Continuar
/tutor:exercise                # Practicar
/tutor:review src/main.rs      # Feedback
/tutor:progress                # Ver progreso

# Dudas
"Explícame ownership de otra forma"
"No entiendo este error"
"Dame una pista"
```

---

## Agentes del Plugin

| Agente | Rol | Modelo |
|--------|-----|--------|
| **Tutor** | Explica conceptos, genera lecciones | opus |
| **Evaluator** | Revisa código, ejecuta tests | sonnet |
| **Practice Coach** | Genera ejercicios adaptados | sonnet |

---

## Herramientas MCP

El servidor MCP proporciona:

| Herramienta | Descripción |
|-------------|-------------|
| `get_student_progress` | Obtiene progreso actual |
| `update_exercise_progress` | Actualiza ejercicios |
| `get_next_lesson` | Recomienda siguiente lección |
| `validate_rust_code` | Compila código Rust |
| `run_rust_tests` | Ejecuta tests |
| `run_clippy` | Análisis con Clippy |
| `get_curriculum` | Obtiene curriculum |
| `save_curriculum` | Guarda curriculum |
| `start_study_session` | Inicia sesión |
| `end_study_session` | Finaliza sesión |

---

## Estructura del Plugin

```
tutor-plugin/
├── .claude-plugin/
│   ├── plugin.json           # Manifiesto
│   └── marketplace.json      # Para instalación desde GitHub
├── .mcp.json                 # Configuración MCP
│
├── agents/
│   ├── tutor.md
│   ├── evaluator.md
│   └── practice-coach.md
│
├── commands/
│   ├── init.md
│   ├── learn.md
│   ├── exercise.md
│   ├── progress.md
│   ├── review.md
│   └── curriculum.md
│
├── skills/
│   └── learning-tracker/
│       ├── SKILL.md
│       └── scripts/
│           └── progress.py
│
├── server/
│   ├── tutor_mcp.py
│   └── requirements.txt
│
├── templates/
│   ├── lesson.md
│   ├── exercise.md
│   └── project.md
│
└── README.md
```

---

## Personalización

### Modelos de agentes

Edita `agents/*.md`:

```yaml
---
model: sonnet    # opus, sonnet, haiku
---
```

### Preferencias

Edita `.tutor/config.json` en tu proyecto:

```json
{
  "preferences": {
    "explanation_style": "concise",
    "exercise_difficulty": "challenging",
    "show_hints": false
  }
}
```

---

## Solución de Problemas

### Plugin no se instala

```
/plugin marketplace list
/plugin marketplace add hsantos/tutor-plugin
```

### MCP no funciona

El servidor MCP se inicia automáticamente con el plugin. Si hay problemas:

```bash
# 1. Verifica que FastMCP está instalado
pip install fastmcp

# 2. Prueba el servidor manualmente (solo para debug)
cd tutor-plugin/server
python tutor_mcp.py

# 3. Si funciona manualmente, reinicia Claude Code
claude --debug
```

### Comandos no aparecen

```bash
claude --debug
/plugin
```

---

## Desinstalar

```
/plugin uninstall tutor@hsantos-tutor-plugin
/plugin marketplace remove hsantos-tutor-plugin
```

---

## Contribuir

1. Fork el repositorio
2. Crea una rama
3. Haz cambios
4. Pull request

---

## Licencia

MIT License
