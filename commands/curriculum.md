---
description: Gestionar el plan de estudios. Usa /tutor:curriculum para ver el curriculum actual, /tutor:curriculum generar para crear uno automático, o /tutor:curriculum importar para usar uno externo (ej. de Coursera).
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# Comando: Curriculum

El usuario quiere ver, generar, o importar un plan de estudios.

## Modos de Uso

### 1. Ver curriculum actual: `/tutor:curriculum`
Si existe `.tutor/curriculum.json`, muestra el plan de estudios actual con progreso.

### 2. Generar curriculum: `/tutor:curriculum generar [lenguaje]`
Genera un curriculum completo y estructurado para el lenguaje especificado.

### 3. Importar curriculum: `/tutor:curriculum importar`
Permite al usuario proporcionar un plan de estudios externo (de un curso, libro, etc.)
y lo convierte al formato del tutor.

## Estructura de curriculum.json

```json
{
  "title": "Aprendiendo Rust: De Cero a Experto",
  "language": "rust",
  "version": "1.0",
  "source": "generated|imported|custom",
  "source_details": "Basado en The Rust Book + ejercicios propios",
  "created_at": "2026-01-06",
  "total_hours_estimated": 80,
  "modules": [
    {
      "id": "01-basics",
      "title": "Fundamentos de Rust",
      "description": "Primeros pasos con Rust: instalación, sintaxis básica, y primeros programas",
      "order": 1,
      "topics": [
        {
          "id": "setup",
          "title": "Instalación y configuración",
          "description": "Instalar Rust, configurar IDE, entender Cargo",
          "resources": ["https://rust-lang.org/learn/get-started"],
          "estimated_minutes": 30
        },
        {
          "id": "hello-world",
          "title": "Hello World",
          "description": "Tu primer programa en Rust",
          "estimated_minutes": 20
        }
      ],
      "exercises": [
        {
          "id": "ex01_hello",
          "title": "Modifica Hello World",
          "difficulty": "basic",
          "topics": ["hello-world"]
        }
      ],
      "prerequisites": [],
      "estimated_hours": 4
    }
  ]
}
```

## Generar Curriculum

Cuando el usuario pida generar un curriculum:

1. Pregunta el nivel de partida:
   - Total principiante (nunca programó)
   - Principiante (sabe otro lenguaje)
   - Intermedio (algo de experiencia con el lenguaje)

2. Pregunta objetivos:
   - Desarrollo web (backend)
   - CLI tools
   - Sistemas/embedded
   - Contribuir a open source
   - Aprendizaje general

3. Pregunta tiempo disponible:
   - Casual (2-3h/semana)
   - Regular (5-10h/semana)
   - Intensivo (15h+/semana)

4. Genera un curriculum personalizado considerando:
   - Orden pedagógico correcto
   - Prerrequisitos claros
   - Ejercicios progresivos
   - Proyectos prácticos intercalados
   - Estimaciones realistas de tiempo

## Importar Curriculum

Cuando el usuario quiera importar un curriculum:

1. Solicita la fuente:
   ```
   ¿De dónde quieres importar el plan de estudios?

   1. Pegar el temario/syllabus aquí
   2. URL de un curso (Coursera, Udemy, etc.)
   3. Libro o recurso específico
   ```

2. Si pega texto:
   - Analiza la estructura
   - Identifica módulos y temas
   - Mapea a formato del tutor
   - Pregunta por aclaraciones si es necesario

3. Si proporciona URL:
   - Intenta obtener el syllabus
   - Extrae la estructura del curso
   - Convierte a formato del tutor

4. Valida con el usuario:
   ```
   He identificado la siguiente estructura:

   Módulo 1: [nombre] - X temas
   Módulo 2: [nombre] - Y temas
   ...

   ¿Es correcta? ¿Quieres ajustar algo?
   ```

5. Guarda en `.tutor/curriculum.json`

## Mostrar Curriculum

Formato visual para mostrar el curriculum:

```
📚 CURRICULUM: Rust - De Cero a Experto
═══════════════════════════════════════════════════════════════

📖 Fuente: Generado + The Rust Book
⏱️  Tiempo estimado: ~80 horas
📅 A tu ritmo actual: ~3 meses

═══════════════════════════════════════════════════════════════

MÓDULO 1: Fundamentos de Rust (✅ Completado)
├── ✅ Instalación y Cargo
├── ✅ Hello World
├── ✅ Variables y tipos
├── ✅ Funciones
└── 📝 4 ejercicios completados

MÓDULO 2: Ownership y Borrowing (🔄 En progreso - 60%)
├── ✅ El concepto de ownership
├── ✅ Referencias y borrowing
├── 🔄 Slices ← Estás aquí
├── ⬚ Lifetimes básicos
└── 📝 6/10 ejercicios completados

MÓDULO 3: Estructuras de Datos (⬚ Pendiente)
├── ⬚ Structs
├── ⬚ Enums
├── ⬚ Pattern matching
└── 📝 0/8 ejercicios

[...más módulos...]

═══════════════════════════════════════════════════════════════
💡 Usa /tutor:learn para continuar con "Slices"
```

## Modificar Curriculum

Permitir ajustes:
- Añadir módulos o temas
- Reordenar según preferencias
- Marcar temas como "ya conocido" para saltarlos
- Añadir recursos externos
