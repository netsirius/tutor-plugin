---
description: Manage your study syllabus. Use /tutor:syllabus to view, add, import, or modify your study topics. Supports importing from text, PDF descriptions, or manual entry.
allowed-tools: Read, Write, Bash
---

# Command: Syllabus

The user wants to manage their syllabus (temario). This command allows viewing, adding, importing, and modifying study topics.

## Your Task

### If called without arguments (`/tutor:syllabus`):

Show current syllabus status and options:

```
================================================================================
                              TEMARIO
================================================================================

Asignatura: Estructuras de Datos
Temas: 8 unidades | 24 subtemas

  #  │ UNIDAD                      │ PESO  │ ESTADO      │ HORAS
  ───┼─────────────────────────────┼───────┼─────────────┼───────
  1  │ Arrays y Listas             │  10%  │ ✅ Dominado │  4h
  2  │ Pilas y Colas               │  10%  │ ✅ Dominado │  3h
  3  │ Árboles Binarios            │  15%  │ 🔄 80%      │  5h
  4  │ Árboles AVL                 │  15%  │ 🔄 60%      │  6h
  5  │ Grafos                      │  20%  │ ⏳ Nuevo    │  8h
  6  │ Tablas Hash                 │  10%  │ ⏳ Nuevo    │  4h
  7  │ Ordenamiento                │  15%  │ ⏳ Nuevo    │  5h
  8  │ Búsqueda                    │   5%  │ ⏳ Nuevo    │  2h

  Total: 37 horas estimadas | 35% completado

OPCIONES:
  [A] Añadir tema nuevo
  [I] Importar temario (texto/descripción)
  [M] Modificar tema existente
  [R] Eliminar tema
  [P] Cambiar prioridades/pesos
  [V] Ver detalle de un tema
  [G] Generar plan de estudio

================================================================================
```

### If called with `add` (`/tutor:syllabus add`):

Interactive topic addition:

```
AÑADIR NUEVO TEMA
=================

Nombre del tema: [input]
Descripción (opcional): [input]

¿Entra en el examen? [S/n]: s
Peso aproximado en examen (1-100): [input]

Horas estimadas de estudio: [input]

¿Tiene prerequisitos? [S/n]: s
Selecciona prerequisitos:
  [1] Arrays y Listas
  [2] Pilas y Colas
  [3] Árboles Binarios
  ...

Subtemas (separados por coma, opcional):
[input]

────────────────────────────────────────────────────────────────

✅ Tema añadido: "Tablas Hash"
   Peso: 10% | Horas: 4h | Prerequisitos: Arrays

⚠️  PLAN ACTUALIZADO:
   Antes: 14 días | 8 temas | 1.5h/día
   Ahora: 14 días | 9 temas | 1.7h/día (+12 min/día)

¿Quieres regenerar el plan de estudio? [S/n]
```

### If called with `import` (`/tutor:syllabus import`):

```
IMPORTAR TEMARIO
================

¿Cómo quieres importar el temario?

  [1] Pegar texto (copia del syllabus del profesor)
  [2] Describir los temas (yo extraigo la estructura)
  [3] Desde URL (si está online)
  [4] Importar de archivo local

> 1

Pega el temario a continuación (termina con una línea vacía):
──────────────────────────────────────────────────────────────
[User pastes syllabus text]
──────────────────────────────────────────────────────────────

Analizando...

He detectado 8 temas principales:

  1. Introducción a Estructuras de Datos
  2. Arrays y Listas Enlazadas
  3. Pilas (Stacks)
  4. Colas (Queues)
  5. Árboles Binarios
  6. Árboles Balanceados (AVL, Red-Black)
  7. Grafos y Algoritmos
  8. Tablas Hash

¿Es correcto? [S/n/editar]

Estimando pesos y tiempos basándome en la descripción...

  #  │ TEMA                        │ PESO  │ HORAS │ PREREQUISITOS
  ───┼─────────────────────────────┼───────┼───────┼───────────────
  1  │ Introducción                │   5%  │  2h   │ -
  2  │ Arrays y Listas             │  10%  │  4h   │ 1
  3  │ Pilas                       │  10%  │  3h   │ 2
  4  │ Colas                       │  10%  │  3h   │ 2
  5  │ Árboles Binarios            │  15%  │  5h   │ 2
  6  │ Árboles Balanceados         │  15%  │  6h   │ 5
  7  │ Grafos                      │  25%  │  8h   │ 2, 5
  8  │ Tablas Hash                 │  10%  │  4h   │ 2

¿Quieres ajustar algo? [S/n]

✅ Temario importado: 8 temas, 35 horas totales

¿Generar plan de estudio ahora? [S/n]
```

### If called with `modify` (`/tutor:syllabus modify [topic]`):

```
MODIFICAR TEMA: Árboles AVL
===========================

Valores actuales:
  Nombre: Árboles AVL
  Descripción: Árboles binarios auto-balanceados
  Peso: 15%
  Horas estimadas: 6h
  Prerequisitos: Árboles Binarios
  Subtemas: Rotaciones, Factor de balance, Inserción, Eliminación

¿Qué quieres modificar?
  [1] Nombre
  [2] Descripción
  [3] Peso en examen
  [4] Horas estimadas
  [5] Prerequisitos
  [6] Subtemas
  [7] Todo (formulario completo)

> 3

Nuevo peso en examen (actual: 15%): 20

✅ Peso actualizado: 15% → 20%

⚠️  Esto afecta las prioridades del plan de estudio.
¿Regenerar plan? [S/n]
```

### If called with `remove` (`/tutor:syllabus remove [topic]`):

```
ELIMINAR TEMA
=============

⚠️  Vas a eliminar: "Tablas Hash"

Estado actual:
  - Progreso: 0% (no iniciado)
  - Ejercicios: 0 completados

¿Estás seguro? [s/N]: s

✅ Tema eliminado

Nota: Si ya habías estudiado este tema, el progreso se conserva
en el historial pero no cuenta para el plan actual.
```

### If called with `weights` (`/tutor:syllabus weights`):

```
AJUSTAR PESOS DEL EXAMEN
========================

Distribuye los pesos según la importancia en el examen.
El total debe sumar 100%.

  TEMA                      │ PESO ACTUAL │ NUEVO PESO
  ──────────────────────────┼─────────────┼───────────
  Arrays y Listas           │     10%     │ [  ]
  Pilas y Colas             │     10%     │ [  ]
  Árboles Binarios          │     15%     │ [  ]
  Árboles AVL               │     15%     │ [  ]
  Grafos                    │     20%     │ [  ]
  Tablas Hash               │     10%     │ [  ]
  Ordenamiento              │     15%     │ [  ]
  Búsqueda                  │      5%     │ [  ]
  ──────────────────────────┼─────────────┼───────────
  TOTAL                     │    100%     │ [  ]

Tip: Los temas con mayor peso se priorizarán cuando quede poco
tiempo para el examen.
```

## Data Storage

Topics are stored in `.tutor/university_config.json` under `syllabus_units`:

```json
{
  "syllabus_units": [
    {
      "id": "u1-arrays",
      "name": "Arrays y Listas",
      "description": "Estructuras de datos lineales básicas",
      "weight": 10,
      "estimated_hours": 4,
      "order": 1,
      "prerequisites": [],
      "topics": ["arrays", "listas_enlazadas", "listas_dobles"],
      "resources": []
    }
  ]
}
```

Topic status is stored in `.tutor/topic_status.json`:

```json
{
  "u1-arrays": "mastered",
  "u2-stacks": "learned",
  "u3-trees": "in_progress",
  "u4-graphs": "new"
}
```

## After Modifying Syllabus

1. Always offer to regenerate the study plan
2. If exam is close, warn about time implications
3. Update topic_status.json for new topics (set to "new")
4. Recalculate total hours and check against available time

## Notes

- Use the user's `learning_language` for all output
- When importing, be smart about detecting structure from messy text
- Allow partial information - the system can estimate missing values
- Always show the impact of changes on the study plan
- Keep prerequisite chains logical
