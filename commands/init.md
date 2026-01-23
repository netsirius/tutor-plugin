---
description: Initialize a new tutoring project. Use /tutor:init to configure the current directory as a learning space with progress tracking. Supports any subject and learning context - university, research, certification, professional, or self-taught.
allowed-tools: Read, Write, Bash
---

# Command: Init

The user wants to initialize a new tutoring project in the current directory.

## Your Task

1. **Check if configuration already exists**:
   - If `.tutor/` exists, ask if they want to reset or continue
   - Warn that resetting will lose current progress

2. **Ask for learning context FIRST**:

   ```
   What type of learning are you starting?

     [1] University/Institute (subject with exams)
     [2] Research (TFG/TFM/Thesis, literature review)
     [3] Professional Certification
     [4] Online Course (Coursera, Udemy, etc.)
     [5] Self-Taught (personal interest)
     [6] Professional Training (work skills)
     [7] Language Learning
     [8] Exam Preparation (competitive exams)
     [9] Build a Project (learn while building)
     [10] Get AI Project Suggestions (portfolio-ready projects)
   ```

3. **Based on context, gather specific information**:

### For UNIVERSITY/INSTITUTE context:

```
UNIVERSITY SETUP
================

a) Subject name: [e.g., "Data Structures", "Calculus II"]
b) Subject code (optional): [e.g., "CS201"]
c) Professor (optional): [name]

d) Do you have an exam date? [Y/n]
   If yes: What date? [DD/MM/YYYY]

e) Exam weight distribution (optional):
   - If they have a syllabus, ask them to paste it
   - Or they can add topics manually later

f) How much time can you dedicate per week?
   [1] Casual: 3-5 hours/week
   [2] Regular: 6-10 hours/week
   [3] Intensive: 10+ hours/week
   [4] Emergency: as much as possible

g) Preferred learning style:
   [1] Visual (diagrams, schemas, mind maps)
   [2] Practical (hands-on from day 1)
   [3] Theoretical (understand theory first)
   [4] Mixed (adapts per topic)
   [5] Let the system detect automatically
```

### For RESEARCH context:

```
RESEARCH SETUP
==============

a) Research topic: [e.g., "Machine Learning in Medical Diagnosis"]
b) Type:
   [1] TFG/TFM/Thesis
   [2] Literature Review
   [3] Exploring new field
   [4] Free research project

c) Do you have a deadline? [Y/n]
   If yes: What date? [DD/MM/YYYY]

d) Current phase:
   [1] Defining topic
   [2] Literature review
   [3] Methodology/Design
   [4] Development/Experimentation
   [5] Analysis
   [6] Writing
```

### For PROJECT context:

```
PROJECT SETUP
=============

a) What do you want to build?
   [Free text: e.g., "A REST API for personal finances"]

b) What should it be able to do when finished?
   [Free text: e.g., "Track expenses, generate reports, set budgets"]

c) What type of project is this?
   [1] Web Backend API (REST API, server)
   [2] Web Frontend (React, Vue, etc.)
   [3] Full Stack Web App (frontend + backend)
   [4] CLI Tool (command line utility)
   [5] Library/Package (reusable code)
   [6] Mobile App
   [7] Data Science/ML Project
   [8] Game
   [9] DevOps/Infrastructure
   [10] Custom (define your own structure)

d) What technologies do you want to use?
   Primary language: [e.g., "Python", "TypeScript"]
   Frameworks: [e.g., "FastAPI, SQLAlchemy"]
   Tools: [e.g., "PostgreSQL, Docker"]

e) For each technology, what's your current level?
   [1] Never used
   [2] Basic (tutorials)
   [3] Intermediate (built something)
   [4] Advanced (professional experience)

f) What do you want to learn through this project?
   [Free text: e.g., "REST APIs, database design, authentication"]

g) Overall difficulty level:
   [1] Beginner - First project of this type
   [2] Intermediate - Have built similar before
   [3] Advanced - Want to learn advanced patterns

h) Do you have a deadline? [Y/n]
   If yes: What date? [DD/MM/YYYY]

i) How much time can you dedicate per week?
   [1] Casual: 3-5 hours/week
   [2] Regular: 6-10 hours/week
   [3] Intensive: 10+ hours/week
```

After gathering project info, use the `initialize_project` tool:

```
initialize_project(
    name="Personal Finance API",
    description="REST API for tracking personal finances",
    objective="Track expenses, generate reports, set budgets",
    project_type="web_backend",  # From option c
    primary_language="python",
    technologies=["FastAPI", "PostgreSQL", "SQLAlchemy"],
    target_skills=["REST APIs", "database design", "authentication"],
    difficulty_level="intermediate",
    estimated_hours=20.0,
    use_template=True  # Use predefined tasks for the project type
)
```

This will:
1. Create a project with predefined tasks based on project type
2. Set up milestones for tracking progress
3. Generate a roadmap showing what to build
4. Each task teaches specific concepts progressively
5. Mark key tasks as milestones

If `use_template=True` and project type is not "custom":
- Backend API: setup -> models -> CRUD -> validation -> auth -> tests -> docs -> deploy
- Frontend: setup -> layout -> components -> state -> API integration -> forms -> tests -> deploy
- CLI: setup -> args -> core command -> subcommands -> error handling -> tests -> packaging
- etc.

For CUSTOM projects or when user wants full control:
1. Generate a learning plan (syllabus_units) based on the project requirements
2. Identify what the user needs to learn for each part of the project
3. Organize into milestones (significant achievements)
4. Each unit should have `why_for_goal` explaining relevance to the project
5. Mark key units as `is_milestone: true`
6. Add `task_type`, `difficulty`, `success_criteria`, `concepts_taught` to each unit

### For AI PROJECT SUGGESTIONS context (Option 10):

This is the recommended option when users want:
- AI to suggest portfolio-ready projects based on what they want to learn
- Projects tailored to their career goals (job interviews, etc.)
- Multiple project options to choose from

```
AI PROJECT SUGGESTIONS
======================

What would you like to achieve?

[1] Learn specific skills/technologies
    (e.g., "I want to learn React and REST APIs")

[2] Prepare for a career goal
    (e.g., "I'm preparing for backend developer interviews")

[3] Build an impressive GitHub portfolio
    (e.g., "I want projects that look great to recruiters")

[4] Let me describe what I need
    (free text description)
```

#### If they choose [1] Learn skills:

```
What skills or technologies do you want to learn?
(comma-separated, e.g., "REST APIs, authentication, databases")

Skills to learn: _______________

What skills do you already have? (optional)
Current skills: _______________

Preferred difficulty?
[1] Beginner
[2] Intermediate
[3] Advanced
[4] Any
```

Then use the tool:
```
suggest_projects_by_skills(
    skills_to_learn=["REST APIs", "authentication", "databases"],
    current_skills=["Python", "basic SQL"],
    difficulty="intermediate",
    limit=4
)
```

#### If they choose [2] Career goal:

```
What are you preparing for?

[1] Frontend Developer position
[2] Backend Developer position
[3] Full Stack Developer position
[4] Data Engineer position
[5] ML Engineer position
[6] DevOps/Platform Engineer position
[7] Mobile Developer position
[8] Freelance/Consulting work
[9] Startup founder
[10] Technical interview preparation
[11] Open source contribution
[12] General portfolio building
```

Then use:
```
suggest_projects_by_career(
    career_goal="backend_job",
    current_skills=["Python", "SQL"],
    limit=4
)
```

#### If they choose [3] Portfolio:

```
What type of projects interest you?

[1] Backend / APIs
[2] Frontend / UI
[3] Full Stack
[4] DevOps / Infrastructure
[5] Data / ML
[6] Mobile
[7] CLI Tools / Libraries
[8] Any - show me the most impressive options
```

Then use:
```
suggest_portfolio_projects(
    categories=["backend", "api_design"],
    current_skills=["Python"],
    limit=4
)
```

#### Present suggestions:

Show 2-4 project options with:
- Name and tagline
- Skills they'll learn
- Technologies used
- Difficulty and estimated time
- Portfolio appeal score
- Interview topics covered (if relevant)

```
## Suggested Projects

### 1. [Name] - Best Match for Your Goals

**Tagline**: [tagline]

**What you'll build**: [short description]

**Skills you'll learn**:
- [skill 1]
- [skill 2]

**Technologies**: [tech list]

**Difficulty**: Intermediate | **Time**: ~25 hours

**Portfolio Score**: 8/10
- [what makes it impressive]

---

### 2. [Another option]
...

---

Which project would you like to build? (1, 2, 3, or 4)
```

#### When they select a project:

Use `start_suggested_project(project_id)` to initialize it:

```
start_suggested_project(project_id="rest-api-auth")
```

This will:
1. Create the project with predefined tasks
2. Set up all config files
3. Ready to start with `/tutor:build`

### For OTHER contexts:

Gather relevant information:
- Subject/topic to learn
- Current level (beginner/intermediate/advanced)
- Goals (what they want to achieve)
- Available time
- Learning style preference

4. **Ask for language preference**:

```
What language do you want to learn in?
- English
- Spanish (Español)
- Other (specify)
```

5. **Create directory structure**:

```
.tutor/
├── config.json              # Main configuration
├── university_config.json   # University-specific config (if applicable)
├── progress.json            # Progress tracking
├── curriculum.json          # Study plan (if applicable)
├── topic_status.json        # Status per topic
├── study_plan.json          # Generated study plan
└── sessions/                # Session history

lessons/                     # Lesson content
projects/                    # Projects
```

6. **Create config.json** (base configuration):

```json
{
  "learning_language": "es",
  "context": "university",
  "subject_type": "programming",
  "subject": "Data Structures",
  "level": "intermediate",
  "started_at": "2026-01-09T10:00:00",
  "goals": ["Pass final exam", "Understand trees and graphs"],
  "preferences": {
    "explanation_style": "detailed",
    "exercise_difficulty": "adaptive",
    "show_hints": true,
    "learning_style": "auto_detect"
  },
  "adaptive_learning": {
    "skill_tracking": true,
    "spaced_repetition": true,
    "learning_style_detection": true
  }
}
```

7. **For UNIVERSITY context, also create university_config.json**:

```json
{
  "context": "university",
  "subject": {
    "name": "Data Structures",
    "code": "CS201",
    "professor": "Dr. García",
    "semester": "2025-2"
  },
  "exams": [
    {
      "date": "2026-02-15",
      "name": "Final Exam",
      "type": "final",
      "weight": 100,
      "duration_minutes": 120,
      "topics_included": []
    }
  ],
  "syllabus_units": [],
  "learner_profile": {
    "style": "auto_detect",
    "pace": "regular",
    "hours_per_week": 8,
    "preferred_session_minutes": 45,
    "study_days": ["mon", "tue", "wed", "thu", "fri"],
    "preferred_time": "evening"
  },
  "learning_language": "es",
  "created_at": "2026-01-09T10:00:00"
}
```

8. **Create initial progress.json**:

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

9. **Show welcome message** (in user's language):

For Spanish (University context):
```
================================================================================
                    PROYECTO DE ESTUDIO INICIALIZADO
================================================================================

Asignatura: Estructuras de Datos
Contexto: Universidad
Examen: 15/02/2026 (37 días)

Estructura creada:
├── .tutor/          → Configuración y progreso
├── lessons/         → Aquí aparecerán las lecciones
└── projects/        → Mini-proyectos

PRÓXIMOS PASOS:

  /tutor              → Dashboard inteligente (punto de entrada principal)
  /tutor:syllabus     → Añadir o importar temario
  /tutor:learn        → Empezar a aprender
  /tutor:progress     → Ver tu progreso

TIP: Usa /tutor para empezar. El sistema te guiará según tu situación.

¡Buena suerte en tu aprendizaje!
================================================================================
```

For English (University context):
```
================================================================================
                       STUDY PROJECT INITIALIZED
================================================================================

Subject: Data Structures
Context: University
Exam: 02/15/2026 (37 days)

Structure created:
├── .tutor/          → Configuration and progress
├── lessons/         → Lessons will appear here
└── projects/        → Mini-projects

NEXT STEPS:

  /tutor              → Smart dashboard (main entry point)
  /tutor:syllabus     → Add or import syllabus
  /tutor:learn        → Start learning
  /tutor:progress     → View your progress

TIP: Use /tutor to start. The system will guide you based on your situation.

Good luck on your learning journey!
================================================================================
```

For PROJECT context:
```
================================================================================
                      PROJECT-BASED LEARNING INITIALIZED
================================================================================

Project: Personal Finance API
Type: Web Backend | Difficulty: Intermediate
Objective: Track expenses, generate reports, set budgets

Technologies: Python, FastAPI, PostgreSQL
Skills to learn: REST APIs, database design, authentication

Tasks: 10 | Milestones: 3
Estimated time: ~20 hours

Structure created:
├── .tutor/          → Configuration and progress
│   └── project.json → Project tasks and milestones
├── lessons/         → Concept explanations
└── src/             → Your project code (create as needed)

NEXT STEPS:

  /tutor:project      → View project dashboard and roadmap
  /tutor:build        → Start building the next feature
  /tutor:learn [topic] → Learn about a specific concept

ROADMAP:
  [1] Setup → [2] Database → [3] CRUD → [4] Validation → ...

TIP: Run /tutor:build to start your first task!

Let's build something amazing!
================================================================================
```

## Reset Existing Project

If `.tutor/` already exists:

```
A study project already exists in this directory.

Current subject: [subject name]
Progress: [X]% complete
Last session: [date]

Options:
  [1] Continue with current project
  [2] Reset completely (you will lose all progress)
  [3] Create backup and reset

What would you like to do?
```

If they choose backup:
- Create `.tutor.backup.[date]/`
- Copy all `.tutor/` contents
- Then reset

## Key Points

- The command should be interactive but efficient
- If user gives short answers, infer reasonable defaults
- Create minimum necessary structure
- Syllabus/curriculum can be added later with /tutor:syllabus
- **learning_language** determines language for ALL generated content
- For university context, always ask about exam dates
- Guide them to use /tutor as the main entry point
