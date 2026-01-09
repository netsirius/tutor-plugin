---
description: Export your study plan to calendar. Use /tutor:calendar to export to Google Calendar, Apple Calendar, Outlook, or generic .ics format.
allowed-tools: Read, Write, Bash
---

# Command: Calendar

The user wants to export their study plan to a calendar application.

## Your Task

### If called without arguments (`/tutor:calendar`):

Show calendar options:

```
================================================================================
                       EXPORTAR A CALENDARIO
================================================================================

Tu plan de estudio tiene:
├── 28 sesiones de estudio
├── 3 simulacros de examen
├── 1 examen final
└── Rango: 09/01/2026 - 15/02/2026

¿Qué quieres hacer?

  [1] Exportar a Google Calendar
  [2] Exportar a Apple Calendar (.ics)
  [3] Exportar a Outlook (.ics)
  [4] Descargar archivo .ics (universal)
  [5] Ver eventos próximos
  [6] Sincronizar con calendario existente

================================================================================
```

### If user selects Google Calendar (`/tutor:calendar google`):

```
================================================================================
                    EXPORTAR A GOOGLE CALENDAR
================================================================================

OPCIONES DE EXPORTACIÓN:

¿Qué quieres exportar?

  [1] Plan completo (todas las sesiones)
  [2] Solo exámenes y fechas clave
  [3] Solo sesiones de esta semana
  [4] Personalizado

> 1

Configuración:

  ¿Nombre del calendario?
  > Estudio - Estructuras de Datos

  ¿Color preferido?
  [1] Azul (estudio)
  [2] Rojo (exámenes)
  [3] Verde (completado)
  [4] Personalizado
  > 1

  ¿Añadir recordatorios?
  [1] 30 minutos antes
  [2] 1 hora antes
  [3] 1 día antes (para exámenes)
  [4] Personalizado
  > 1

  ¿Bloquear tiempo como "ocupado"? [S/n]
  > s

────────────────────────────────────────────────────────────────────────────────

MÉTODO DE EXPORTACIÓN:

  [1] Generar enlaces individuales (abrir en navegador)
  [2] Descargar .ics e importar manualmente
  [3] Conectar cuenta de Google (requiere autorización)

> 1

Generando enlaces...

================================================================================
                         ENLACES GENERADOS
================================================================================

Haz clic en cada enlace para añadir el evento a tu Google Calendar:

ESTA SEMANA:
────────────────────────────────────────────────────────────────────────────────

📚 Lun 13/01 18:00 - Árboles AVL - Rotaciones (1.5h)
   https://calendar.google.com/calendar/render?action=TEMPLATE&text=...

📚 Mar 14/01 18:00 - Repaso SRS + Ejercicios (1h)
   https://calendar.google.com/calendar/render?action=TEMPLATE&text=...

📚 Mié 15/01 18:00 - Grafos - Introducción (2h)
   https://calendar.google.com/calendar/render?action=TEMPLATE&text=...

📝 Sáb 18/01 10:00 - SIMULACRO #2 (1.5h)
   https://calendar.google.com/calendar/render?action=TEMPLATE&text=...

... y 24 eventos más

────────────────────────────────────────────────────────────────────────────────

¿Prefieres descargar un archivo .ics con todos los eventos? [S/n]

================================================================================
```

### If user selects .ics export:

```
================================================================================
                      ARCHIVO ICS GENERADO
================================================================================

✅ Archivo creado: .tutor/calendar_exports/estudio_estructuras_20260109.ics

Contiene:
├── 28 sesiones de estudio
├── 3 simulacros
├── 1 examen
└── Recordatorios configurados

CÓMO IMPORTAR:

  Google Calendar:
  1. Abre calendar.google.com
  2. Configuración (⚙️) → Importar y exportar
  3. Selecciona el archivo .ics
  4. Elige el calendario destino
  5. Importar

  Apple Calendar:
  1. Abre el archivo .ics
  2. Se abrirá Calendario automáticamente
  3. Selecciona el calendario destino
  4. Confirmar

  Outlook:
  1. Archivo → Abrir y exportar → Importar
  2. Selecciona "Archivo iCalendar (.ics)"
  3. Selecciona el archivo
  4. Importar

================================================================================
```

### If user selects sync (`/tutor:calendar sync`):

```
================================================================================
                     SINCRONIZACIÓN DE CALENDARIO
================================================================================

La sincronización bidireccional permite:
├── Exportar automáticamente nuevas sesiones de estudio
├── Detectar conflictos con otros eventos
├── Ajustar el plan si añades compromisos
└── Mantener todo actualizado

CONFIGURAR SINCRONIZACIÓN:

  [1] Conectar con Google Calendar (OAuth)
  [2] Usar archivo .ics compartido
  [3] Configurar sincronización manual

> 1

────────────────────────────────────────────────────────────────────────────────

Para conectar con Google Calendar necesitas autorizar el acceso.

1. Abre este enlace en tu navegador:
   https://accounts.google.com/o/oauth2/auth?client_id=...

2. Autoriza el acceso a tu calendario

3. Copia el código de autorización y pégalo aquí:
   > [código]

────────────────────────────────────────────────────────────────────────────────

✅ Conectado a Google Calendar

Calendarios disponibles:
  [1] Personal
  [2] Trabajo
  [3] Crear nuevo calendario "Estudio"

> 3

✅ Calendario "Estudio - Estructuras de Datos" creado
✅ 32 eventos sincronizados

Sincronización automática: ACTIVADA
├── Nuevos eventos se añadirán automáticamente
├── Cambios en el plan se reflejarán en el calendario
└── Conflictos te serán notificados

================================================================================
```

### Show event preview (`/tutor:calendar preview`):

```
================================================================================
                    PRÓXIMOS EVENTOS EN CALENDARIO
================================================================================

ESTA SEMANA (09/01 - 15/01):
────────────────────────────────────────────────────────────────────────────────

  Lun 13/01
  └── 18:00-19:30  📚 Árboles AVL - Rotaciones
                   Objetivo: Dominar rotaciones simples y dobles
                   Recordatorio: 30 min antes

  Mar 14/01
  └── 18:00-19:00  🔄 Repaso SRS + Ejercicios Árboles
                   5 conceptos pendientes de revisión

  Mié 15/01
  └── 18:00-20:00  📚 Grafos - Introducción
                   Tema nuevo: BFS, DFS, representaciones

  Jue 16/01
  └── 18:00-20:00  📚 Grafos - Algoritmos
                   Dijkstra, caminos mínimos

  Vie 17/01
  └── 18:00-19:30  💪 Ejercicios mixtos
                   Práctica de todos los temas

  Sáb 18/01
  └── 10:00-11:30  📝 SIMULACRO #2
                   Examen completo de práctica

PRÓXIMA SEMANA:
────────────────────────────────────────────────────────────────────────────────
  [Ver más eventos...]

FECHA CLAVE:
────────────────────────────────────────────────────────────────────────────────

  🚨 Sáb 15/02 09:00  ⚡ EXAMEN FINAL
                      Estructuras de Datos
                      Duración: 2 horas

================================================================================
```

## Event Format

Events exported include:

```
Título: 📚 Árboles AVL - Rotaciones
Hora: 18:00 - 19:30
Descripción:
  Objetivo: Dominar rotaciones simples y dobles

  Plan de la sesión:
  • Repasar concepto de balance (10 min)
  • Rotación simple izquierda/derecha (20 min)
  • Rotación doble (25 min)
  • Ejercicios prácticos (35 min)

  Abrir tutor: /tutor continue

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Progreso: 78% | Examen en 8 días

Recordatorios: 30 min antes, 5 min antes
Color: Azul
```

## Data Storage

Calendar data stored in `.tutor/calendar_events.json`:

```json
{
  "events": [
    {
      "id": "tutor_abc123",
      "title": "Árboles AVL - Rotaciones",
      "start": "2026-01-13T18:00:00",
      "end": "2026-01-13T19:30:00",
      "type": "study_session",
      "topic_id": "u4-avl",
      "description": "...",
      "reminders": [30, 5],
      "synced": true
    }
  ],
  "last_sync": "2026-01-09T10:00:00",
  "calendar_id": "google_calendar_id"
}
```

Exported files go to `.tutor/calendar_exports/`.

## Conflict Detection

When syncing, detect conflicts:

```
⚠️  CONFLICTO DETECTADO
────────────────────────────────────────────────────────────────────────────────

Tu calendario tiene un evento que conflictúa con el plan de estudio:

  Evento existente: "Cena de cumpleaños"
  Horario: Jue 16/01 19:00 - 22:00

  Sesión planificada: "Grafos - Algoritmos"
  Horario: Jue 16/01 18:00 - 20:00

¿Qué quieres hacer?

  [1] Mover sesión a otro horario (16:00-18:00)
  [2] Repartir en otros días
  [3] Acortar la sesión (18:00-19:00)
  [4] Saltar esta sesión
  [5] Ignorar conflicto

> 1

✅ Sesión movida a 16:00-18:00

================================================================================
```

## Notes

- Use user's `learning_language` for all text
- Generate valid .ics files following RFC 5545
- Include proper timezone handling
- Provide multiple export methods for flexibility
- Track sync status to avoid duplicates
