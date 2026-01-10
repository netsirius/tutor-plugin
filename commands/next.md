---
description: Get the next recommended action based on your learning context and progress. Adapts to any learning type - university, project, self-taught, etc.
allowed-tools: Read, Write, Bash, mcp__plugin_tutor_tutor-tools__get_student_progress, mcp__plugin_tutor_tutor-tools__get_next_lesson, mcp__plugin_tutor_tutor-tools__get_university_config, mcp__plugin_tutor_tutor-tools__get_topic_status, mcp__plugin_tutor_tutor-tools__get_spaced_repetition_items, mcp__plugin_tutor_tutor-tools__start_study_session
---

# Command: Next

The user wants to know what to do next. This command adapts to the learning context and provides the most appropriate next action.

## Your Task

1. **Read the configuration** to understand the context:
   - Read `.tutor/config.json` for the learning context
   - Read `.tutor/university_config.json` if exists
   - Use `get_student_progress` to check current state
   - Use `get_topic_status` to see topic states

2. **Check for urgent items first**:
   - Use `get_spaced_repetition_items` to check if anything needs review
   - If exam is near (university context), prioritize exam-related topics
   - If milestone is close (project context), focus on completing it

3. **Determine the next action based on context**:

### For UNIVERSITY context:

```
Priority order:
1. SRS items due for review → suggest /tutor:reinforce
2. Exam < 3 days → suggest /tutor:exam-prep
3. Topic in progress → continue with /tutor:learn [topic]
4. New topic available → start with /tutor:learn [next-topic]
5. All topics done → suggest /tutor:extend or exam prep
```

### For PROJECT context:

```
Priority order:
1. SRS items due for review → quick review, then continue building
2. Current task in progress → continue building that part
3. Next task available → explain what to build and why
4. Milestone close → push to complete it
5. Project complete → celebrate and suggest extensions
```

Key differences for PROJECT:
- **Learning IS building** - don't separate "learn" from "practice"
- **Contextual explanations** - always explain concepts in terms of the project
- **Deliverables** - focus on what the user can DO, not just what they know
- **Milestones** - celebrate significant achievements

### For SELF-TAUGHT/OTHER contexts:

```
Priority order:
1. SRS items due for review → suggest review
2. Topic in progress → continue learning
3. Interest-based suggestion → what seems most engaging
4. All basics done → suggest deepening or new area
```

4. **Present the recommendation clearly**:

For all contexts, show:
```
┌─────────────────────────────────────────────────────────────┐
│  NEXT STEP                                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📍 [Action]: [Brief description]                            │
│                                                              │
│  WHY THIS MATTERS:                                           │
│  [Explain why this is the right next step for their goal]    │
│                                                              │
│  AFTER THIS YOU'LL BE ABLE TO:                               │
│  [Concrete capability/deliverable they'll have]              │
│                                                              │
│  Command: /tutor:learn [topic] or just say "let's go"        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

5. **For PROJECT context specifically**:

When continuing a project task:
- Remind them what they're building
- Explain the concept they'll learn IN CONTEXT of the project
- The "exercise" IS building that part of the project
- After completing, verify understanding with a question

Example for project:
```
┌─────────────────────────────────────────────────────────────┐
│  NEXT STEP: Create endpoint GET /expenses                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  YOUR PROJECT: Finance API                                   │
│  CURRENT MILESTONE: Basic CRUD (2/4 tasks done)              │
│                                                              │
│  WHY THIS MATTERS:                                           │
│  This endpoint will let users see their expense history.     │
│  It's what any app calling your API will use to display      │
│  the list of expenses.                                       │
│                                                              │
│  AFTER THIS:                                                 │
│  ✓ Your API will be able to return expense lists             │
│  ✓ You'll understand how GET endpoints work with databases   │
│                                                              │
│  Ready? Say "let's build it" to continue.                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

6. **Start a study session** if the user agrees to continue:
   - Use `start_study_session` to track time and streak

## Key Principles

1. **Always explain WHY** - Connect every action to the user's goal
2. **Show progress in meaningful terms** - "You can now do X" not just "70% done"
3. **Adapt to context** - University ≠ Project ≠ Self-taught
4. **Keep it actionable** - One clear next step, not a list of options
5. **Verify understanding** - After completing, ask a comprehension question

## If No Configuration Exists

```
It looks like you haven't set up your learning project yet.

Run /tutor:init to get started!
```
