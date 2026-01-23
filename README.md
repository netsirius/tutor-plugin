<p align="center">
  <img src="https://img.shields.io/badge/version-3.3.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-yellow?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/MCP-FastMCP-orange?style=for-the-badge" alt="MCP">
</p>

<h1 align="center">Tutor Plugin for Claude Code</h1>

<p align="center">
  <strong>AI-powered tutoring with intelligent project suggestions, project-based learning, adaptive learning, exam preparation, and smart study planning.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#project-based-learning">Project-Based Learning</a> •
  <a href="#learning-contexts">Learning Contexts</a> •
  <a href="#commands">Commands</a> •
  <a href="#exam-preparation">Exam Preparation</a> •
  <a href="#how-it-works">How It Works</a>
</p>

---

## Features

### AI Project Suggestions (New in 3.3.0)
- **Skill-Based Suggestions** — Tell the AI what you want to learn, get portfolio-ready projects
- **Career Goal Matching** — Preparing for interviews? Get projects that cover common topics
- **Portfolio Optimization** — Projects designed to impress on GitHub
- **Multiple Options** — Choose from 2-4 suggested projects tailored to your goals

### Core Learning
- **Any Subject** — Programming, math, sciences, languages, history, and more
- **Spaced Repetition** — SM-2 algorithm for optimal memory retention
- **Misconception Tracking** — Identifies and addresses recurring errors
- **Prerequisites Check** — Ensures you have the foundation before advancing
- **Adaptive Difficulty** — Adjusts based on your performance

### University & Exam Focus
- **Exam Preparation** — Simulations with 8 question types, adaptive strategies
- **Dynamic Study Plans** — Auto-adjusts based on exam dates and available time
- **Syllabus Management** — Import, add, and track your course syllabus
- **Calendar Export** — Google Calendar, Apple Calendar, Outlook, .ics

### Learning Modes
- **Learn** — New content with explanations and examples
- **Reinforce** — Strengthen what you know with SRS and targeted practice
- **Extend** — Go deeper into mastered topics

### Personalization
- **Learning Styles** — Visual, practical, theoretical, mixed, or auto-detect
- **Multiple Contexts** — University, research, certification, self-taught, and more
- **Gamification** — XP, badges, streaks, and weekly challenges

## Installation

### Option A: From Marketplace (recommended)

```bash
# In Claude Code, run:
/plugin marketplace add hsantos/tutor-plugin
/plugin install tutor@hsantos-tutor-plugin
```

The plugin will be installed automatically with all dependencies.

### Option B: From local path

If you have the plugin cloned locally:

```bash
# In Claude Code, run:
/plugin install /path/to/tutor-plugin
```

### Option C: From GitHub URL

```bash
# In Claude Code, run:
/plugin install https://github.com/hsantos/tutor-plugin
```

### Verify Installation

After installation, restart Claude Code and run:

```bash
/tutor:init
```

If everything is configured correctly, you'll see the initialization wizard.

<details>
<summary>Manual Installation (advanced)</summary>

If the plugin system doesn't work, you can configure manually:

1. Clone the repository:
```bash
git clone https://github.com/hsantos/tutor-plugin
```

2. Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "tutor-tools": {
      "command": "/bin/bash",
      "args": ["/path/to/tutor-plugin/server/run_server.sh"],
      "env": {
        "TUTOR_PLUGIN_ROOT": "/path/to/tutor-plugin"
      }
    }
  }
}
```

3. Restart Claude Code.
</details>

<details>
<summary>Troubleshooting</summary>

**Plugin not found?**
```bash
/plugin list  # Check installed plugins
```

**Server not starting?**
```bash
# Test the server manually
cd /path/to/tutor-plugin/server
bash run_server.sh
```

**Dependencies issues?**
```bash
# Remove venv and let it recreate
rm -rf /path/to/tutor-plugin/server/.venv
```
</details>

## Quick Start

```bash
# Initialize your learning project
/tutor:init

# Check your daily dashboard (recommended entry point)
/tutor

# Start learning
/tutor:learn binary-trees

# Practice
/tutor:exercise

# Prepare for an exam
/tutor:exam-prep
```

## Learning Contexts

The tutor adapts to your learning situation:

| Context | Use Case |
|---------|----------|
| **University** | Subjects with exams, syllabus, grades |
| **Research** | TFG/TFM/Thesis, literature review |
| **Certification** | Professional certifications (AWS, etc.) |
| **Online Course** | Coursera, Udemy, etc. |
| **Self-Taught** | Personal interest learning |
| **Professional** | Work skills training |
| **Language** | Learning new languages |
| **Exam Prep** | Competitive exams, standardized tests |
| **Project** | Learn while building something real |

### Project-Based Learning (Enhanced in 3.2.0)

Learn by building a complete project from start to finish. The tutor guides you through progressive tasks that teach real-world skills.

**Project Types:**
- Web Backend API (REST APIs, databases, authentication)
- Web Frontend (React/Vue, state management, API integration)
- Full Stack (complete web applications)
- CLI Tools (argument parsing, configuration, packaging)
- Libraries (API design, testing, documentation)
- And more: Mobile, Data Science, Game, DevOps

**Features:**
- **Progressive Tasks** — Build feature by feature with clear success criteria
- **Milestones** — Celebrate achievements like "MVP Complete" or "Production Ready"
- **Capabilities Tracking** — See what your project can do as you progress
- **Architecture Decisions** — Record and learn from design choices
- **Hints System** — Get progressive hints when stuck
- **Project Templates** — Predefined tasks for common project types

See [Project-Based Learning](#project-based-learning) for full details.

## Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `/tutor` | Smart dashboard — your daily entry point |
| `/tutor:init` | Initialize a new learning project |
| `/tutor:learn [topic]` | Start or continue a lesson |
| `/tutor:next` | Get the recommended next action (adapts to context) |
| `/tutor:exercise [level]` | Practice (basic / intermediate / advanced / challenge) |
| `/tutor:progress` | View statistics and recommendations |

### University & Exam Commands

| Command | Description |
|---------|-------------|
| `/tutor:syllabus` | View, add, import, or modify your syllabus |
| `/tutor:exam-prep` | Exam preparation dashboard with simulations |
| `/tutor:calendar` | Export study plan to calendar |

### Learning Mode Commands

| Command | Description |
|---------|-------------|
| `/tutor:reinforce` | Strengthen learned topics (SRS, flashcards, quizzes) |
| `/tutor:extend` | Go deeper into mastered topics |
| `/tutor:review [path]` | Review code with educational feedback |

### Project Commands

| Command | Description |
|---------|-------------|
| `/tutor:project` | View project dashboard with roadmap and progress |
| `/tutor:build` | Build the next feature with guided implementation |
| `/tutor:project roadmap` | View visual project roadmap |
| `/tutor:project capabilities` | See what your project can do |

### AI Project Suggestions (New in 3.3.0)

| Command | Description |
|---------|-------------|
| `/tutor:suggest-project` | Get AI-suggested portfolio-ready projects |

**Usage Examples:**
- "I want to learn React and REST APIs" → Get projects that teach those skills
- "I'm preparing for backend developer interviews" → Get relevant portfolio projects
- "Show me impressive GitHub portfolio projects" → Get high-impact suggestions

### Curriculum Commands

| Command | Description |
|---------|-------------|
| `/tutor:curriculum` | View, generate, or import a curriculum |

## Project-Based Learning

Learn programming and technology skills by building real projects. Instead of isolated lessons, every concept is taught in the context of building something useful.

### Getting Started

```bash
# Initialize a project
/tutor:init
# Select option [9] "Build a Project"

# View your project dashboard
/tutor:project

# Start building
/tutor:build
```

### Project Types

| Type | What You'll Build |
|------|-------------------|
| **Web Backend** | REST API with models, CRUD, auth, tests, deployment |
| **Web Frontend** | SPA with components, state management, API integration |
| **Full Stack** | Complete web application (frontend + backend) |
| **CLI Tool** | Command-line utility with arguments, config, packaging |
| **Library** | Reusable package with API design, tests, documentation |
| **Mobile** | Mobile app with native integrations |
| **Data Science** | Data pipeline with analysis and visualization |

### How It Works

1. **Choose what to build** — Describe your project idea
2. **Select technologies** — Pick languages and frameworks to learn
3. **Get a roadmap** — System generates tasks organized by phases
4. **Build progressively** — Each task teaches new concepts
5. **Track capabilities** — See what your project can do as you progress
6. **Celebrate milestones** — MVP, Secure, Production Ready, etc.

### Example: Building a REST API

```
/tutor:init → Project → "Personal Finance API"

Roadmap generated:
├── Setup (2 tasks)
│   ├── Project Setup
│   └── Database Setup
├── Core Features (4 tasks)
│   ├── Create Models ← Milestone
│   ├── CRUD Endpoints ← Milestone
│   ├── Input Validation
│   └── Authentication ← Milestone
├── Testing (2 tasks)
│   ├── Write Tests
│   └── Documentation
└── Deploy (1 task)
    └── Deployment ← Milestone

/tutor:build

## Next Task: CRUD Endpoints

**Goal**: Basic CRUD operations available via API

**What you'll learn**:
- HTTP methods (GET, POST, PUT, DELETE)
- Route handling with FastAPI
- Response models
- Error handling

**Success Criteria**:
- [ ] POST endpoint creates resources
- [ ] GET endpoint retrieves resources
- [ ] PUT/PATCH endpoint updates resources
- [ ] DELETE endpoint removes resources
```

### Project Commands

| Command | Description |
|---------|-------------|
| `/tutor:project` | View project dashboard with roadmap |
| `/tutor:build` | Work on the next task |
| `/tutor:project roadmap` | View visual roadmap |
| `/tutor:project capabilities` | What your project can do now |

### Task Features

Each task includes:
- **Description** — What needs to be done
- **Success Criteria** — How to verify completion
- **Concepts Taught** — What you'll learn
- **Hints** — Progressive hints if stuck
- **Code Snippets** — Example patterns for reference

### Architecture Decisions

Record important design choices:

```
record_architecture_decision(
    title="Use PostgreSQL for database",
    context="Need persistent storage with relational support",
    decision="PostgreSQL with SQLAlchemy ORM",
    alternatives=["SQLite", "MongoDB"],
    concepts_learned=["Relational databases", "ORM patterns"]
)
```

These decisions become learning material for future reference.

## Exam Preparation

### Adaptive Modes

The system automatically adjusts based on time until exam:

| Days Until Exam | Mode | Strategy |
|-----------------|------|----------|
| > 14 days | **FULL** | Complete coverage + depth |
| 7-14 days | **STANDARD** | Cover all + reinforce weak |
| 3-7 days | **INTENSIVE** | Priority topics + simulations |
| 1-3 days | **EMERGENCY** | Review only + rest |
| < 1 day | **LAST_MINUTE** | Quick formulas + confidence |

### Question Types

Exam simulations support 8 question types:

| Type | Description |
|------|-------------|
| `multiple_choice` | Multiple choice (test) |
| `true_false` | True/False |
| `short_answer` | Short answer (1-3 lines) |
| `long_answer` | Long answer (essay) |
| `coding` | Code/Programming |
| `problem_solving` | Problem solving |
| `fill_blank` | Fill in the blank |
| `matching` | Matching/Relating |

### Simulation Presets

1. **Test exam** — 100% multiple choice
2. **Mixed exam** — 40% test + 30% essay + 30% problems
3. **Essay exam** — 70% essay + 30% problems
4. **Programming exam** — 60% code + 40% problems
5. **Custom** — Configure each type manually

## How It Works

```
You                              Tutor Plugin
 │                                    │
 ├─ /tutor:init ─────────────────────▶│ Creates .tutor/ config
 │   "University, Data Structures"    │ Sets up exam dates, syllabus
 │                                    │
 ├─ /tutor ──────────────────────────▶│ Smart Dashboard:
 │                                    │   • Progress overview
 │                                    │   • Exam countdown
 │                                    │   • Today's recommendations
 │                                    │   • SRS items due
 │                                    │
 ├─ /tutor:learn "AVL Trees" ────────▶│ Checks prerequisites
 │                                    │ Adapts to learning style
 │                                    │ Creates lesson content
 │                                    │
 ├─ /tutor:exam-prep simulate ───────▶│ Creates exam simulation
 │                                    │ 25 questions, 90 minutes
 │◀── Questions + Timer ──────────────│ Tracks time and answers
 │                                    │
 ├─ [Complete simulation] ───────────▶│ Results analysis:
 │◀── Score: 78% ─────────────────────│   • By topic breakdown
 │    "Focus on AVL rotations"        │   • Weak points identified
 │                                    │   • Recommendations
 │                                    │
 └─ /tutor:calendar ─────────────────▶│ Export to Google Calendar
                                      │ .ics file generated
```

### Generated Structure

```
your-project/
├── .tutor/                    # Config & progress data
│   ├── config.json            # Main configuration
│   ├── university_config.json # University-specific (exams, syllabus)
│   ├── progress.json          # Learning progress
│   ├── topic_status.json      # Status per topic
│   ├── study_plan.json        # Generated study plan
│   ├── srs.json               # Spaced repetition schedule
│   ├── exam_simulations.json  # Simulation history
│   └── sessions/              # Session history
│
├── lessons/
│   └── 01-basics/
│       ├── README.md          # Lesson content
│       ├── flashcards.md      # Key concepts for review
│       └── exercises/
│           └── ex01/
│               ├── README.md
│               └── REVIEW.md  # Your feedback
│
└── projects/                  # Mini-projects
```

## Calendar Integration

Export your study plan to any calendar:

```bash
/tutor:calendar
```

Options:
- **Google Calendar** — Direct links to add events
- **Apple Calendar** — .ics file import
- **Outlook** — .ics file import
- **Universal .ics** — Works with any calendar app

Features:
- Study sessions with descriptions
- Exam dates with reminders
- Conflict detection
- Automatic plan sync

## Learning Styles

The tutor adapts content presentation:

| Style | Approach |
|-------|----------|
| **Visual** | Diagrams, schemas, mind maps |
| **Practical** | Hands-on exercises from day 1 |
| **Theoretical** | Deep understanding of concepts first |
| **Mixed** | Balanced approach |
| **Auto-detect** | System learns your preference |

## Tips

- **Daily check** — Start with `/tutor` to see your personalized dashboard
- **SRS reviews** — Do them daily for best retention
- **Exam prep** — Start simulations at least 1 week before
- **Questions** — Just ask directly in the chat anytime
- **More detail** — Ask "expand the section on X" or "add more examples"
- **Cheat sheets** — Ask "create a cheat-sheet for X"
- **Projects** — Ask "I want to build a project" for a portfolio-ready mini-project

## MCP Tools

The plugin exposes 60+ tools via MCP:

<details>
<summary>View all tools</summary>

### Progress & Learning
- `get_student_progress` — Get current learning progress
- `update_exercise_progress` — Update exercise status
- `get_next_lesson` — Get recommended next lesson
- `start_study_session` / `end_study_session` — Session management

### University Context
- `get_university_config` — Get university configuration
- `add_exam` — Add an exam date
- `add_syllabus_unit` — Add a unit to syllabus
- `get_topic_status` / `update_topic_status` — Topic status management

### Study Planning
- `generate_study_plan` — Generate personalized study plan
- `get_today_plan` — Get today's study plan
- `get_week_overview` — Get week overview
- `adjust_study_plan` — Adjust plan for changes

### Exam Preparation
- `get_exam_prep_status` — Get exam prep mode and status
- `create_exam_simulation` — Create exam simulation
- `get_simulation_results` — Get simulation results

### Calendar
- `export_to_calendar` — Export to calendar format
- `get_calendar_events` — Get upcoming events

### Spaced Repetition
- `get_spaced_repetition_items` — Get items due for review
- `record_srs_review` — Record review result

### Adaptive Learning
- `get_skill_gaps` — Analyze skill gaps
- `get_learning_recommendations` — Get personalized recommendations
- `get_learning_style` / `update_learning_style` — Learning style management

### Gamification
- `check_achievements` — Check for new achievements
- `get_gamification_progress` — Get XP, level, badges
- `get_current_challenge` — Get weekly challenge

### Project-Based Learning
- `initialize_project` — Create a new project with tasks and milestones
- `add_project_task` — Add custom tasks to the project
- `start_build_task` — Start working on a task
- `complete_build_task` — Mark a task as completed
- `get_task_hint` — Get progressive hints for a task
- `record_architecture_decision` — Record design decisions
- `get_project_status` — Get comprehensive project status
- `get_project_capabilities` — What your project can do now
- `get_project_roadmap` — Visual roadmap with phases
- `get_next_build_task` — Next task to build
- `get_build_log` — Recent project activity

### AI Project Suggestions (New in 3.3.0)
- `suggest_projects_by_skills` — Get project suggestions based on skills to learn
- `suggest_projects_by_career` — Get projects for career goals (interviews, etc.)
- `suggest_portfolio_projects` — Get impressive portfolio projects
- `get_learnable_skills` — List all skills available across projects
- `get_career_goals` — List supported career goals
- `get_project_details` — Get full details about a suggested project
- `start_suggested_project` — Initialize a project from a suggestion

</details>

## License

MIT

---

<p align="center">
  Made with care for learners everywhere
</p>
