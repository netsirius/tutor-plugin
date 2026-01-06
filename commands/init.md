---
description: Inicializar un nuevo proyecto de tutoría. Usa /tutor:init para configurar el directorio actual como un espacio de aprendizaje con seguimiento de progreso.
allowed-tools: Read, Write, Bash
---

# Comando: Init

El usuario quiere inicializar un nuevo proyecto de tutoría en el directorio actual.

## Tu Tarea

1. **Verificar si ya existe configuración**:
   - Si existe `.tutor/`, preguntar si desea reiniciar o continuar
   - Advertir que reiniciar perderá el progreso actual

2. **Recopilar información**:
   Pregunta al usuario:

   a) **Lenguaje a aprender**:
   ```
   ¿Qué lenguaje quieres aprender?
   - Rust
   - Python
   - TypeScript
   - Go
   - Otro (especificar)
   ```

   b) **Nivel actual**:
   ```
   ¿Cuál es tu nivel actual?
   - Total principiante (nunca he programado)
   - Principiante (sé programar en otro lenguaje)
   - Intermedio (algo de experiencia con este lenguaje)
   - Avanzado (quiero profundizar conocimientos)
   ```

   c) **Objetivos** (opcional):
   ```
   ¿Qué quieres lograr? (selecciona uno o más)
   - Aprendizaje general
   - Desarrollo web (backend)
   - CLI tools
   - Sistemas/embedded
   - Contribuir a open source
   - Preparación para entrevistas
   ```

   d) **Curriculum**:
   ```
   ¿Cómo quieres estructurar tu aprendizaje?
   - Generar curriculum automático (recomendado)
   - Tengo un plan de estudios que quiero seguir
   - Solo quiero practicar sin estructura fija
   ```

3. **Crear estructura de directorios**:

   ```
   .tutor/
   ├── config.json       # Configuración del curso
   ├── progress.json     # Progreso (inicialmente vacío)
   ├── curriculum.json   # Plan de estudios (si aplica)
   └── sessions/         # Directorio para sesiones

   lessons/              # Donde irán las lecciones

   projects/             # Donde irán los mini-proyectos
   ```

4. **Crear config.json**:

   ```json
   {
     "language": "[lenguaje elegido]",
     "student_name": "[nombre si lo proporciona]",
     "level": "[nivel elegido]",
     "started_at": "[fecha actual ISO]",
     "goals": ["[objetivos seleccionados]"],
     "curriculum_source": "generated|custom|none",
     "preferences": {
       "explanation_style": "detailed",
       "exercise_difficulty": "adaptive",
       "show_hints": true
     }
   }
   ```

5. **Crear progress.json inicial**:

   ```json
   {
     "current_module": null,
     "current_topic": null,
     "modules": {},
     "statistics": {
       "total_time_minutes": 0,
       "total_exercises_completed": 0,
       "total_exercises_attempted": 0,
       "average_score": 0,
       "streak_days": 0,
       "last_session": null
     }
   }
   ```

6. **Si eligió generar curriculum**:
   - Llama a `/tutor:curriculum generar [lenguaje]` internamente
   - O genera un curriculum básico directamente

7. **Mensaje de bienvenida**:

   ```
   🎓 ¡Proyecto de tutoría inicializado!

   📁 Estructura creada:
   ├── .tutor/          → Tu configuración y progreso
   ├── lessons/         → Aquí aparecerán las lecciones
   └── projects/        → Aquí harás mini-proyectos

   📚 Lenguaje: Rust
   📊 Nivel: Principiante
   🎯 Objetivos: CLI tools, Open source

   ¿Listo para empezar? Usa:
   • /tutor:learn         → Comenzar primera lección
   • /tutor:curriculum    → Ver/ajustar plan de estudios
   • /tutor:progress      → Ver tu progreso (vacío por ahora)

   ¡Buena suerte en tu viaje de aprendizaje! 🚀
   ```

## Reiniciar Proyecto Existente

Si el usuario tiene un `.tutor/` existente:

```
⚠️ Ya existe un proyecto de tutoría en este directorio.

Opciones:
1. Continuar con el curso actual
2. Reiniciar desde cero (perderás tu progreso)
3. Crear backup y reiniciar

¿Qué prefieres?
```

Si elige backup:
- Crear `.tutor.backup.[fecha]/`
- Copiar todo `.tutor/` ahí
- Luego reiniciar

## Notas

- El comando debe ser interactivo pero no tedioso
- Si el usuario da respuestas cortas, inferir el resto
- Siempre crear la estructura mínima necesaria
- El curriculum puede añadirse después si lo prefiere
