<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blueviolet?style=for-the-badge&logo=anthropic" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/version-2.0.1-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">Tutor Plugin for Claude Code</h1>

<p align="center">
  <strong>An adaptive AI-powered personal tutor for learning ANYTHING</strong>
</p>

<p align="center">
  Learn programming (any language), mathematics, sciences, languages, and more<br>
  with personalized lessons, adaptive exercises, and intelligent feedback — all within Claude Code.
</p>

---

## Why Tutor Plugin?

Learning is hard. Traditional resources often lack personalization, immediate feedback, and the ability to adapt to your pace. **Tutor Plugin** brings the power of AI directly into your development environment, creating a personalized learning experience that:

- **Teaches ANY subject** — Programming, math, science, languages, and more
- **Adapts to your level** — From complete beginner to expert
- **Uses adaptive learning** — Skill gap analysis, spaced repetition, learning style detection
- **Provides instant feedback** — Get reviews and hints in real-time
- **Tracks your progress** — Visual dashboards show your journey
- **Speaks your language** — Learn in English, Spanish, or other languages

---

## What's New in v2.0

- **Universal Subject Support** — Learn any subject, not just programming
- **Adaptive Learning Engine** — Skill gap analysis and personalized recommendations
- **Spaced Repetition System** — Optimized knowledge retention with SM-2 algorithm
- **Learning Style Detection** — Adapts content to your learning preferences
- **Comprehensive Analytics** — Detailed insights and improvement suggestions

---

## Supported Subjects

| Category | Examples |
|----------|----------|
| **Programming** | Rust, Python, TypeScript, Go, Java, C++, Ruby, PHP, Swift, Kotlin |
| **Mathematics** | Algebra, Calculus, Statistics, Linear Algebra, Discrete Math |
| **Sciences** | Physics, Chemistry, Biology, Computer Science Theory |
| **Languages** | English, Spanish, French, German, Japanese, and more |
| **Technical Skills** | System Design, DevOps, Data Science, Machine Learning |
| **Other** | Any subject you want to learn! |

---

## Features

| Feature | Description |
|---------|-------------|
| **Universal Learning** | Learn any subject with appropriate teaching methods |
| **Progressive Curriculum** | Structured learning from basics to advanced topics |
| **Adaptive Exercises** | Personalized exercises based on skill gaps and learning style |
| **Spaced Repetition** | Automatic review scheduling for optimal retention |
| **Smart Progress Tracking** | Track modules, exercises, streaks, and performance metrics |
| **Skill Gap Analysis** | Identifies and targets areas needing improvement |
| **Learning Style Adaptation** | Detects and adapts to your learning preferences |
| **Flexible Curriculum** | Generate automatically or import from external sources |
| **Educational Reviews** | Constructive feedback that teaches, not just corrects |
| **Multi-Language Interface** | Learn in English, Spanish, or other languages |
| **Three Specialized Agents** | Tutor, Evaluator, and Practice Coach working together |

---

## Quick Start

### 1. Install uv (Required)

The MCP server uses [uv](https://docs.astral.sh/uv/) to auto-manage Python dependencies.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install the Plugin

```bash
# In Claude Code
/plugin marketplace add netsirius/tutor-plugin
/plugin install tutor@netsirius-tutor-plugin
```

### 3. Start Learning!

```bash
mkdir ~/my-learning && cd ~/my-learning
claude
```

```
/tutor:init
```

The tutor will guide you through setup — choosing your subject, level, and goals.

**Example setups:**
- Learn Rust programming from scratch
- Study calculus for university
- Practice Spanish conversation
- Master system design for interviews

---

## Commands

| Command | Description |
|---------|-------------|
| `/tutor:init` | Initialize a new learning project |
| `/tutor:learn [topic]` | Start or continue a lesson |
| `/tutor:exercise [level]` | Get a practice exercise (basic/intermediate/advanced/challenge) |
| `/tutor:progress` | View your learning dashboard |
| `/tutor:review [file]` | Get educational code review |
| `/tutor:curriculum` | View, generate, or import study plans |

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        TUTOR PLUGIN                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────┐    ┌───────────┐    ┌───────────────┐          │
│   │   TUTOR   │    │ EVALUATOR │    │ PRACTICE COACH│          │
│   │  (Opus)   │    │ (Sonnet)  │    │   (Sonnet)    │          │
│   └─────┬─────┘    └─────┬─────┘    └───────┬───────┘          │
│         │                │                  │                   │
│         └────────────────┼──────────────────┘                   │
│                          │                                      │
│                    ┌─────▼─────┐                                │
│                    │    MCP    │                                │
│                    │  Server   │                                │
│                    └─────┬─────┘                                │
│                          │                                      │
│         ┌────────────────┼────────────────┐                     │
│         │                │                │                     │
│   ┌─────▼─────┐   ┌──────▼─────┐   ┌─────▼─────┐               │
│   │ Progress  │   │ Curriculum │   │ Adaptive  │               │
│   │ Tracking  │   │ Management │   │ Learning  │               │
│   └───────────┘   └────────────┘   └───────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Three Agents

- **Tutor** — Your main instructor. Explains concepts with analogies, creates lessons, and guides your learning journey.
- **Evaluator** — Reviews your code, runs tests, and provides constructive feedback tailored to your level.
- **Practice Coach** — Generates personalized exercises that challenge you just enough to grow.

---

## Daily Workflow

```bash
# Start your session
claude
/tutor:learn                    # Continue where you left off

# Practice what you learned
/tutor:exercise                 # Get an exercise for current topic

# Get help when stuck
"I don't understand this error"
"Give me a hint"
"Explain ownership another way"

# Review your code
/tutor:review src/main.rs       # Get educational feedback

# Check your progress
/tutor:progress                 # See your dashboard
```

---

## Project Structure

When you run `/tutor:init`, this structure is created:

```
your-learning-project/
├── .tutor/
│   ├── config.json         # Your preferences & settings
│   ├── progress.json       # Detailed progress data
│   ├── curriculum.json     # Your study plan
│   └── sessions/           # Session history
│
├── lessons/                # Generated lessons
│   ├── 01-basics/
│   │   ├── README.md
│   │   ├── examples/
│   │   └── exercises/
│   └── 02-ownership/
│
└── projects/               # Mini-projects
```

---

## Customization

### Learning Preferences

Edit `.tutor/config.json` in your project:

```json
{
  "learning_language": "en",
  "preferences": {
    "explanation_style": "detailed",
    "exercise_difficulty": "adaptive",
    "show_hints": true
  }
}
```

### Agent Models

Edit `agents/*.md` to change which Claude model each agent uses:

```yaml
---
model: opus     # opus, sonnet, or haiku
---
```

---

## Requirements

- **Claude Code CLI** — [Install guide](https://docs.anthropic.com/claude-code)
- **uv** — Python package manager ([Install](https://docs.astral.sh/uv/getting-started/installation/))
- **Python 3.10+** — Required by the MCP server
- **Rust** (optional) — Only if learning Rust

---

## Troubleshooting

<details>
<summary><strong>Plugin doesn't install</strong></summary>

```bash
/plugin marketplace list
/plugin marketplace add netsirius/tutor-plugin
```
</details>

<details>
<summary><strong>MCP server issues</strong></summary>

```bash
# Test MCP server manually
cd ~/.claude/plugins/cache/tutor-plugins/tutor/1.0.0
uv run server/tutor_mcp.py

# Check uv is installed
uv --version

# Restart Claude Code with debug
claude --debug
```
</details>

<details>
<summary><strong>Commands don't appear</strong></summary>

```bash
claude --debug
/plugin
```
</details>

---

## Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 hsantos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

- Built for [Claude Code](https://claude.ai/claude-code) by Anthropic
- Inspired by the need for personalized programming education

---

<p align="center">
  <strong>Happy Learning!</strong><br>
  <sub>Made with ❤️ for developers who want to level up</sub>
</p>
