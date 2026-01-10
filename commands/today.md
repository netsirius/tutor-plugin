---
description: Smart dashboard showing what to study today. Use /tutor:today or just /tutor to get personalized recommendations based on your progress, exam dates, and SRS items due.
allowed-tools: Read, Write, Bash
---

# Command: Today (Dashboard)

The user wants to see their personalized study dashboard. This is the **main entry point** for daily study.

**IMPORTANT**: The dashboard adapts to the learning context (university, project, self-taught, etc.). Read the context from config and display accordingly.

## Your Task

1. **Read configuration and progress files**:
   - `.tutor/config.json` - Main configuration
   - `.tutor/university_config.json` - University-specific config (if exists)
   - `.tutor/progress.json` - Current progress
   - `.tutor/study_plan.json` - Study plan (if exists)
   - `.tutor/topic_status.json` - Status per topic
   - `.tutor/srs.json` - Spaced repetition items

2. **Use MCP tools to get current state**:
   - `get_student_progress()` - Get overall progress
   - `get_spaced_repetition_items()` - Get SRS items due
   - `get_learning_recommendations()` - Get AI recommendations

3. **Display the dashboard** (in user's learning_language):

### Spanish Version:
```
================================================================================
                         ESTRUCTURAS DE DATOS
================================================================================
                                                    Examen en 12 días

  PROGRESO GENERAL
  ────────────────────────────────────────────────────────────────────────────
  Temario:     [████████░░░░░░░░░░░░] 40% completado
  Ejercicios:  [██████░░░░░░░░░░░░░░] 30% resueltos
  Simulacros:  [████░░░░░░░░░░░░░░░░] 1/3 completados

  Racha: 5 días consecutivos

  PARA HOY
  ────────────────────────────────────────────────────────────────────────────

  1. Repaso SRS (5 conceptos vencidos)                           10 min
     → Árboles, Colas, Pilas (conceptos que necesitan repaso)

  2. Continuar: Árboles AVL - Rotaciones                         45 min
     → Tema en progreso, al 60%

  3. Ejercicio de práctica                                        20 min
     → Reforzar Árboles Binarios (punto débil detectado)

  Tiempo total estimado: ~1h 15min

  ESTADO DEL TEMARIO
  ────────────────────────────────────────────────────────────────────────────
  ✅ Completados (4):  Arrays, Listas, Pilas, Colas
  🔄 En progreso (1):  Árboles AVL
  ⏳ Pendientes (3):   Grafos, Hash Tables, Ordenamiento
  ⚠️  Oxidados (2):    Pilas, Colas (necesitan repaso SRS)

  ACCIONES RÁPIDAS
  ────────────────────────────────────────────────────────────────────────────
  [C] Continuar donde lo dejé (recomendado)
  [R] Repasar conceptos (SRS)
  [E] Hacer ejercicio
  [S] Simulacro de examen
  [P] Ver plan completo
  [?] Más opciones

================================================================================
```

### English Version:
```
================================================================================
                          DATA STRUCTURES
================================================================================
                                                      Exam in 12 days

  OVERALL PROGRESS
  ────────────────────────────────────────────────────────────────────────────
  Syllabus:    [████████░░░░░░░░░░░░] 40% completed
  Exercises:   [██████░░░░░░░░░░░░░░] 30% solved
  Simulations: [████░░░░░░░░░░░░░░░░] 1/3 completed

  Streak: 5 consecutive days

  FOR TODAY
  ────────────────────────────────────────────────────────────────────────────

  1. SRS Review (5 concepts due)                                  10 min
     → Trees, Queues, Stacks (concepts needing review)

  2. Continue: AVL Trees - Rotations                              45 min
     → Topic in progress, 60% done

  3. Practice exercise                                            20 min
     → Reinforce Binary Trees (detected weak point)

  Total estimated time: ~1h 15min

  SYLLABUS STATUS
  ────────────────────────────────────────────────────────────────────────────
  ✅ Completed (4):   Arrays, Lists, Stacks, Queues
  🔄 In progress (1): AVL Trees
  ⏳ Pending (3):     Graphs, Hash Tables, Sorting
  ⚠️  Rusty (2):      Stacks, Queues (need SRS review)

  QUICK ACTIONS
  ────────────────────────────────────────────────────────────────────────────
  [C] Continue where I left off (recommended)
  [R] Review concepts (SRS)
  [E] Do exercise
  [S] Exam simulation
  [P] View full plan
  [?] More options

================================================================================
```

### For PROJECT context (Spanish):
```
================================================================================
                      API DE FINANZAS PERSONALES
================================================================================

  TU PROYECTO PUEDE:
  ────────────────────────────────────────────────────────────────────────────
  ✓ Responder a peticiones HTTP
  ✓ Conectarse a la base de datos
  ✓ Listar gastos (GET /gastos)

  PRÓXIMAMENTE PODRÁ:
  → Crear gastos (POST /gastos)        ← SIGUIENTE PASO

  PROGRESO
  ────────────────────────────────────────────────────────────────────────────
  Milestone 1: Setup        [████████████████████] 100% ✓
  Milestone 2: Base de Datos [████████████████░░░░] 80%
  Milestone 3: CRUD         [████░░░░░░░░░░░░░░░░] 20%  ← AQUÍ ESTÁS
  Milestone 4: Reportes     [░░░░░░░░░░░░░░░░░░░░] 0%

  Racha: 3 días | XP: 450 | Nivel: 4

  PARA HOY
  ────────────────────────────────────────────────────────────────────────────

  1. Repaso rápido (2 conceptos vencidos)                         5 min
     → SQL queries, HTTP methods

  2. CONSTRUIR: Endpoint POST /gastos                            45 min
     → Aprenderás: validación con Pydantic, INSERT en SQL
     → Después de esto tu API podrá guardar gastos nuevos

  Tiempo total estimado: ~50 min

  SIGUIENTE PASO
  ────────────────────────────────────────────────────────────────────────────

  📍 Crear endpoint POST /gastos

  ¿POR QUÉ ESTO?
  Sin esto, los usuarios no pueden agregar gastos. Es la segunda
  operación más importante de tu API después de listar.

  ¿LISTO? Escribe /tutor:next para empezar a construir.

================================================================================
```

### For PROJECT context (English):
```
================================================================================
                      PERSONAL FINANCE API
================================================================================

  YOUR PROJECT CAN:
  ────────────────────────────────────────────────────────────────────────────
  ✓ Respond to HTTP requests
  ✓ Connect to database
  ✓ List expenses (GET /expenses)

  COMING NEXT:
  → Create expenses (POST /expenses)    ← NEXT STEP

  PROGRESS
  ────────────────────────────────────────────────────────────────────────────
  Milestone 1: Setup        [████████████████████] 100% ✓
  Milestone 2: Database     [████████████████░░░░] 80%
  Milestone 3: CRUD         [████░░░░░░░░░░░░░░░░] 20%  ← YOU ARE HERE
  Milestone 4: Reports      [░░░░░░░░░░░░░░░░░░░░] 0%

  Streak: 3 days | XP: 450 | Level: 4

  FOR TODAY
  ────────────────────────────────────────────────────────────────────────────

  1. Quick review (2 concepts due)                                5 min
     → SQL queries, HTTP methods

  2. BUILD: POST /expenses endpoint                              45 min
     → You'll learn: Pydantic validation, SQL INSERT
     → After this your API will be able to save new expenses

  Total estimated time: ~50 min

  NEXT STEP
  ────────────────────────────────────────────────────────────────────────────

  📍 Create POST /expenses endpoint

  WHY THIS?
  Without this, users can't add expenses. It's the second
  most important operation in your API after listing.

  READY? Type /tutor:next to start building.

================================================================================
```

4. **If exam is urgent (< 7 days)**, add urgency banner:

```
  ⚠️  MODO URGENTE - EXAMEN EN 5 DÍAS
  ────────────────────────────────────────────────────────────────────────────
  Enfócate en: Temas de alto peso + Puntos débiles + Simulacros

  HOY PRIORIZA:
  1. [CRÍTICO] Grafos - BFS/DFS (25% del examen, no cubierto)
  2. [IMPORTANTE] Simulacro #2 (para practicar tiempo)
  3. [RECOMENDADO] Repaso rápido de fórmulas clave
```

5. **If exam is emergency (< 3 days)**, show emergency mode:

```
  🚨 MODO EMERGENCIA - EXAMEN EN 2 DÍAS
  ────────────────────────────────────────────────────────────────────────────

  ESTRATEGIA DE ÚLTIMA HORA:
  ├── Solo repaso activo (no contenido nuevo)
  ├── Flashcards de conceptos clave
  ├── 1 simulacro rápido
  └── Descanso antes del examen

  ⚡ ACCIÓN: /tutor:exam-prep emergency
```

6. **If no configuration exists**, guide to initialization:

```
  No se encontró un proyecto de estudio en este directorio.

  Para empezar, ejecuta:
    /tutor:init

  Esto configurará tu espacio de aprendizaje personalizado.
```

## Adaptive Recommendations

The dashboard should adapt based on:

1. **Time of day**:
   - Morning: "Buen momento para contenido nuevo"
   - Evening: "Ideal para repaso y ejercicios"

2. **Progress pattern**:
   - Behind schedule: Suggest intensive mode
   - Ahead: Suggest going deeper or taking a break

3. **SRS items**: Always prioritize due items at the start

4. **Exam proximity**: Adjust recommendations based on days remaining

5. **Learning style**:
   - Visual: Suggest diagram-heavy content
   - Practical: Prioritize exercises
   - Theoretical: Suggest reading material

## After Showing Dashboard

Wait for user input. Based on their choice:
- `C` → Run `/tutor:learn` (continue)
- `R` → Show SRS review session
- `E` → Run `/tutor:exercise`
- `S` → Run `/tutor:exam-prep simulate`
- `P` → Show full study plan
- `?` → Show all available commands

## Notes

- This command should be FAST - don't make the user wait
- Always show the exam countdown if there's an exam
- Highlight items that need attention (SRS due, weak points)
- The dashboard is the primary daily entry point
- Use the user's `learning_language` for all text
