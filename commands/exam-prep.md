---
description: Exam preparation mode. Use /tutor:exam-prep to enter exam preparation mode with simulations, focused review, and adaptive strategies based on time remaining.
allowed-tools: Read, Write, Bash
---

# Command: Exam Prep

The user wants to prepare for an exam. This command provides focused exam preparation including simulations, analysis, and adaptive strategies.

## Your Task

### If called without arguments (`/tutor:exam-prep`):

Show exam preparation dashboard:

```
================================================================================
                      PREPARACIÓN DE EXAMEN
================================================================================

Asignatura: Estructuras de Datos
Fecha examen: 15/02/2026
Días restantes: 12

MODO: ESTÁNDAR (1-2 semanas)

  TU PREPARACIÓN
  ────────────────────────────────────────────────────────────────────────────
  Temario cubierto:     [████████████░░░░░░░░] 60%
  Ejercicios resueltos: [████████░░░░░░░░░░░░] 40%
  Simulacros:           [████░░░░░░░░░░░░░░░░] 1/3

  Nivel de confianza estimado: 65%

  ANÁLISIS POR TEMA (ordenado por prioridad)
  ────────────────────────────────────────────────────────────────────────────

  ⚠️  CRÍTICO (cubrir urgentemente):
  │
  ├── Grafos                    0%  [░░░░░░░░░░] Peso: 25%
  │   → Sin empezar, alto peso en examen
  │
  └── Tablas Hash              20%  [██░░░░░░░░] Peso: 10%
      → Iniciado pero incompleto

  📚 REFORZAR:
  │
  ├── Árboles AVL              60%  [██████░░░░] Peso: 15%
  │   → Rotaciones dobles aún débiles
  │
  └── Pilas/Colas              80%  [████████░░] Peso: 10%
      → Oxidado (último repaso hace 8 días)

  ✅ DOMINADOS:
  │
  └── Arrays, Listas, Árboles Binarios

  PLAN SUGERIDO (12 días)
  ────────────────────────────────────────────────────────────────────────────

  Semana 1: Cubrir pendientes
  ├── Día 1-2: Grafos básicos (BFS, DFS)
  ├── Día 3-4: Grafos avanzados (Dijkstra, etc.)
  ├── Día 5: Tablas Hash completo
  ├── Día 6: Refuerzo Árboles AVL
  └── Día 7: SIMULACRO #2

  Semana 2: Consolidar + Examen
  ├── Día 8-9: Ejercicios mixtos
  ├── Día 10: SIMULACRO #3 (completo)
  ├── Día 11: Repaso puntos débiles
  └── Día 12: Repaso ligero + EXAMEN

  ACCIONES
  ────────────────────────────────────────────────────────────────────────────
  [S] Iniciar simulacro de examen
  [F] Flashcards de repaso rápido
  [W] Trabajar en puntos débiles
  [P] Ver plan detallado día a día
  [A] Ajustar plan (cambiar horas disponibles)

================================================================================
```

### If exam is URGENT (< 7 days):

```
================================================================================
                    ⚠️  PREPARACIÓN URGENTE
================================================================================

                         EXAMEN EN 5 DÍAS

MODO: INTENSIVO

  ESTRATEGIA URGENTE
  ────────────────────────────────────────────────────────────────────────────

  PRIORIDAD 1 - Temas de alto peso no cubiertos:
  ├── Grafos (25% del examen) - DEDICAR 2 DÍAS
  └── Enfoque: Conceptos clave + ejercicios tipo examen

  PRIORIDAD 2 - Reforzar puntos débiles:
  ├── Árboles AVL - Rotaciones (1 día)
  └── Enfoque: Práctica intensiva

  PRIORIDAD 3 - Consolidar:
  ├── Simulacro completo (1 día)
  └── Repaso final (1 día)

  ⚡ NO RECOMENDADO en modo urgente:
  ├── Estudiar temas nuevos de bajo peso
  ├── Profundizar en temas ya dominados
  └── Sesiones muy largas sin descanso

  PLAN 5 DÍAS
  ────────────────────────────────────────────────────────────────────────────
  Día 1: Grafos - Conceptos + BFS/DFS           3h
  Día 2: Grafos - Dijkstra + Ejercicios         3h
  Día 3: AVL Rotaciones + Hash Tables           2.5h
  Día 4: SIMULACRO COMPLETO + Análisis          2h
  Día 5: Repaso débiles + Descanso              1.5h → EXAMEN

================================================================================
```

### If exam is EMERGENCY (< 3 days):

```
================================================================================
                    🚨 MODO EMERGENCIA
================================================================================

                        EXAMEN EN 2 DÍAS

  ESTRATEGIA DE ÚLTIMA HORA
  ────────────────────────────────────────────────────────────────────────────

  ❌ NO HAGAS:
  ├── Intentar aprender temas nuevos completos
  ├── Leer teoría extensa
  └── Sesiones de más de 2h seguidas

  ✅ ENFÓCATE EN:
  ├── Repaso activo de lo que ya sabes
  ├── Fórmulas y conceptos clave
  ├── 1 simulacro corto para practicar timing
  └── DESCANSAR bien antes del examen

  PLAN DE EMERGENCIA
  ────────────────────────────────────────────────────────────────────────────

  HOY:
  ├── 30 min: Flashcards conceptos clave
  ├── 45 min: Simulacro rápido (la mitad de preguntas)
  ├── 30 min: Revisar errores del simulacro
  └── DESCANSO

  MAÑANA (día antes del examen):
  ├── 20 min: Repaso ligero por la mañana
  ├── Tarde libre - descanso mental
  └── Dormir temprano

  DÍA DEL EXAMEN:
  ├── Repaso de 10 min de fórmulas clave
  └── ¡A por ello!

  ────────────────────────────────────────────────────────────────────────────
  💡 Consejo: En este punto, descansar bien es más importante que
     estudiar más. Tu cerebro necesita consolidar lo aprendido.
================================================================================
```

### If called with `simulate` (`/tutor:exam-prep simulate`):

First, ask for configuration:

```
================================================================================
                    CONFIGURAR SIMULACRO
================================================================================

¿Qué tipo de examen quieres simular?

  PRESETS RÁPIDOS:
  ────────────────────────────────────────────────────────────────────────────
  [1] Examen tipo test (100% opción múltiple)
  [2] Examen mixto (40% test + 30% desarrollo + 30% problemas)
  [3] Examen de desarrollo (70% desarrollo + 30% problemas)
  [4] Examen de programación (60% código + 40% problemas)
  [5] Personalizado

  > 5

  CONFIGURACIÓN PERSONALIZADA:
  ────────────────────────────────────────────────────────────────────────────

  Distribuye el porcentaje para cada tipo de pregunta (debe sumar 100%):

  Opción múltiple (multiple_choice):     [40] %
  Verdadero/Falso (true_false):          [10] %
  Respuesta corta (short_answer):        [20] %
  Desarrollo largo (long_answer):        [10] %
  Código (coding):                       [10] %
  Resolución problemas (problem_solving): [10] %
  Rellenar espacios (fill_blank):        [ 0] %
  Emparejar (matching):                  [ 0] %
                                         ─────
  TOTAL:                                  100%

  ¿Duración del simulacro? [90] minutos
  ¿Número de preguntas?    [25]
  ¿Temas a incluir?        [Todos] (o especificar IDs)

================================================================================
```

After configuration:

```
================================================================================
                      SIMULACRO DE EXAMEN #2
================================================================================

Configuración:
├── Duración: 90 minutos (como el examen real)
├── Preguntas: 25
├── Distribución:
│   ├── Test (opción múltiple): 40% (10 preguntas)
│   ├── Desarrollo corto: 20% (5 preguntas)
│   ├── Código: 20% (5 preguntas)
│   ├── Problemas: 10% (3 preguntas)
│   └── V/F: 10% (2 preguntas)
├── Sin ayudas externas

¿Listo para empezar? [S/n]

────────────────────────────────────────────────────────────────────────────────

                         ⏱️  87:23 restantes

  Pregunta 4 de 25                              [Anterior] [Siguiente]
  ────────────────────────────────────────────────────────────────────

  Tema: Árboles AVL
  Tipo: Desarrollo
  Puntos: 4

  Dado el siguiente árbol AVL, realiza la inserción del valor 15
  y muestra paso a paso las rotaciones necesarias:

           20
          /  \
        10    30
       /  \
      5   12

  Tu respuesta:
  [área de texto para respuesta]

  ────────────────────────────────────────────────────────────────────

  [Marcar para revisar]  [Saltar]  [Siguiente →]

================================================================================
```

### After completing simulation, show results:

```
================================================================================
                    RESULTADOS SIMULACRO #2
================================================================================

  NOTA ESTIMADA: 7.2 / 10   ✅ APROBADO

  Puntos: 72/100
  Tiempo: 82/90 minutos (buen ritmo)

  DESGLOSE POR TEMA
  ────────────────────────────────────────────────────────────────────────────

  TEMA                    │ ACIERTOS │ PUNTOS  │ RESULTADO
  ────────────────────────┼──────────┼─────────┼─────────────────────
  Arrays/Listas           │   3/3    │  12/12  │ ████████████████ 100%
  Pilas/Colas             │   2/3    │   8/12  │ ████████████░░░░  67%
  Árboles Binarios        │   3/4    │  12/16  │ ████████████░░░░  75%
  Árboles AVL             │   2/4    │   8/16  │ ████████░░░░░░░░  50% ⚠️
  Grafos                  │   3/5    │  16/20  │ ████████████░░░░  80%
  Hash Tables             │   2/3    │  10/12  │ ████████████░░░░  83%
  Ordenamiento            │   1/3    │   6/12  │ ████████░░░░░░░░  50% ⚠️

  ANÁLISIS
  ────────────────────────────────────────────────────────────────────────────

  ✅ Fortalezas:
  ├── Arrays y Listas - Dominio completo
  ├── Grafos - Buen nivel, mejor que el simulacro anterior
  └── Buen manejo del tiempo

  ⚠️ Puntos a reforzar:
  ├── Árboles AVL - Rotaciones dobles (2 errores)
  ├── Ordenamiento - Confusión QuickSort/MergeSort
  └── Pilas - Error en notación polaca inversa

  📈 Comparación con simulacros anteriores:
  ├── Simulacro #1: 6.5
  └── Simulacro #2: 7.2 (+0.7) ↑ Mejorando

  PLAN SUGERIDO
  ────────────────────────────────────────────────────────────────────────────
  1. Revisar rotaciones AVL (30 min)
  2. Practicar 3 ejercicios de ordenamiento
  3. Repasar notación polaca inversa

  [Ver errores detallados]  [Repetir simulacro]  [Volver al plan]

================================================================================
```

## Exam Preparation Modes

| Days Until Exam | Mode | Strategy |
|-----------------|------|----------|
| > 14 days | FULL | Complete coverage + depth |
| 7-14 days | STANDARD | Cover all + reinforce weak |
| 3-7 days | INTENSIVE | Priority topics + simulations |
| 1-3 days | EMERGENCY | Review only + rest |
| 0 days | LAST_MINUTE | Quick formulas + confidence |

## Data Storage

Simulations are stored in `.tutor/exam_simulations.json`:

```json
{
  "simulations": [
    {
      "id": "sim_20260110",
      "date": "2026-01-10",
      "score": 72,
      "duration_used": 82,
      "topics_performance": {
        "arrays": 100,
        "avl": 50,
        "graphs": 80
      }
    }
  ]
}
```

## Notes

- Adapt language based on `learning_language`
- Simulations should feel like real exam conditions
- Always provide actionable feedback after simulations
- Track progress across multiple simulations
- Encourage rest in emergency mode
