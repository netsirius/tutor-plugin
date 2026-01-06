---
description: Ver el progreso de aprendizaje. Muestra estadísticas, temas completados, racha de estudio, y sugerencias de qué estudiar a continuación.
allowed-tools: Read, Bash
---

# Comando: Progress

El usuario quiere ver su progreso de aprendizaje.

## Tu Tarea

1. Lee los archivos de estado:
   - `.tutor/config.json` - configuración del curso
   - `.tutor/progress.json` - progreso detallado
   - `.tutor/curriculum.json` - plan de estudios

2. Calcula estadísticas:
   - Módulos completados / total
   - Ejercicios completados / total
   - Tiempo total de estudio
   - Racha actual de días
   - Promedio de intentos por ejercicio

3. Presenta el informe de forma visual y motivadora

## Formato de Respuesta

```
╔══════════════════════════════════════════════════════════════╗
║                    📚 Tu Progreso en Rust                    ║
╠══════════════════════════════════════════════════════════════╣
║  Nivel: Intermedio                                           ║
║  Días estudiando: 15  |  Racha actual: 🔥 5 días            ║
╚══════════════════════════════════════════════════════════════╝

📊 RESUMEN GENERAL
├── Módulos completados: 3/10 (30%)
├── Ejercicios resueltos: 24/80
├── Tiempo total: ~12 horas
└── Promedio por ejercicio: 1.5 intentos

📈 PROGRESO POR MÓDULO
┌────────────────────────────────────────┐
│ ✅ 01. Fundamentos        [██████████] │
│ ✅ 02. Ownership          [██████████] │
│ ✅ 03. Structs & Enums    [██████████] │
│ 🔄 04. Error Handling     [████░░░░░░] │ ← Aquí estás
│ ⬚ 05. Colecciones         [░░░░░░░░░░] │
│ ⬚ 06. Traits              [░░░░░░░░░░] │
│ ...                                    │
└────────────────────────────────────────┘

💪 FORTALEZAS
• Variables y tipos básicos
• Pattern matching
• Uso de Option y Result

📌 ÁREAS A REFORZAR
• Lifetimes (3 ejercicios con dificultad)
• Borrowing en estructuras complejas

🎯 SIGUIENTE PASO SUGERIDO
Continuar con "Error Handling" - te quedan 4 ejercicios
del módulo. ¡Estás cerca de completarlo!

📅 ÚLTIMA SESIÓN
Hace 2 días - Trabajaste en "Result y el operador ?"
```

## Si No Hay Progreso

Si `.tutor/` no existe:

```
👋 ¡Hola! Aún no has iniciado ningún curso.

Para comenzar, usa:
  /tutor:learn           - Iniciar un nuevo curso
  /tutor:curriculum      - Configurar un plan de estudios

¿Listo para empezar tu viaje de aprendizaje?
```

## Información Adicional Disponible

Si el usuario pide más detalle:
- Historial de sesiones (`.tutor/sessions/`)
- Ejercicios específicos completados
- Tiempo por módulo
- Gráfico de actividad semanal
