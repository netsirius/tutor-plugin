---
description: Initialize a new tutoring project. Use /tutor:init to configure the current directory as a learning space with progress tracking. Supports any subject - programming, math, science, languages, etc.
allowed-tools: Read, Write, Bash
---

# Command: Init

The user wants to initialize a new tutoring project in the current directory.

## Your Task

1. **Check if configuration already exists**:
   - If `.tutor/` exists, ask if they want to reset or continue
   - Warn that resetting will lose current progress

2. **Gather information**:
   Ask the user:

   a) **Preferred learning language** (IMPORTANT - ask this first):
   ```
   What language would you like to learn in?
   - English
   - Spanish (Español)
   - Other (specify)
   ```

   **Note**: This setting determines the language used for all lessons, exercises, explanations, and feedback throughout the learning experience.

   b) **Subject to learn**:
   ```
   What do you want to learn?

   Programming:
   - Rust, Python, TypeScript, Go, Java, C++, etc.

   Mathematics:
   - Algebra, Calculus, Statistics, Linear Algebra, etc.

   Sciences:
   - Physics, Chemistry, Biology, Computer Science Theory

   Languages:
   - English, Spanish, French, German, Japanese, etc.

   Technical Skills:
   - System Design, DevOps, Data Science, Machine Learning

   Other:
   - Any subject you want to learn!
   ```

   c) **Current level**:
   ```
   What is your current level in this subject?
   - Total beginner (no prior knowledge)
   - Beginner (basic familiarity)
   - Intermediate (working knowledge)
   - Advanced (want to master/deepen knowledge)
   ```

   d) **Goals** (optional):
   ```
   What do you want to achieve? (select one or more)

   For Programming:
   - General learning, Web development, CLI tools, Systems, Open source, Interview prep

   For Math/Science:
   - Academic study, Professional application, Research, Exam preparation

   For Languages:
   - Conversation, Reading, Writing, Business, Travel, Certification

   For Technical Skills:
   - Career change, Skill upgrade, Certification, Project-based
   ```

   e) **Curriculum**:
   ```
   How do you want to structure your learning?
   - Generate automatic curriculum (recommended)
   - I have a study plan I want to follow
   - Just want to practice without fixed structure
   ```

3. **Create directory structure**:

   ```
   .tutor/
   ├── config.json       # Course configuration
   ├── progress.json     # Progress (initially empty)
   ├── curriculum.json   # Study plan (if applicable)
   └── sessions/         # Directory for sessions

   lessons/              # Where lessons will go

   projects/             # Where mini-projects will go
   ```

4. **Create config.json**:

   ```json
   {
     "learning_language": "[chosen language: en|es|etc]",
     "subject_type": "[programming|mathematics|science|language|technical|other]",
     "subject": "[specific subject: rust|calculus|physics|spanish|etc]",
     "student_name": "[name if provided]",
     "level": "[chosen level]",
     "started_at": "[current ISO date]",
     "goals": ["[selected goals]"],
     "curriculum_source": "generated|custom|none",
     "preferences": {
       "explanation_style": "detailed",
       "exercise_difficulty": "adaptive",
       "show_hints": true,
       "learning_style": "adaptive"
     },
     "adaptive_learning": {
       "skill_tracking": true,
       "spaced_repetition": true,
       "learning_style_detection": true
     }
   }
   ```

   **Note**: For backward compatibility, if subject_type is "programming", also set "programming_language" to the subject value.

5. **Create initial progress.json**:

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

6. **If they chose to generate curriculum**:
   - Call `/tutor:curriculum generate [language]` internally
   - Or generate a basic curriculum directly

7. **Welcome message** (in the user's chosen learning language):

   For English:
   ```
   🎓 Tutoring project initialized!

   📁 Structure created:
   ├── .tutor/          → Your configuration and progress
   ├── lessons/         → Lessons will appear here
   └── projects/        → Mini-projects go here

   📚 Language: Rust
   📊 Level: Beginner
   🎯 Goals: CLI tools, Open source

   Ready to start? Use:
   • /tutor:learn         → Start first lesson
   • /tutor:curriculum    → View/adjust study plan
   • /tutor:progress      → View your progress (empty for now)

   Good luck on your learning journey! 🚀
   ```

   For Spanish:
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

## Reset Existing Project

If the user has an existing `.tutor/`:

```
⚠️ A tutoring project already exists in this directory.

Options:
1. Continue with current course
2. Reset from scratch (you will lose your progress)
3. Create backup and reset

What would you prefer?
```

If they choose backup:
- Create `.tutor.backup.[date]/`
- Copy all `.tutor/` there
- Then reset

## Notes

- The command should be interactive but not tedious
- If the user gives short answers, infer the rest
- Always create the minimum necessary structure
- The curriculum can be added later if preferred
- **IMPORTANT**: The `learning_language` setting determines the language for ALL content generated by the tutor (lessons, exercises, feedback, progress reports)
