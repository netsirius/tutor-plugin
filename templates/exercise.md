# Template: Exercise

Use this template when generating exercises for the student.

**CRITICAL**: All exercises MUST be created as physical files. The student works directly in these files. DO NOT present exercises only as chat messages.

**Note**: Adapt all content to the student's `learning_language` from `.tutor/config.json`.

## Required File Structure

Every exercise must be a complete, self-contained directory:

```
lessons/[module]/exercises/ex[NN]_[name]/
├── README.md           # Exercise description (student reads this first)
├── HINTS.md            # Progressive hints (student reads when stuck)
├── Cargo.toml          # Project configuration
├── src/
│   └── main.rs         # Starter code with todo!() markers
└── tests/
    └── tests.rs        # Automated tests to validate solution
```

Optional (created after completion):
```
├── REVIEW.md           # Feedback from evaluator
└── .solution/
    └── main.rs         # Reference solution (hidden)
```

## README.md Template

```markdown
# Exercise: [Descriptive Title]

| Difficulty | Topic | Time |
|------------|-------|------|
| ★★ Intermediate | [Curriculum topic] | ~20 min |

## Objective
[One sentence: what the student will learn/practice]

## Description
[Clear explanation of the problem in 2-3 paragraphs]

## Example

**Input:**
```
[example input if applicable]
```

**Expected Output:**
```
[expected result]
```

## Instructions

1. Open `src/main.rs`
2. Read the code comments to understand the structure
3. Implement the function `[function_name]`
4. Make sure to handle [specific edge case]
5. Run tests to verify:
   ```bash
   cargo test
   ```

## Success Criteria

- [ ] All tests pass
- [ ] Code compiles without warnings
- [ ] [Additional criteria]

## Need Help?

1. First, try re-reading the lesson: [link to relevant lesson]
2. If stuck, check `HINTS.md` (start with Hint 1)
3. Still stuck? Ask Claude for guidance

## When You're Done

Tell Claude: "I finished the exercise" for feedback and to record progress.
```

## HINTS.md Template

```markdown
# Hints for: [Exercise Name]

> **Try to solve without hints first!**
> Reading hints reduces your exercise score.
> Only read when truly stuck.

---

## Hint 1: Direction (Gentle nudge)

Think about [general concept]...

<details>
<summary>Click to reveal</summary>

[Soft hint about the approach without code]

</details>

---

## Hint 2: Approach (More specific)

<details>
<summary>Click to reveal</summary>

[More specific guidance, maybe mentioning a function or pattern]

```rust
// Consider using something like:
// some_function(...)
```

</details>

---

## Hint 3: Structure (Almost the answer)

<details>
<summary>Click to reveal</summary>

[Very direct hint with pseudocode or structure]

```rust
// Your solution should look something like:
fn solution() {
    // Step 1: ...
    // Step 2: ...
    // Step 3: ...
}
```

</details>

---

> Still stuck after all hints? Ask Claude: "I need more help with this exercise"
```

## src/main.rs Template

```rust
// =============================================================================
// EXERCISE: [Descriptive Title]
// =============================================================================
//
// Difficulty: ★★ (Intermediate)
// Topic: [Curriculum topic]
// Estimated time: 20 minutes
//
// INSTRUCTIONS:
// 1. Read the function signature and comments
// 2. Implement the logic where you see todo!()
// 3. Run `cargo test` to check your solution
// 4. See HINTS.md if you get stuck
//
// =============================================================================

/// [Function documentation]
///
/// # Arguments
/// * `arg1` - [description]
///
/// # Returns
/// [description]
///
/// # Examples
/// ```
/// let result = function_name(input);
/// assert_eq!(result, expected);
/// ```
fn function_name(arg1: Type) -> ReturnType {
    // TODO: Implement this function
    //
    // Your task:
    // 1. [Step 1]
    // 2. [Step 2]
    // 3. [Step 3]

    todo!("Implement your solution here")
}

fn main() {
    println!("=== Exercise: [Title] ===\n");

    // You can test your implementation here
    // let result = function_name(test_input);
    // println!("Result: {:?}", result);

    println!("Run `cargo test` to verify your solution");
}
```

## tests/tests.rs Template

```rust
//! Tests for: [Exercise Name]
//!
//! Run with: cargo test

use exercise_name::*; // Adjust based on lib.rs or inline

#[test]
fn test_basic_case() {
    // Tests the simplest valid case
    let result = function_name(basic_input);
    assert_eq!(result, expected_output);
}

#[test]
fn test_typical_case() {
    // Tests a common/typical usage
    let result = function_name(typical_input);
    assert_eq!(result, expected_output);
}

#[test]
fn test_edge_case() {
    // Tests boundary/edge cases
    let result = function_name(edge_input);
    assert_eq!(result, expected_output);
}

#[test]
#[should_panic(expected = "error message")]
fn test_invalid_input() {
    // Tests that invalid input is handled correctly
    function_name(invalid_input);
}
```

## Cargo.toml Template

```toml
[package]
name = "ex[NN]_[name]"
version = "0.1.0"
edition = "2021"

[dependencies]
# Add exercise-specific dependencies

[dev-dependencies]
# Add test dependencies
```

## Difficulty Guidelines

### ★ Basic
- Direct application of concept
- 1-2 concepts involved
- Code similar to examples
- 5-10 minutes
- 1-2 tests

### ★★ Intermediate
- Combines 2-3 concepts
- Requires adapting examples
- Small design decisions
- 15-30 minutes
- 3-4 tests

### ★★★ Advanced
- Multiple integrated concepts
- Own solution design
- Edge case handling
- 30-60 minutes
- 5+ tests

### ★★★★ Challenge
- Open-ended problem
- Multiple valid solutions
- May require research
- 1-2 hours
- Complex test scenarios

## Chat Interaction After Creating Exercise

After creating all files, tell the student:

```
📝 Exercise created!

📁 Location: lessons/[module]/exercises/ex01_[name]/
📖 Read README.md for instructions
✏️ Write your solution in src/main.rs
🧪 Run `cargo test` to check your solution
💡 If stuck, check HINTS.md (try without hints first!)

Good luck! Let me know when you're done or if you need help.
```

## Notes for the Practice Coach

1. **ALWAYS create files** - Never present exercises only in chat
2. **Clear tests** - Tests should give useful feedback when failing
3. **Progressive hints** - From vague to specific, never the complete solution
4. **Real context** - Use real-world applicable scenarios
5. **One new concept** - Introduce only one new difficulty at a time
6. **Runnable immediately** - `cargo test` should work right away (fail on todo!)
7. **Use student's language** - All text content in `learning_language`
