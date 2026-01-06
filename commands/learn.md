---
description: Iniciar o continuar una lección sobre un tema específico. Usa /tutor:learn [tema] para aprender algo nuevo o /tutor:learn para continuar donde lo dejaste.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Comando: Learn

El usuario quiere aprender o continuar aprendiendo.

## Tu Tarea

### Si se proporciona un tema (ej: `/tutor:learn ownership`)
1. Lee `.tutor/progress.json` para conocer el contexto
2. Verifica si el tema está en el curriculum del estudiante
3. Si hay prerequisitos pendientes, sugiere estudiarlos primero
4. Presenta una lección estructurada sobre el tema:
   - Explicación conceptual con analogías
   - Ejemplos de código funcionales
   - Conexión con lo que ya sabe
5. Crea archivos de ejemplo en `lessons/[modulo]/examples/`
6. Ofrece ejercicios de práctica al final
7. Actualiza el progreso

### Si no se proporciona tema (ej: `/tutor:learn`)
1. Lee `.tutor/progress.json`
2. Determina el siguiente tema según el curriculum
3. Resume brevemente lo último aprendido
4. Continúa con la siguiente lección

### Si es la primera vez (no existe .tutor/)
1. Da la bienvenida al estudiante
2. Pregunta:
   - ¿Qué lenguaje quieres aprender?
   - ¿Cuál es tu experiencia previa?
   - ¿Tienes un plan de estudios específico o quieres que genere uno?
   - ¿Cuánto tiempo puedes dedicar?
3. Crea la estructura inicial:
   ```
   .tutor/
   ├── config.json      # Configuración del curso
   ├── progress.json    # Progreso inicial
   └── curriculum.json  # Plan de estudios (generado o importado)
   ```
4. Inicia la primera lección

## Estructura de config.json
```json
{
  "language": "rust",
  "student_name": "nombre",
  "level": "beginner|intermediate|advanced",
  "started_at": "2026-01-06",
  "goals": ["Contribuir a proyectos open source", "Crear CLI tools"],
  "time_per_session": "30min|1h|2h",
  "curriculum_source": "generated|custom"
}
```

## Recuerda
- Adapta el nivel de explicación según el progreso del estudiante
- Usa ejemplos del mundo real, no abstractos
- Celebra el progreso
- Ofrece descansos si la sesión es larga
