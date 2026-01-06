---
description: View learning progress. Shows statistics, completed topics, study streak, and suggestions for what to study next.
allowed-tools: Read, Bash
---

# Command: Progress

The user wants to see their learning progress.

## Important: Language Adaptation

Before presenting any content, read `.tutor/config.json` and check the `learning_language` field. ALL output MUST be presented in the student's chosen language.

## Your Task

1. Read the state files:
   - `.tutor/config.json` - course configuration (includes learning_language)
   - `.tutor/progress.json` - detailed progress
   - `.tutor/curriculum.json` - study plan

2. Calculate statistics:
   - Modules completed / total
   - Exercises completed / total
   - Total study time
   - Current day streak
   - Average attempts per exercise

3. Present the report visually and motivationally (in the student's language)

## Response Format (English Example)

```
╔══════════════════════════════════════════════════════════════╗
║                    📚 Your Progress in Rust                   ║
╠══════════════════════════════════════════════════════════════╣
║  Level: Intermediate                                          ║
║  Days studying: 15  |  Current streak: 🔥 5 days             ║
╚══════════════════════════════════════════════════════════════╝

📊 GENERAL SUMMARY
├── Modules completed: 3/10 (30%)
├── Exercises solved: 24/80
├── Total time: ~12 hours
└── Average per exercise: 1.5 attempts

📈 PROGRESS BY MODULE
┌────────────────────────────────────────┐
│ ✅ 01. Fundamentals       [██████████] │
│ ✅ 02. Ownership          [██████████] │
│ ✅ 03. Structs & Enums    [██████████] │
│ 🔄 04. Error Handling     [████░░░░░░] │ ← You are here
│ ⬚ 05. Collections         [░░░░░░░░░░] │
│ ⬚ 06. Traits              [░░░░░░░░░░] │
│ ...                                    │
└────────────────────────────────────────┘

💪 STRENGTHS
• Variables and basic types
• Pattern matching
• Using Option and Result

📌 AREAS TO REINFORCE
• Lifetimes (3 exercises with difficulty)
• Borrowing in complex structures

🎯 SUGGESTED NEXT STEP
Continue with "Error Handling" - you have 4 exercises
left in the module. You're close to completing it!

📅 LAST SESSION
2 days ago - You worked on "Result and the ? operator"
```

## Response Format (Spanish Example)

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

## If There's No Progress

If `.tutor/` doesn't exist:

For English:
```
👋 Hi! You haven't started any course yet.

To begin, use:
  /tutor:init           - Initialize a new course
  /tutor:curriculum     - Set up a study plan

Ready to start your learning journey?
```

For Spanish:
```
👋 ¡Hola! Aún no has iniciado ningún curso.

Para comenzar, usa:
  /tutor:init           - Iniciar un nuevo curso
  /tutor:curriculum     - Configurar un plan de estudios

¿Listo para empezar tu viaje de aprendizaje?
```

## Additional Information Available

If the user asks for more detail:
- Session history (`.tutor/sessions/`)
- Specific completed exercises
- Time per module
- Weekly activity graph
