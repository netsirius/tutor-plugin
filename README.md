<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.2-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-yellow?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/MCP-FastMCP-orange?style=for-the-badge" alt="MCP">
</p>

<h1 align="center">Tutor Plugin for Claude Code</h1>

<p align="center">
  <strong>AI-powered tutoring with spaced repetition, misconception tracking, and adaptive learning.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#commands">Commands</a> •
  <a href="#how-it-works">How It Works</a>
</p>

---

## Features

- **Any Subject** — Programming, math, sciences, languages, and more
- **Spaced Repetition** — SM-2 algorithm for optimal memory retention
- **Misconception Tracking** — Identifies and addresses recurring errors
- **Prerequisites Check** — Ensures you have the foundation before advancing
- **File-Based** — All content persists as Markdown for future reference
- **Adaptive Difficulty** — Adjusts based on your performance

## Installation

```bash
# Clone into your plugins directory
git clone https://github.com/yourusername/tutor-plugin ~/.claude/plugins/tutor-plugin

# Done! The plugin auto-registers with Claude Code
```

<details>
<summary>Manual setup (alternative)</summary>

```bash
git clone https://github.com/yourusername/tutor-plugin
cd tutor-plugin/server
uv sync  # or: pip install -e .
```
</details>

## Quick Start

```bash
/tutor:init              # Initialize a learning project
/tutor:learn rust        # Start learning a topic
/tutor:exercise          # Get a practice exercise
/tutor:progress          # View your stats
```

## Commands

| Command | Description |
|---------|-------------|
| `/tutor:init` | Initialize a new learning project |
| `/tutor:learn [topic]` | Start or continue a lesson |
| `/tutor:exercise [level]` | Practice (basic / intermediate / advanced / challenge) |
| `/tutor:progress` | View statistics and recommendations |
| `/tutor:curriculum` | View, generate, or import a curriculum |
| `/tutor:review [path]` | Review code with educational feedback |

## How It Works

```
You                          Tutor Plugin
 │                                │
 ├─ /tutor:init ─────────────────▶│ Creates .tutor/ config
 │                                │
 ├─ /tutor:learn "ownership" ────▶│ Checks prerequisites
 │                                │ Warns about past mistakes
 │                                │ Creates lessons/02-ownership/
 │                                │   ├── README.md
 │                                │   ├── flashcards.md
 │                                │   └── exercises/
 │                                │
 ├─ /tutor:exercise ─────────────▶│ Generates exercise
 │                                │ Evaluates your solution
 │◀── Feedback + REVIEW.md ───────│ Tracks misconceptions
 │                                │
 └─ /tutor:progress ─────────────▶│ Shows:
                                  │   • Items due for review (SRS)
                                  │   • Skill gaps
                                  │   • Recommendations
```

### Generated Structure

```
your-project/
├── .tutor/              # Config & progress data
│   ├── config.json
│   ├── progress.json
│   └── srs.json         # Spaced repetition schedule
│
└── lessons/
    └── 01-basics/
        ├── README.md       # Lesson content
        ├── flashcards.md   # Key concepts for review
        └── exercises/
            └── ex01/
                ├── README.md
                └── REVIEW.md   # Your feedback
```

## Tips

- **Questions** — Just ask directly in the chat anytime
- **More detail** — Ask "expand the section on X" or "add more examples"
- **Cheat sheets** — Ask "create a cheat-sheet for X"
- **More practice** — Ask "add more exercises on this topic"
- **Projects** — Ask "I want to build a project" to get a portfolio-ready mini-project with README, requirements, tests, and phased milestones

## License

MIT

---

<p align="center">
  Made with ❤️ for learners everywhere
</p>
