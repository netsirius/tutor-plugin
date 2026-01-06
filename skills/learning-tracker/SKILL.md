---
name: learning-tracker
description: Manages the student's learning progress. Reads and updates course state, completed modules, solved exercises, and learning metrics. This skill is used automatically when the tutor needs to know or update progress.
allowed-tools: Read, Write, Bash(python:*)
---

# Learning Tracker Skill

This skill provides capabilities to manage the student's learning progress.

## IMPORTANT: File-Based Learning Model

All learning content is stored as **physical files**. The student interacts with Claude to navigate, ask questions, and get feedback, but the **actual content lives in files**.

### Complete Project Structure
```
[project-root]/
├── .tutor/                    # Configuration and progress (managed by this skill)
│   ├── config.json            # Student preferences
│   ├── progress.json          # Module/exercise progress
│   ├── curriculum.json        # Study plan
│   └── sessions/              # Session history
│
├── lessons/                   # Learning content (created by tutor agent)
│   ├── 01-basics/
│   │   ├── README.md          # Module overview
│   │   ├── 01-variables.md    # Topic content
│   │   ├── 02-types.md
│   │   ├── common-mistakes.md # Updated as students make mistakes
│   │   ├── faq.md             # Updated as students ask questions
│   │   ├── examples/
│   │   │   ├── Cargo.toml
│   │   │   └── examples/
│   │   │       └── ex01_basic.rs
│   │   └── exercises/
│   │       └── ex01_hello/
│   │           ├── README.md
│   │           ├── HINTS.md
│   │           ├── Cargo.toml
│   │           └── src/main.rs
│   └── 02-ownership/
│       └── ...
│
└── projects/                  # Mini-projects
    └── calculator/
        ├── README.md
        ├── REQUIREMENTS.md
        └── ...
```

### Key Principle
This skill tracks **progress through files**, but agents must create the actual content as files. Never present lessons/exercises only in chat.

## State Files

### Location
All state files are saved in `.tutor/` in the current project directory:

```
.tutor/
├── config.json       # Course configuration
├── progress.json     # Detailed progress
├── curriculum.json   # Study plan
└── sessions/         # Session history
    └── YYYY-MM-DD.json
```

## Data Structure

### config.json
```json
{
  "learning_language": "en",
  "programming_language": "rust",
  "student_name": "name",
  "level": "beginner",
  "started_at": "2026-01-06T10:00:00Z",
  "goals": ["Create CLI tools", "Contribute to open source"],
  "time_per_session": "1h",
  "curriculum_source": "generated",
  "preferences": {
    "explanation_style": "detailed",
    "exercise_difficulty": "adaptive",
    "show_hints": true
  }
}
```

**Note**: The `learning_language` field determines the language for ALL content presented to the student.

### progress.json
```json
{
  "current_module": "02-ownership",
  "current_topic": "borrowing",
  "modules": {
    "01-basics": {
      "status": "completed",
      "started_at": "2026-01-06",
      "completed_at": "2026-01-08",
      "score": 92,
      "time_spent_minutes": 180,
      "exercises": {
        "ex01_hello": {"status": "completed", "attempts": 1, "score": 100},
        "ex02_variables": {"status": "completed", "attempts": 2, "score": 85}
      }
    },
    "02-ownership": {
      "status": "in_progress",
      "started_at": "2026-01-09",
      "exercises": {
        "ex01_ownership": {"status": "completed", "attempts": 3, "score": 75},
        "ex02_borrowing": {"status": "in_progress", "attempts": 1}
      }
    }
  },
  "statistics": {
    "total_time_minutes": 420,
    "total_exercises_completed": 15,
    "total_exercises_attempted": 18,
    "average_score": 85,
    "streak_days": 5,
    "last_session": "2026-01-10"
  }
}
```

## Available Operations

### 1. Initialize Course
When `.tutor/` doesn't exist, create the initial structure:

```python
# Use the utility script
python ${SKILL_ROOT}/scripts/progress.py init --language rust --level beginner
```

### 2. Load Progress
Read the student's current state:

```python
python ${SKILL_ROOT}/scripts/progress.py get
```

Returns JSON with all progress.

### 3. Update Progress
After completing a lesson or exercise:

```python
# Complete exercise
python ${SKILL_ROOT}/scripts/progress.py complete-exercise \
  --module "02-ownership" \
  --exercise "ex02_borrowing" \
  --score 90 \
  --attempts 2

# Complete module
python ${SKILL_ROOT}/scripts/progress.py complete-module \
  --module "02-ownership" \
  --score 88
```

### 4. Record Session
At the start and end of each study session:

```python
# Start session
python ${SKILL_ROOT}/scripts/progress.py start-session

# End session
python ${SKILL_ROOT}/scripts/progress.py end-session \
  --topics-covered "borrowing,slices" \
  --exercises-done 3
```

### 5. Get Recommendations
Determine what to study next:

```python
python ${SKILL_ROOT}/scripts/progress.py recommend
```

Returns the next topic based on:
- Completed prerequisites
- Areas that need reinforcement
- Time since last practice

### 6. Generate Report
Create a progress summary:

```python
python ${SKILL_ROOT}/scripts/progress.py report
```

## Metrics Calculation

### Exercise Score
- 100 points: Completed on first attempt
- -10 points per additional attempt
- Minimum 60 points if completed

### Module Score
- Weighted average of exercises
- Bonus for completing without skipping exercises

### Streak
- Counts consecutive days with activity
- Resets if more than 24h pass without studying
- Consider student's timezone

### Mastery Level
Based on cumulative score:
- < 70: Needs reinforcement
- 70-85: Competent
- 85-95: Proficient
- > 95: Expert

## Usage in Agents

Tutor agents should:

1. **At session start**: Load progress to contextualize
2. **After each exercise**: Update progress immediately
3. **When giving feedback**: Consider student history
4. **When suggesting next step**: Use recommendations

## Integration Example

```
1. User says "continue with the course"
2. Tutor executes: python progress.py get
3. Reads that they're on module 02, topic "borrowing"
4. Checks if lesson files exist: lessons/02-ownership/
   - If YES: Guide student to the files ("Open lessons/02-ownership/README.md")
   - If NO: CREATE the lesson files first, then guide student
5. Student works through the files, asks questions in chat
6. On exercise completion, executes: python progress.py complete-exercise ...
7. Suggests next topic based on: python progress.py recommend
```

## File-Based Workflow

### When Teaching
```
Tutor: "Let me create the lesson for you..."
       [Creates lessons/02-ownership/ with all files]
       "I've created the lesson. Open lessons/02-ownership/README.md to begin."

Student: [Reads files, runs examples]
         "I don't understand borrowing"

Tutor: "Good question! Let me add a clarification..."
       [Updates lessons/02-ownership/01-borrowing.md with FAQ section]
       "I've added more explanation to the file. Check the FAQ section."
```

### When Practicing
```
Student: "/tutor:exercise"

Coach: [Creates lessons/02-ownership/exercises/ex01_move/]
       "Exercise ready! Check lessons/02-ownership/exercises/ex01_move/README.md"

Student: [Works on src/main.rs, runs cargo test]
         "I'm done!"

Evaluator: [Reads student's code, runs tests]
           [Creates REVIEW.md in exercise directory]
           "Great job! I've saved feedback to REVIEW.md. Score: 85/100"
           [Updates .tutor/progress.json]
```
