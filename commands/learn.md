---
description: Start or continue a lesson on a specific topic. Use /tutor:learn [topic] to learn something new or /tutor:learn to continue where you left off.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Command: Learn

The user wants to learn or continue learning.

## Important: Language Adaptation

Before presenting any content, read `.tutor/config.json` and check the `learning_language` field. ALL content (explanations, examples, code comments, feedback) MUST be presented in the student's chosen language.

## CRITICAL: File-Based Learning

**ALL learning content MUST be generated as physical files** in the project structure. The student reads and works with these files directly. Claude's role in chat is ONLY to:
- Guide the student through the files
- Answer questions about the content
- Provide clarifications when asked
- Correct mistakes in student's code
- Suggest when to move to the next section

**NEVER present lesson content only in chat.** Always create/update files first, then reference them.

## Your Task

### If a topic is provided (e.g., `/tutor:learn ownership`)
1. Read `.tutor/progress.json` to understand the context
2. Read `.tutor/config.json` to get the student's learning language
3. Check if the topic is in the student's curriculum
4. If there are pending prerequisites, suggest studying them first
5. **CREATE the lesson as files** in `lessons/[module]/`:
   ```
   lessons/02-ownership/
   ├── README.md              # Main lesson content
   ├── 01-concepts.md         # Conceptual explanation with analogies
   ├── 02-examples.md         # Detailed examples with explanations
   ├── examples/
   │   ├── example_01.rs      # Working code examples
   │   ├── example_02.rs
   │   └── run_examples.sh    # Script to run examples
   └── exercises/             # Practice exercises (created separately)
   ```
6. In chat, tell the student: "I've created the lesson in `lessons/[module]/`. Start by reading `README.md`"
7. Update `.tutor/progress.json` with current_module and current_topic
8. Wait for student to read and ask questions

### If no topic is provided (e.g., `/tutor:learn`)
1. Read `.tutor/progress.json`
2. Read `.tutor/config.json` to get the learning language
3. Determine the next topic according to the curriculum
4. Check if lesson files already exist for current topic:
   - If yes: Ask student where they left off, guide them through existing files
   - If no: Create the lesson files (see structure above)
5. Update progress and guide student to the files

### If it's the first time (.tutor/ doesn't exist)
1. Welcome the student
2. Ask:
   - What language would you like to learn in? (English/Spanish/Other)
   - What programming language do you want to learn?
   - What is your previous experience?
   - Do you have a specific study plan or want me to generate one?
   - How much time can you dedicate?
3. Create the initial structure:
   ```
   .tutor/
   ├── config.json      # Course configuration
   ├── progress.json    # Initial progress
   └── curriculum.json  # Study plan (generated or imported)
   ```
4. Start the first lesson

## config.json Structure
```json
{
  "learning_language": "en",
  "programming_language": "rust",
  "student_name": "name",
  "level": "beginner|intermediate|advanced",
  "started_at": "2026-01-06",
  "goals": ["Contribute to open source projects", "Create CLI tools"],
  "time_per_session": "30min|1h|2h",
  "curriculum_source": "generated|custom"
}
```

## Lesson File Structure

Each lesson module should contain:

```
lessons/[XX-module-name]/
├── README.md                 # Overview, objectives, prerequisites
├── 01-[topic].md            # First topic explanation
├── 02-[topic].md            # Second topic explanation
├── ...
├── examples/
│   ├── ex01_[name].rs       # Runnable example with comments
│   ├── ex02_[name].rs
│   └── Cargo.toml           # So examples can be run
└── exercises/               # Created by /tutor:exercise
```

### README.md Template
```markdown
# Module: [Module Name]

## Learning Objectives
After this module, you will be able to:
- [ ] [Objective 1]
- [ ] [Objective 2]
- [ ] [Objective 3]

## Prerequisites
- [Previous module or concept]

## Topics
1. [01-topic.md](01-topic.md) - Description
2. [02-topic.md](02-topic.md) - Description

## Estimated Time
~[X] hours

## How to Use This Lesson
1. Read each topic file in order
2. Run the examples in `examples/`
3. Complete exercises when suggested
4. Ask Claude if you have questions
```

## Chat Interaction Guidelines

**DO in chat:**
- "Open `lessons/02-ownership/README.md` to begin"
- "Try running `cargo run --example ex01_basic`"
- "What questions do you have about the content in `01-concepts.md`?"
- "Great question! Let me add a clarification to the file..."
- Update files with corrections or additional explanations when needed

**DON'T in chat:**
- Present entire lessons as chat messages
- Explain concepts without creating corresponding files
- Give code examples without saving them to files

## Remember
- **ALL content must exist as files** - chat is for guidance only
- Adapt the explanation level according to the student's progress
- Use real-world examples, not abstract ones
- Celebrate progress
- Offer breaks if the session is long
- **Always use the student's chosen learning language for ALL file content**
- When student asks a question, consider if the answer should be added to the lesson files
