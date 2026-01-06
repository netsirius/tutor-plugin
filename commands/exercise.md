---
description: Get a practice exercise. Use /tutor:exercise for an exercise on the current topic, or /tutor:exercise [difficulty] where difficulty can be basic, intermediate, advanced, or challenge.
allowed-tools: Read, Write, Bash
---

# Command: Exercise

The user wants to practice with an exercise.

## Important: Language Adaptation

Before generating any content, read `.tutor/config.json` and check the `learning_language` field. ALL content (descriptions, instructions, hints, feedback) MUST be presented in the student's chosen language.

## CRITICAL: File-Based Exercises

**ALL exercises MUST be generated as physical files.** The student works directly in these files. Claude's role in chat is ONLY to:
- Tell the student where to find the exercise
- Answer questions about the requirements
- Give hints when asked (but encourage reading the hints in the file first)
- Review their solution when submitted
- Update progress when completed

**NEVER present exercise content only in chat.** Always create files first.

## Your Task

1. Read `.tutor/progress.json` to know:
   - Student's current topic
   - Appropriate difficulty level
   - Already completed exercises

2. Read `.tutor/config.json` to get the learning language

3. Determine the difficulty:
   - If specified: use the indicated one
   - If not: calculate based on progress
     - Few exercises completed → basic
     - Good performance → raise level
     - Recent difficulties → maintain or lower

4. **CREATE the exercise as files** in `lessons/[module]/exercises/`:
   ```
   lessons/02-ownership/exercises/ex01_move_semantics/
   ├── README.md           # Exercise description and objectives
   ├── Cargo.toml          # Project configuration
   ├── src/
   │   └── main.rs         # Starter code with todo!() markers
   ├── tests/
   │   └── tests.rs        # Automated tests to validate solution
   └── HINTS.md            # Progressive hints (student reads when stuck)
   ```

5. In chat, tell the student:
   ```
   Exercise created!
   📁 Location: lessons/[module]/exercises/ex01_[name]/
   📖 Read README.md for instructions
   ✏️ Write your solution in src/main.rs
   🧪 Run `cargo test` to check your solution
   💡 If stuck, check HINTS.md (try without hints first!)
   ```

6. Wait for student to work on the exercise
7. When they ask for review or run tests, evaluate and update progress

## Difficulty Levels

### basic (★)
- Direct application of the concept
- 1-2 concepts involved
- ~10 minutes

### intermediate (★★)
- Combination of concepts
- Requires thinking through the solution
- ~20-30 minutes

### advanced (★★★)
- Multiple integrated concepts
- Edge cases to consider
- ~45-60 minutes

### challenge (★★★★)
- Open-ended problem
- Multiple valid solutions
- May require research
- ~1-2 hours

## Generated Exercise Format

```rust
// =============================================================================
// Exercise: [Descriptive Title]
// Difficulty: ★★ (Intermediate)
// Topic: [Curriculum topic]
// Estimated time: 20 minutes
// =============================================================================
//
// DESCRIPTION:
// [Clear explanation of the problem to solve]
//
// EXAMPLE:
// Input: [example]
// Expected output: [result]
//
// INSTRUCTIONS:
// 1. Implement the function [name]
// 2. Make sure to handle [special case]
// 3. Run `cargo test` to verify
//
// HINTS (only if you get stuck):
// Hint 1: [soft hint]
// Hint 2: [more direct hint]
// Hint 3: [almost the solution]
// =============================================================================

fn main() {
    // Your code here
    todo!("Implement the solution")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_case() {
        // Test for the simplest case
    }
}
```

## Exercise File Templates

### README.md
```markdown
# Exercise: [Descriptive Title]

**Difficulty:** ★★ (Intermediate)
**Topic:** [Curriculum topic]
**Estimated time:** 20 minutes

## Objective
[What the student will learn/practice]

## Description
[Clear explanation of the problem to solve]

## Example
**Input:**
```
[example input]
```

**Expected Output:**
```
[expected result]
```

## Instructions
1. Open `src/main.rs`
2. Implement the function `[name]`
3. Make sure to handle [special case]
4. Run `cargo test` to verify your solution

## Success Criteria
- [ ] All tests pass
- [ ] Code handles edge cases
- [ ] [Other criteria]

## When You're Done
Tell Claude: "I finished the exercise" for review and feedback.
```

### HINTS.md
```markdown
# Hints for: [Exercise Name]

Try to solve without hints first! Only read when stuck.

---

## Hint 1 (Gentle nudge)
[Soft hint about approach]

---

## Hint 2 (More direction)
[More specific guidance]

---

## Hint 3 (Almost the answer)
[Very direct hint, almost solution]
```

## Chat Interaction Guidelines

**DO in chat:**
- "Your exercise is ready at `lessons/02-ownership/exercises/ex01_move/`"
- "Run `cargo test` in the exercise directory to check your solution"
- "Have you checked HINTS.md? Try hint 1 first."
- "Let me review your solution..." (then read their code)

**DON'T in chat:**
- Give the complete solution
- Explain hints beyond what's in HINTS.md
- Write code for the student (guide them instead)

## Remember
- **ALL exercise content must exist as files** - chat is for guidance only
- The exercise should be challenging but achievable
- Always include automated tests
- Don't reveal the solution, only progressive hints
- Celebrate when the student completes the exercise
- **Use the student's learning language for all file content**
- When student completes exercise, update `.tutor/progress.json`
