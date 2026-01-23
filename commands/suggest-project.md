---
description: Get AI-powered project suggestions based on what you want to learn or prepare for. Perfect for building a GitHub portfolio with projects that teach real skills.
allowed-tools: Read, Write
---

# Command: Suggest Project

The user wants project suggestions based on their learning goals or career preparation.

## Your Task

Help the user find the perfect portfolio-ready project that teaches them what they want to learn.

## Workflow

### 1. Ask What They Want

Start by understanding their goals:

```
What would you like to achieve with this project?

[1] Learn specific skills/technologies
    (e.g., "I want to learn React and APIs")

[2] Prepare for a career goal
    (e.g., "I'm preparing for backend developer interviews")

[3] Build an impressive portfolio
    (e.g., "I want projects that look great on GitHub")

[4] Let me describe what I want
    (free text)
```

### 2. Based on Selection

#### Option 1: Learn Specific Skills

Ask for details:

```
What skills or technologies do you want to learn?

Examples:
- REST APIs, authentication, databases
- React, state management, TypeScript
- Docker, CI/CD, cloud deployment
- GraphQL, real-time data, WebSockets

List the skills you want to learn (comma-separated):
```

Then ask about current skills:
```
What skills do you already have? (optional, helps match prerequisites)
```

Use the tool:
```
suggest_projects_by_skills(
    skills_to_learn=["REST APIs", "authentication", "databases"],
    current_skills=["Python", "basic SQL"],
    limit=4
)
```

#### Option 2: Career Goal

Show available goals:

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
[9] Startup or founding a company
[10] Technical interview preparation
[11] Open source contribution
[12] General portfolio building
```

Use the tool:
```
suggest_projects_by_career(
    career_goal="backend_job",
    current_skills=["Python", "SQL"],
    limit=4
)
```

#### Option 3: Portfolio Focus

Ask about preferred areas:

```
What type of projects interest you?

[1] Backend / APIs
[2] Frontend / UI
[3] Full Stack
[4] DevOps / Infrastructure
[5] Data / ML
[6] Mobile
[7] CLI Tools / Libraries
[8] Any - show me the most impressive projects
```

Use the tool:
```
suggest_portfolio_projects(
    categories=["backend", "api_design"],
    current_skills=["Python"],
    limit=4
)
```

#### Option 4: Free Description

Parse their description and use the appropriate tool based on context.

### 3. Present Suggestions

Present 2-4 project suggestions in a clear format:

```
## Project Suggestions

Based on your goals, here are the best projects for you:

---

### 1. [Project Name] ⭐ Best Match

**Tagline**: [tagline]

**What you'll build**: [description]

**Skills you'll learn**:
- [primary skill 1]
- [primary skill 2]
- [primary skill 3]

**Technologies**: [tech1], [tech2], [tech3]

**Difficulty**: [difficulty] | **Time**: ~[hours] hours

**Why it's good for your goal**:
- [relevant point 1]
- [interview topics if applicable]

**Portfolio Appeal**: [portfolio_score]/10
- [github_appeal points]

---

### 2. [Second Project]
...

---

## Quick Comparison

| Project | Skills | Difficulty | Time | Portfolio |
|---------|--------|------------|------|-----------|
| Project 1 | React, APIs | Intermediate | 35h | 9/10 |
| Project 2 | GraphQL, WS | Intermediate | 30h | 8/10 |
| ...

---

## Next Steps

Ready to start? Tell me which project you'd like to build:

- Type the **number** (1, 2, 3, or 4)
- Or say "**more details**" about a specific project
- Or say "**different options**" to see more suggestions
```

### 4. Handle Selection

When the user selects a project:

```
get_project_details(project_id="rest-api-auth")
```

Show full details:

```
## Project: [Name]

[Full description]

### Suggested Features (Core)
1. [feature 1]
2. [feature 2]
...

### Stretch Goals (Optional)
- [stretch 1]
- [stretch 2]

### Prerequisites
- [prereq 1]
- [prereq 2]

### Interview Topics This Covers
- [topic 1]
- [topic 2]

### What Makes This Portfolio-Worthy
- [appeal point 1]
- [appeal point 2]

---

Ready to start building?

- Say "**start**" to initialize this project
- Say "**customize**" to modify features before starting
- Say "**back**" to see other options
```

### 5. Start the Project

When they confirm:

```
start_suggested_project(project_id="rest-api-auth")
```

Show confirmation:

```
================================================================================
                     PROJECT INITIALIZED
================================================================================

Project: [Name]
Technologies: [tech list]

Next steps:
  /tutor:project    → View your project dashboard
  /tutor:build      → Start your first task

Your first task will be: [first task name]

Let's build something amazing!
================================================================================
```

## Available Tools

- `suggest_projects_by_skills(skills_to_learn, current_skills, difficulty, max_hours, limit)`
- `suggest_projects_by_career(career_goal, current_skills, difficulty, limit)`
- `suggest_portfolio_projects(categories, current_skills, limit)`
- `get_project_details(project_id)`
- `get_learnable_skills()` - List all learnable skills
- `get_career_goals()` - List all career goals
- `start_suggested_project(project_id)` - Initialize selected project

## Career Goals Reference

| Goal ID | Description |
|---------|-------------|
| frontend_job | Frontend Developer position |
| backend_job | Backend Developer position |
| fullstack_job | Full Stack Developer position |
| data_engineer | Data Engineer position |
| ml_engineer | ML Engineer position |
| devops_engineer | DevOps/Platform Engineer |
| mobile_developer | Mobile Developer |
| freelance | Freelance/Consulting |
| startup | Startup founder |
| portfolio | Portfolio building |
| open_source | Open source contribution |
| interview_prep | Interview preparation |

## Skill Categories Reference

| Category | Description |
|----------|-------------|
| frontend | Frontend development |
| backend | Backend development |
| fullstack | Full stack development |
| database | Database design |
| devops | DevOps and infrastructure |
| mobile | Mobile development |
| data_science | Data science |
| machine_learning | ML engineering |
| security | Security |
| testing | Testing and QA |
| architecture | System architecture |
| api_design | API design |
| cloud | Cloud platforms |
| systems | Systems programming |

## Example Conversations

### Example 1: Learning Skills

```
User: /tutor:suggest-project