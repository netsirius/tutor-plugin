---
description: Reinforce mode for strengthening learned topics. Use /tutor:reinforce to review and solidify your knowledge through targeted practice, spaced repetition, and active recall exercises.
allowed-tools: Read, Write, Bash
---

# Command: Reinforce

The user wants to reinforce/strengthen topics they've already learned. This mode focuses on retention, active recall, and addressing weak points.

## Your Task

### If called without arguments (`/tutor:reinforce`):

Show reinforcement dashboard:

```
================================================================================
                         MODO REFUERZO
================================================================================

Reforzar = Consolidar lo aprendido para no olvidarlo

  TEMAS PARA REFORZAR
  ────────────────────────────────────────────────────────────────────────────

  ⚠️  OXIDADOS (necesitan atención urgente):
  │
  ├── Pilas y Colas                    Último repaso: hace 12 días
  │   └── Retención estimada: 65% ↓
  │
  └── Árboles Binarios                 Último repaso: hace 8 días
      └── Retención estimada: 72% ↓

  📊 PUNTOS DÉBILES (errores frecuentes):
  │
  ├── Árboles AVL - Rotaciones dobles  2 errores en últimos ejercicios
  │
  └── Ordenamiento - QuickSort vs Merge  Confusión detectada

  ✅ ESTABLES (buen nivel de retención):
  │
  ├── Arrays y Listas                  Retención: 95%
  └── Recursión básica                 Retención: 88%

  ACCIONES
  ────────────────────────────────────────────────────────────────────────────
  [1] Sesión de repaso SRS (5 conceptos vencidos)         ~10 min
  [2] Ejercicios de puntos débiles                        ~20 min
  [3] Quiz rápido de retención                            ~5 min
  [4] Repaso completo de un tema oxidado                  ~30 min
  [5] Flashcards activas                                  ~15 min

================================================================================
```

### If called with a topic (`/tutor:reinforce [topic]`):

```
================================================================================
                    REFORZAR: ÁRBOLES AVL
================================================================================

Estado actual:
├── Aprendido: hace 5 días
├── Última práctica: hace 3 días
├── Retención estimada: 78%
├── Punto débil: Rotaciones dobles
└── Ejercicios: 8/15 completados

  PLAN DE REFUERZO
  ────────────────────────────────────────────────────────────────────────────

  Fase 1: Repaso activo (10 min)
  ├── Flashcards de conceptos clave
  └── Factor de balance, tipos de rotación

  Fase 2: Práctica guiada (15 min)
  ├── 3 ejercicios de rotación simple
  └── 2 ejercicios de rotación doble (punto débil)

  Fase 3: Aplicación (10 min)
  ├── 1 problema de dificultad media
  └── Sin ayudas, simular condiciones de examen

  Tiempo total: ~35 min

  ¿Empezar refuerzo? [S/n]

================================================================================
```

### SRS Review Session (`/tutor:reinforce srs`):

```
================================================================================
                       REPASO SRS
================================================================================

5 conceptos vencidos para revisar hoy

  CONCEPTO 1 de 5
  ────────────────────────────────────────────────────────────────────────────

  Tema: Pilas
  Tipo: Definición

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │   ¿Qué es el principio LIFO y cómo se aplica a las pilas?              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  [Mostrar respuesta]

  ────────────────────────────────────────────────────────────────────────────

  > [Mostrar respuesta]

  RESPUESTA:
  ────────────────────────────────────────────────────────────────────────────

  LIFO = Last In, First Out (Último en entrar, primero en salir)

  En una pila:
  • push(x) - añade x al tope
  • pop() - elimina y retorna el tope
  • El último elemento añadido es el primero en ser eliminado

  Ejemplo: Pila de platos, historial del navegador, call stack

  ────────────────────────────────────────────────────────────────────────────

  ¿Qué tal lo recordabas?

  [1] Perfecto - Lo sabía sin dudar
  [2] Bien - Con algo de esfuerzo
  [3] Regular - Recordé partes
  [4] Mal - No lo recordaba
  [5] Nada - Completamente olvidado

  > 2

  ✓ Próxima revisión: en 4 días

  ────────────────────────────────────────────────────────────────────────────
  Progreso: [██░░░] 1/5                               [Continuar →]

================================================================================
```

### Quick Quiz (`/tutor:reinforce quiz`):

```
================================================================================
                      QUIZ DE RETENCIÓN
================================================================================

Quiz rápido para medir tu retención actual
10 preguntas | ~5 minutos | Temas variados

  PREGUNTA 3 de 10
  ────────────────────────────────────────────────────────────────────────────

  Tema: Árboles Binarios
  Dificultad: Media

  ¿Cuál es la complejidad temporal de búsqueda en un árbol binario
  de búsqueda balanceado?

    (a) O(1)
    (b) O(log n)
    (c) O(n)
    (d) O(n log n)

  > b

  ✓ ¡Correcto!

  Explicación: Un árbol balanceado tiene altura log(n), y la búsqueda
  recorre desde la raíz hasta potencialmente una hoja.

  ────────────────────────────────────────────────────────────────────────────
  Racha: 3 correctas                        [Siguiente →]

================================================================================
```

### After Quiz - Results:

```
================================================================================
                    RESULTADOS DEL QUIZ
================================================================================

  Puntuación: 8/10 (80%)

  DESGLOSE POR TEMA
  ────────────────────────────────────────────────────────────────────────────

  TEMA                    │ RESULTADO │ RETENCIÓN
  ────────────────────────┼───────────┼──────────────────────
  Pilas y Colas           │   2/2     │ ██████████████████ 100% ↑
  Árboles Binarios        │   2/2     │ ██████████████████ 100% ↑
  Árboles AVL             │   1/2     │ ████████████░░░░░░  67% ↓
  Listas                  │   2/2     │ ██████████████████ 100%
  Recursión               │   1/2     │ ████████████░░░░░░  67% ↓

  ANÁLISIS
  ────────────────────────────────────────────────────────────────────────────

  ✅ Fortalezas:
  ├── Pilas y Colas - Excelente retención
  └── Árboles Binarios - Bien consolidado

  ⚠️ Necesitan refuerzo:
  ├── Árboles AVL - Error en pregunta de rotaciones
  └── Recursión - Error en caso base

  RECOMENDACIÓN:
  Dedicar 15 minutos a práctica de rotaciones AVL

  [Ver errores detallados]  [Practicar puntos débiles]  [Volver]

================================================================================
```

### Flashcard Mode (`/tutor:reinforce flashcards [topic]`):

```
================================================================================
                       FLASHCARDS
================================================================================

Tema: Árboles AVL | 12 tarjetas | Modo: Aleatorio

  TARJETA 4 de 12
  ────────────────────────────────────────────────────────────────────────────

                    ┌────────────────────────────────┐
                    │                                │
                    │   ¿Qué indica un factor de    │
                    │   balance de -2 en un nodo?   │
                    │                                │
                    │                                │
                    │         [Voltear →]            │
                    │                                │
                    └────────────────────────────────┘

  ────────────────────────────────────────────────────────────────────────────

  > [Voltear]

                    ┌────────────────────────────────┐
                    │                                │
                    │   El subárbol DERECHO es más  │
                    │   alto que el izquierdo por   │
                    │   2 niveles.                  │
                    │                                │
                    │   → Requiere rotación         │
                    │     izquierda (o doble)       │
                    │                                │
                    └────────────────────────────────┘

  ¿La recordabas?
  [←] No  [→] Sí  [↑] Fácil (no mostrar más)

================================================================================
```

## Reinforcement Strategies

The system uses different strategies based on the situation:

1. **Spaced Repetition (SRS)**: For concepts that need periodic review
2. **Active Recall**: Questions that force retrieval from memory
3. **Interleaving**: Mix topics to improve discrimination
4. **Elaboration**: Connect concepts to deepen understanding
5. **Targeted Practice**: Focus on specific weak points

## When to Suggest Reinforcement

- Topic hasn't been reviewed in X days (based on SRS schedule)
- Errors detected in recent exercises
- Before exam (consolidation phase)
- User explicitly requests review
- Topic shows declining performance trend

## Data Updates

After reinforcement session, update:

1. `.tutor/srs.json` - Update review intervals
2. `.tutor/progress.json` - Update topic mastery scores
3. `.tutor/topic_status.json` - May change status (e.g., RUSTY → LEARNED)
4. Record session in `.tutor/sessions/`

## Notes

- Reinforcement should feel productive, not punishing
- Mix easy and hard items to maintain motivation
- Show progress visually (retention trends)
- Connect to exam preparation when relevant
- Use the user's `learning_language`
