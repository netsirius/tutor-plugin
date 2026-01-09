# Tutor Plugin for Claude Code

A comprehensive tutoring system that teaches any subject with adaptive learning, spaced repetition, and personalized feedback.

## Features

- **Universal Teaching**: Programming, mathematics, sciences, languages, and any other subject
- **Spaced Repetition (SM-2)**: Scientifically-proven algorithm for optimal memory retention
- **Misconception Tracking**: Identifies and addresses recurring errors
- **Prerequisite Verification**: Ensures students have the foundation before advancing
- **File-Based Learning**: All content persists as files for future reference
- **Multi-language Support**: Teach in any language (English, Spanish, etc.)

## Installation

1. Clone this repository into your Claude Code plugins directory
2. The plugin auto-registers with Claude Code

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/tutor:init` | Initialize a new learning project |
| `/tutor:learn [topic]` | Start or continue learning |
| `/tutor:exercise [difficulty]` | Get a practice exercise |
| `/tutor:progress` | View learning statistics |
| `/tutor:curriculum` | View or import a curriculum |
| `/tutor:review` | Review code with feedback |

### Example Session

```
> /tutor:init
> /tutor:learn rust
> /tutor:exercise intermediate
> /tutor:progress
```

## Architecture

```
tutor-plugin/
├── agents/                 # Claude agents
│   ├── tutor.md           # Main instructor (Opus)
│   ├── evaluator.md       # Code reviewer (Sonnet)
│   └── practice-coach.md  # Exercise generator (Sonnet)
├── commands/              # CLI commands
├── server/                # MCP server (Python)
│   ├── tutor_mcp.py      # FastMCP server
│   └── learning/         # Learning modules
│       ├── spaced_repetition.py  # SM-2 algorithm
│       ├── misconceptions.py     # Error tracking
│       ├── prerequisites.py      # Prerequisite graph
│       ├── evaluation.py         # Multi-type evaluation
│       ├── analytics.py          # Performance metrics
│       └── ...
└── skills/                # Reusable skills
```

## MCP Tools

### Progress & Curriculum
- `get_student_progress()` - Get current progress
- `update_exercise_progress()` - Update exercise status
- `get_next_lesson()` - Get recommended next lesson
- `get_curriculum()` / `save_curriculum()` - Manage curriculum

### Spaced Repetition (SM-2)
- `get_spaced_repetition_items()` - Get items due for review
- `record_srs_review(item_id, quality)` - Record review result (0-5 scale)

### Misconception Tracking
- `record_misconception(...)` - Track a conceptual error
- `get_misconception_analysis()` - Analyze error patterns
- `get_topic_warning(topic)` - Check for warnings before teaching

### Prerequisites
- `check_topic_readiness(topic_id)` - Verify prerequisites met
- `get_learning_path_to(target)` - Get path to learn a topic

### Analytics
- `get_skill_gaps()` - Identify areas for improvement
- `get_learning_recommendations()` - Personalized suggestions
- `get_learning_analytics()` - Comprehensive report

## File Structure (Generated)

When learning, the tutor creates:

```
.tutor/                    # Configuration
├── config.json           # Course settings
├── progress.json         # Learning progress
├── curriculum.json       # Course structure
├── srs.json              # Spaced repetition data
├── misconceptions.json   # Error tracking
└── sessions/             # Session history

lessons/                   # Learning content
├── 01-basics/
│   ├── README.md         # Module overview
│   ├── flashcards.md     # Review cards
│   ├── cheat-sheet.md    # Quick reference
│   ├── concepts/         # Topic explanations
│   ├── examples/         # Working code
│   └── exercises/        # Practice exercises
└── review-session/       # SRS review materials
```

## SM-2 Algorithm

The spaced repetition system uses the SM-2 algorithm:

- **Quality 0-2**: Failed recall -> reset to day 1
- **Quality 3-5**: Successful recall -> increase interval
- **E-Factor**: Adjusts difficulty based on performance
- **Intervals**: Day 1 -> Day 6 -> Day 6*E -> ...

## Development

### Run MCP Server

```bash
cd server
uv run tutor_mcp.py
```

### Test Imports

```bash
cd server
python -c "from learning import *; print('OK')"
```

## License

MIT
