---
name: learning-tracker
description: Gestiona el progreso de aprendizaje del estudiante. Lee y actualiza el estado del curso, módulos completados, ejercicios resueltos, y métricas de aprendizaje. Este skill se usa automáticamente cuando el tutor necesita conocer o actualizar el progreso.
allowed-tools: Read, Write, Bash(python:*)
---

# Learning Tracker Skill

Este skill proporciona capacidades para gestionar el progreso de aprendizaje del estudiante.

## Archivos de Estado

### Ubicación
Todos los archivos de estado se guardan en `.tutor/` en el directorio del proyecto actual:

```
.tutor/
├── config.json       # Configuración del curso
├── progress.json     # Progreso detallado
├── curriculum.json   # Plan de estudios
└── sessions/         # Historial de sesiones
    └── YYYY-MM-DD.json
```

## Estructura de Datos

### config.json
```json
{
  "language": "rust",
  "student_name": "nombre",
  "level": "beginner",
  "started_at": "2026-01-06T10:00:00Z",
  "goals": ["Crear CLI tools", "Contribuir a open source"],
  "time_per_session": "1h",
  "curriculum_source": "generated",
  "preferences": {
    "explanation_style": "detailed",
    "exercise_difficulty": "adaptive",
    "show_hints": true
  }
}
```

### progress.json
```json
{
  "current_module": "02-ownership",
  "current_topic": "borrowing",
  "modules": {
    "01-basics": {
      "status": "completed",
      "started_at": "2026-01-06",
      "completed_at": "2026-01-08",
      "score": 92,
      "time_spent_minutes": 180,
      "exercises": {
        "ex01_hello": {"status": "completed", "attempts": 1, "score": 100},
        "ex02_variables": {"status": "completed", "attempts": 2, "score": 85}
      }
    },
    "02-ownership": {
      "status": "in_progress",
      "started_at": "2026-01-09",
      "exercises": {
        "ex01_ownership": {"status": "completed", "attempts": 3, "score": 75},
        "ex02_borrowing": {"status": "in_progress", "attempts": 1}
      }
    }
  },
  "statistics": {
    "total_time_minutes": 420,
    "total_exercises_completed": 15,
    "total_exercises_attempted": 18,
    "average_score": 85,
    "streak_days": 5,
    "last_session": "2026-01-10"
  }
}
```

## Operaciones Disponibles

### 1. Inicializar Curso
Cuando no existe `.tutor/`, crear la estructura inicial:

```python
# Usar el script de utilidades
python ${SKILL_ROOT}/scripts/progress.py init --language rust --level beginner
```

### 2. Cargar Progreso
Leer el estado actual del estudiante:

```python
python ${SKILL_ROOT}/scripts/progress.py get
```

Retorna JSON con todo el progreso.

### 3. Actualizar Progreso
Después de completar una lección o ejercicio:

```python
# Completar ejercicio
python ${SKILL_ROOT}/scripts/progress.py complete-exercise \
  --module "02-ownership" \
  --exercise "ex02_borrowing" \
  --score 90 \
  --attempts 2

# Completar módulo
python ${SKILL_ROOT}/scripts/progress.py complete-module \
  --module "02-ownership" \
  --score 88
```

### 4. Registrar Sesión
Al iniciar y finalizar cada sesión de estudio:

```python
# Iniciar sesión
python ${SKILL_ROOT}/scripts/progress.py start-session

# Finalizar sesión
python ${SKILL_ROOT}/scripts/progress.py end-session \
  --topics-covered "borrowing,slices" \
  --exercises-done 3
```

### 5. Obtener Recomendaciones
Determinar qué estudiar a continuación:

```python
python ${SKILL_ROOT}/scripts/progress.py recommend
```

Retorna el siguiente tema basado en:
- Prerrequisitos completados
- Áreas que necesitan refuerzo
- Tiempo desde última práctica

### 6. Generar Reporte
Crear un resumen del progreso:

```python
python ${SKILL_ROOT}/scripts/progress.py report
```

## Cálculo de Métricas

### Puntuación de Ejercicio
- 100 puntos: Completado en primer intento
- -10 puntos por cada intento adicional
- Mínimo 60 puntos si se completa

### Puntuación de Módulo
- Promedio ponderado de ejercicios
- Bonus por completar sin saltar ejercicios

### Racha (Streak)
- Cuenta días consecutivos con actividad
- Se reinicia si pasan más de 24h sin estudiar
- Considerar zona horaria del estudiante

### Nivel de Maestría
Basado en puntuación acumulada:
- < 70: Necesita refuerzo
- 70-85: Competente
- 85-95: Proficiente
- > 95: Experto

## Uso en los Agentes

Los agentes del tutor deben:

1. **Al inicio de sesión**: Cargar progreso para contextualizar
2. **Después de cada ejercicio**: Actualizar progreso inmediatamente
3. **Al dar feedback**: Considerar el historial del estudiante
4. **Al sugerir siguiente paso**: Usar las recomendaciones

## Ejemplo de Integración

```
1. Usuario dice "continuar con el curso"
2. Tutor ejecuta: python progress.py get
3. Lee que está en módulo 02, tema "borrowing"
4. Presenta la lección correspondiente
5. Al completar ejercicio, ejecuta: python progress.py complete-exercise ...
6. Sugiere siguiente tema basado en: python progress.py recommend
```
