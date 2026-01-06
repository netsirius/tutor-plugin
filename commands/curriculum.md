---
description: Manage the study plan. Use /tutor:curriculum to view the current curriculum, /tutor:curriculum generate to create an automatic one, or /tutor:curriculum import to use an external one (e.g., from Coursera).
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# Command: Curriculum

The user wants to view, generate, or import a study plan.

## Important: Language Adaptation

Before presenting any content, read `.tutor/config.json` and check the `learning_language` field. ALL output MUST be presented in the student's chosen language.

## Usage Modes

### 1. View current curriculum: `/tutor:curriculum`
If `.tutor/curriculum.json` exists, show the current study plan with progress.

### 2. Generate curriculum: `/tutor:curriculum generate [language]`
Generate a complete and structured curriculum for the specified programming language.

### 3. Import curriculum: `/tutor:curriculum import`
Allows the user to provide an external study plan (from a course, book, etc.)
and converts it to the tutor format.

## curriculum.json Structure

```json
{
  "title": "Learning Rust: From Zero to Expert",
  "language": "rust",
  "version": "1.0",
  "source": "generated|imported|custom",
  "source_details": "Based on The Rust Book + custom exercises",
  "created_at": "2026-01-06",
  "total_hours_estimated": 80,
  "modules": [
    {
      "id": "01-basics",
      "title": "Rust Fundamentals",
      "description": "First steps with Rust: installation, basic syntax, and first programs",
      "order": 1,
      "topics": [
        {
          "id": "setup",
          "title": "Installation and configuration",
          "description": "Install Rust, configure IDE, understand Cargo",
          "resources": ["https://rust-lang.org/learn/get-started"],
          "estimated_minutes": 30
        },
        {
          "id": "hello-world",
          "title": "Hello World",
          "description": "Your first program in Rust",
          "estimated_minutes": 20
        }
      ],
      "exercises": [
        {
          "id": "ex01_hello",
          "title": "Modify Hello World",
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

## Generate Curriculum

When the user asks to generate a curriculum:

1. Ask for the starting level:
   - Total beginner (never programmed)
   - Beginner (knows another language)
   - Intermediate (some experience with the language)

2. Ask for goals:
   - Web development (backend)
   - CLI tools
   - Systems/embedded
   - Contribute to open source
   - General learning

3. Ask for available time:
   - Casual (2-3h/week)
   - Regular (5-10h/week)
   - Intensive (15h+/week)

4. Generate a personalized curriculum considering:
   - Correct pedagogical order
   - Clear prerequisites
   - Progressive exercises
   - Interspersed practical projects
   - Realistic time estimates

## Import Curriculum

When the user wants to import a curriculum:

1. Request the source:
   ```
   Where do you want to import the study plan from?

   1. Paste the syllabus here
   2. URL of a course (Coursera, Udemy, etc.)
   3. Specific book or resource
   ```

2. If they paste text:
   - Analyze the structure
   - Identify modules and topics
   - Map to tutor format
   - Ask for clarifications if needed

3. If they provide a URL:
   - Try to get the syllabus
   - Extract the course structure
   - Convert to tutor format

4. Validate with the user:
   ```
   I've identified the following structure:

   Module 1: [name] - X topics
   Module 2: [name] - Y topics
   ...

   Is this correct? Would you like to adjust anything?
   ```

5. Save to `.tutor/curriculum.json`

## Display Curriculum (English)

Visual format to display the curriculum:

```
📚 CURRICULUM: Rust - From Zero to Expert
═══════════════════════════════════════════════════════════════

📖 Source: Generated + The Rust Book
⏱️  Estimated time: ~80 hours
📅 At your current pace: ~3 months

═══════════════════════════════════════════════════════════════

MODULE 1: Rust Fundamentals (✅ Completed)
├── ✅ Installation and Cargo
├── ✅ Hello World
├── ✅ Variables and types
├── ✅ Functions
└── 📝 4 exercises completed

MODULE 2: Ownership and Borrowing (🔄 In progress - 60%)
├── ✅ The ownership concept
├── ✅ References and borrowing
├── 🔄 Slices ← You are here
├── ⬚ Basic lifetimes
└── 📝 6/10 exercises completed

MODULE 3: Data Structures (⬚ Pending)
├── ⬚ Structs
├── ⬚ Enums
├── ⬚ Pattern matching
└── 📝 0/8 exercises

[...more modules...]

═══════════════════════════════════════════════════════════════
💡 Use /tutor:learn to continue with "Slices"
```

## Display Curriculum (Spanish)

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

## Modify Curriculum

Allow adjustments:
- Add modules or topics
- Reorder according to preferences
- Mark topics as "already known" to skip them
- Add external resources
