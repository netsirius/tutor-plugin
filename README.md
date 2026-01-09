<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.2-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/claude--code-plugin-purple.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/MCP-FastMCP-orange.svg" alt="MCP">
</p>

<h1 align="center">Tutor Plugin for Claude Code</h1>

<p align="center">
  <strong>A comprehensive AI-powered tutoring system with adaptive learning, spaced repetition, and personalized feedback.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## Features

| Feature | Description |
|---------|-------------|
| **Universal Teaching** | Programming, mathematics, sciences, languages, and any subject |
| **Spaced Repetition (SM-2)** | Scientifically-proven algorithm for optimal memory retention |
| **Misconception Tracking** | Identifies and addresses recurring conceptual errors |
| **Prerequisite Verification** | Ensures students have the foundation before advancing |
| **File-Based Learning** | All content persists as files for future reference |
| **Multi-language Support** | Teach in any language (English, Spanish, etc.) |
| **Adaptive Difficulty** | Adjusts based on student performance |
| **Progress Analytics** | Detailed insights into learning patterns |

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

### Option 1: As Claude Code Plugin (Recommended)

```bash
# Clone into your plugins directory
git clone https://github.com/yourusername/tutor-plugin ~/.claude/plugins/tutor-plugin

# The plugin auto-registers with Claude Code
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/tutor-plugin
cd tutor-plugin

# Install dependencies
cd server
uv sync  # or: pip install -r requirements.txt
```

## Usage

### Quick Start

```bash
# Initialize a new learning project
/tutor:init

# Start learning a topic
/tutor:learn rust

# Get a practice exercise
/tutor:exercise intermediate

# Check your progress
/tutor:progress
```

### Commands

| Command | Description |
|---------|-------------|
| `/tutor:init` | Initialize a new learning project |
| `/tutor:learn [topic]` | Start or continue learning a topic |
| `/tutor:exercise [difficulty]` | Get a practice exercise (basic, intermediate, advanced, challenge) |
| `/tutor:progress` | View learning statistics and recommendations |
| `/tutor:curriculum` | View, generate, or import a curriculum |
| `/tutor:review [path]` | Review code with educational feedback |

### Example Workflow

```
User: /tutor:init
Tutor: What would you like to learn? (asks about subject, level, goals)

User: /tutor:learn ownership
Tutor: I've created the lesson in `lessons/02-ownership/`.
       Start by reading `README.md`.

       Note: You have 3 items due for review. Would you like to
       do a quick review first?

User: yes
Tutor: [Generates flashcards in `lessons/review-session/`]
       ...

User: /tutor:exercise
Tutor: [Creates exercise in `lessons/02-ownership/exercises/ex01/`]
```

## Architecture

```
tutor-plugin/
├── .claude-plugin/
│   └── plugin.json         # Plugin configuration
├── agents/                  # Claude agents
│   ├── tutor.md            # Main instructor (Claude Opus)
│   ├── evaluator.md        # Code reviewer (Claude Sonnet)
│   └── practice-coach.md   # Exercise generator (Claude Sonnet)
├── commands/               # CLI commands
│   ├── init.md
│   ├── learn.md
│   ├── exercise.md
│   ├── progress.md
│   ├── curriculum.md
│   └── review.md
├── server/                 # MCP server (Python)
│   ├── tutor_mcp.py       # FastMCP server entry point
│   └── learning/          # Learning engine modules
│       ├── adaptive_engine.py     # Main orchestrator
│       ├── spaced_repetition.py   # SM-2 algorithm
│       ├── misconceptions.py      # Error tracking
│       ├── prerequisites.py       # Prerequisite graph
│       ├── evaluation.py          # Multi-type evaluation
│       ├── analytics.py           # Performance metrics
│       ├── recommendations.py     # Learning suggestions
│       ├── skill_analyzer.py      # Skill gap analysis
│       └── export_import.py       # Progress backup
└── skills/                 # Reusable skills
    └── learning-tracker/
```

## API Reference

### MCP Tools

#### Progress & Session Management

| Tool | Description |
|------|-------------|
| `get_student_progress()` | Get comprehensive progress data |
| `update_exercise_progress(module_id, exercise_id, status, score, attempts)` | Update exercise status |
| `get_next_lesson()` | Get recommended next lesson |
| `start_study_session()` | Start a new study session (updates streak) |
| `end_study_session(topics_covered, exercises_completed)` | End session with summary |

#### Spaced Repetition (SM-2)

| Tool | Description |
|------|-------------|
| `get_spaced_repetition_items()` | Get items due for review |
| `record_srs_review(item_id, quality)` | Record review result (quality: 0-5) |

**Quality Scale:**
- `0` - Complete blackout
- `1` - Incorrect, remembered upon seeing answer
- `2` - Incorrect, but answer seemed easy
- `3` - Correct with serious difficulty
- `4` - Correct after hesitation
- `5` - Perfect response

#### Misconception Tracking

| Tool | Description |
|------|-------------|
| `record_misconception(exercise_id, exercise_type, topic, error_description, student_response, correct_response)` | Track a conceptual error |
| `get_misconception_analysis()` | Get analysis and remediation suggestions |
| `get_topic_warning(topic)` | Check for warnings before teaching a topic |

#### Prerequisites

| Tool | Description |
|------|-------------|
| `check_topic_readiness(topic_id)` | Verify prerequisites are met |
| `get_learning_path_to(target_topic)` | Get optimal learning path to a topic |

#### Analytics & Recommendations

| Tool | Description |
|------|-------------|
| `get_skill_gaps()` | Identify areas for improvement |
| `get_learning_recommendations(available_minutes, context)` | Personalized study suggestions |
| `get_learning_analytics()` | Comprehensive performance report |
| `record_exercise_completion(module_id, exercise_id, score, attempts, time_spent_minutes)` | Record completion with full tracking |

#### Curriculum

| Tool | Description |
|------|-------------|
| `get_curriculum()` | Get current curriculum structure |
| `save_curriculum(curriculum_data)` | Save a new curriculum (JSON string) |

#### Export/Import

| Tool | Description |
|------|-------------|
| `export_progress(format)` | Export progress (json or md) |
| `import_progress(filepath)` | Import progress from backup |

## Generated File Structure

When using the tutor, these files are created:

```
project/
├── .tutor/                    # Configuration (auto-generated)
│   ├── config.json           # Course settings
│   ├── progress.json         # Learning progress
│   ├── curriculum.json       # Course structure
│   ├── srs.json              # Spaced repetition data
│   ├── misconceptions.json   # Error tracking
│   ├── evaluations.json      # Exercise evaluations
│   └── sessions/             # Session history
│
└── lessons/                   # Learning content
    ├── 01-basics/
    │   ├── README.md         # Module overview
    │   ├── flashcards.md     # Key concepts for SRS
    │   ├── cheat-sheet.md    # Quick reference
    │   ├── concepts/
    │   │   ├── 01-variables.md
    │   │   └── 02-types.md
    │   ├── examples/
    │   │   └── hello_world.rs
    │   └── exercises/
    │       └── ex01_variables/
    │           ├── README.md
    │           ├── HINTS.md
    │           ├── src/main.rs
    │           └── REVIEW.md    # Feedback after evaluation
    ├── review-session/          # Generated for SRS reviews
    │   └── flashcards.md
    └── learning-path.md         # Generated when prerequisites missing
```

## SM-2 Algorithm

The spaced repetition system implements the [SM-2 algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2):

```
E-Factor = max(1.3, E + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))

Where:
- q = quality of response (0-5)
- E = easiness factor (starts at 2.5)
```

**Interval Progression:**
- First successful review: 1 day
- Second successful review: 6 days
- Subsequent reviews: previous interval × E-Factor

**On failure (quality < 3):**
- Reset to 1 day interval
- Keep E-Factor (for difficulty tracking)

## Development

### Running the MCP Server

```bash
cd server

# With uv (recommended)
uv run tutor_mcp.py

# Or with Python directly
python tutor_mcp.py
```

### Testing

```bash
cd server

# Test imports
python -c "from learning import *; print('All imports OK')"

# Run tests (if available)
pytest tests/
```

### Project Structure

```
server/learning/
├── __init__.py              # Public exports
├── adaptive_engine.py       # Main orchestrator (458 lines)
├── spaced_repetition.py     # SM-2 implementation (371 lines)
├── misconceptions.py        # Error tracking (617 lines)
├── prerequisites.py         # Prerequisite graph (645 lines)
├── evaluation.py            # Multi-type evaluation (547 lines)
├── analytics.py             # Performance metrics (550 lines)
├── recommendations.py       # Learning suggestions (408 lines)
├── skill_analyzer.py        # Skill gap analysis (417 lines)
└── export_import.py         # Progress backup (215 lines)
```

## Contributing

We welcome contributions! Please follow these guidelines:

### Code Style

- Python: Follow PEP 8, use type hints
- Markdown: Use consistent formatting
- Commits: Follow [Conventional Commits](https://www.conventionalcommits.org/)

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Keep modules focused and single-purpose
- Add docstrings to all public functions
- Update the README if adding new features
- Test your changes before submitting

## Changelog

### [2.0.0] - 2025-01-09

#### Removed
- `gamification.py` - Badge/XP system (unused, added complexity)
- `learning_styles.py` - VARK model (scientifically disputed)
- `knowledge_graph.py` - Merged into `prerequisites.py`

#### Changed
- Simplified `export_import.py` (606 → 215 lines)
- Simplified `tutor_mcp.py` (1210 → 1032 lines)
- Updated `tutor.md` to actively use SM-2 and misconception tracking

#### Added
- Integration of SM-2 into tutor workflow
- Misconception tracking in lesson flow
- Prerequisite verification before teaching
- Flashcard generation for each module
- `cheat-sheet.md` generation

### [1.0.0] - Initial Release

- Core tutoring functionality
- Multi-subject support
- File-based learning model
- MCP server with FastMCP

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SM-2 Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) by Piotr Wozniak
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- [Claude Code](https://claude.ai/claude-code) by Anthropic

---

<p align="center">
  Made with ❤️ for learners everywhere
</p>
