# /tutor:project - Project Dashboard

View your project-based learning dashboard with progress, roadmap, and capabilities.

## Required Tools

- `get_project_status`: Get comprehensive project status
- `get_project_capabilities`: Get current project capabilities
- `get_project_roadmap`: Get visual roadmap
- `get_build_log`: Get recent activity

## Workflow

### 1. Get Project Status

```
get_project_status()
```

This returns:
- Project name, description, objective
- Current phase and progress percentage
- Time spent and estimated remaining
- Current task and milestones
- Technologies and target skills

### 2. Get Project Capabilities

```
get_project_capabilities()
```

Shows what the project can currently do based on completed tasks.

### 3. Get Project Roadmap

```
get_project_roadmap()
```

Returns a visual roadmap with:
- Phases (setup, core_features, testing, polish, deploy)
- Tasks in each phase with status
- Milestones and their progress

### 4. Get Recent Activity

```
get_build_log(limit=10)
```

Shows recent project activity.

## Dashboard Format

Present the dashboard in a clear, visual format:

```
# Project: [Project Name]

**Objective**: [objective]
**Type**: [project_type] | **Difficulty**: [difficulty_level]

---

## Progress

[============================----------] 70%

**Tasks**: 7/10 completed | **Time**: 5.2h spent / ~8h remaining
**Phase**: Building

---

## Current Capabilities

Your project can now:
- [capability 1]
- [capability 2]
- [capability 3]

**Next**: [next_capability]

---

## Milestones

| Milestone | Status | Progress |
|-----------|--------|----------|
| MVP Complete | Done | 100% |
| Secure API | In Progress | 60% |
| Production Ready | Locked | 0% |

---

## Roadmap

### Setup [100%]
- [x] Project Setup
- [x] Database Setup

### Core Features [75%]
- [x] Create Models
- [x] CRUD Endpoints
- [x] Input Validation
- [ ] **Authentication** <- Current

### Testing [0%]
- [ ] Write Tests

### Deploy [0%]
- [ ] Documentation
- [ ] Deployment

---

## Recent Activity

- 2h ago: Completed "Input Validation"
- 3h ago: Started "Input Validation"
- 1d ago: Completed "CRUD Endpoints"

---

## Quick Actions

- `/tutor:build` - Work on next task
- `/tutor:learn [topic]` - Learn about a concept
- `/tutor:progress` - Detailed progress stats
```

## Subcommands

The user can specify what to view:

### /tutor:project
Full dashboard (default)

### /tutor:project roadmap
Just the roadmap:
```
get_project_roadmap()
```

### /tutor:project capabilities
Just current capabilities:
```
get_project_capabilities()
```

### /tutor:project log
Recent build activity:
```
get_build_log(limit=20)
```

### /tutor:project decisions
Architecture decisions made:
```
# Extract from project status
get_project_status()  # includes architecture_decisions
```

## No Project Initialized

If no project exists:

```
## No Project Found

You haven't started a project-based learning journey yet.

### Start a Project

Use `/tutor:init` and select "project" as your learning context.

**Popular project types**:
- **Web Backend API** - Build a REST API
- **Web Frontend** - Build a React/Vue app
- **Full Stack** - Complete web application
- **CLI Tool** - Command line utility
- **Library** - Reusable code package

### Why Project-Based Learning?

- Learn by building something real
- Progressive tasks that teach concepts
- See your skills grow with each feature
- Portfolio-ready project at the end
```

## Visual Elements

Use Unicode characters for visual appeal:

- Progress bars: `[========----------]`
- Checkmarks: `[x]` for done, `[ ]` for pending
- Arrows: `<-` for current task
- Emojis (if user prefers): Optional

## Example Output

```
# Project: Personal Finance API

**Objective**: Track personal expenses with categories and reports
**Type**: Web Backend | **Difficulty**: Intermediate

---

## Progress

[=================--------------] 55%

**Tasks**: 5/9 completed | **Time**: 3.5h spent / ~4h remaining
**Phase**: Building

---

## Current Capabilities

Your API can now:
- Create, read, update, delete expenses
- Validate all inputs with helpful errors
- Store data persistently

**Next**: User authentication

---

## Milestones

| Milestone | Status | Progress |
|-----------|--------|----------|
| MVP Complete | Done | 100% |
| Secure API | Current | 40% |
| Production Ready | Locked | 0% |

---

## Next Steps

Ready to continue? Run `/tutor:build` to work on:
**Authentication** - Implement user login and registration
```
