# Template: Mini-Project

Use this template when generating a practical project for the student.

**CRITICAL**: All project content MUST be created as physical files. The student works directly in these files. DO NOT present project descriptions only as chat messages.

**Note**: Adapt all content to the student's `learning_language` from `.tutor/config.json`.

## Required File Structure

Every mini-project must be a complete, self-contained directory:

```
projects/[project-name]/
├── README.md               # Project guide (student reads this first)
├── REQUIREMENTS.md         # Detailed requirements and acceptance criteria
├── Cargo.toml              # Project configuration
├── src/
│   ├── main.rs             # Entry point with TODO markers
│   └── lib.rs              # Library code (if applicable)
├── tests/
│   └── integration.rs      # Integration tests
└── docs/
    └── hints.md            # Progressive hints (optional)
```

Optional (created during/after project):
```
├── REVIEW.md               # Feedback from evaluator
└── .reference/
    └── solution.rs         # Reference implementation (hidden)
```

## README.md Template

```markdown
# Project: [Project Name]

> [One-line description of what this project does]

## Learning Objectives

By completing this project, you will practice:
- [ ] [Concept 1]
- [ ] [Concept 2]
- [ ] [Concept 3]

## The Challenge

[2-3 paragraphs describing the project, its purpose, and why it's useful]

## Features to Implement

### Phase 1: MVP (Minimum Viable Product)
Get the basics working first:
- [ ] [Feature 1]: [Brief description]
- [ ] [Feature 2]: [Brief description]

### Phase 2: Improvements
Make it better:
- [ ] [Feature 3]: [Brief description]
- [ ] [Feature 4]: [Brief description]

### Phase 3: Extras (Optional)
If you want an extra challenge:
- [ ] [Feature 5]: [Brief description]
- [ ] [Feature 6]: [Brief description]

## Usage Example

When complete, your project should work like this:

```bash
$ cargo run -- [arguments]
[Expected output]
```

## Getting Started

1. Read `REQUIREMENTS.md` for detailed specifications
2. Start with `src/main.rs` - follow the TODO comments
3. Run tests frequently: `cargo test`
4. Ask Claude if you get stuck

## Resources

- [Link to relevant documentation]
- [Link to helpful crate]
- [Link to related lesson]

## When You're Done

Tell Claude: "I finished the project" for review and feedback.
```

## REQUIREMENTS.md Template

```markdown
# Requirements: [Project Name]

## Technical Requirements

### Data Structures
- [ ] Use [struct/enum] to represent [concept]
- [ ] Implement [trait] for [purpose]

### Error Handling
- [ ] Use `Result<T, E>` for operations that can fail
- [ ] Provide clear error messages

### Code Quality
- [ ] No compiler warnings
- [ ] Run `cargo clippy` with no warnings
- [ ] Meaningful variable and function names

## Functional Requirements

### Input
- [Description of expected input format]
- [Validation requirements]

### Processing
- [What the program should do]
- [Algorithm requirements if any]

### Output
- [Description of expected output format]
- [Examples]

## Test Requirements

Your implementation should pass:
- [ ] Basic functionality tests
- [ ] Edge case tests
- [ ] Error handling tests

Run all tests with:
```bash
cargo test
```

## Evaluation Criteria

| Aspect | Weight | Description |
|--------|--------|-------------|
| Functionality | 40% | Does it work correctly? |
| Error Handling | 20% | Are errors handled gracefully? |
| Code Quality | 20% | Is the code clean and idiomatic? |
| Tests | 20% | Are there adequate tests? |

## Hints

Stuck? Check `docs/hints.md` for guidance (try without first!).
```

## src/main.rs Template

```rust
//! # [Project Name]
//!
//! [Brief description]
//!
//! ## Usage
//! ```bash
//! cargo run -- [args]
//! ```

use std::error::Error;

// TODO: Define your data structures here
// struct MyStruct { ... }

// TODO: Implement your main logic here
fn main() -> Result<(), Box<dyn Error>> {
    println!("=== [Project Name] ===\n");

    // TODO: Implement your project
    //
    // Phase 1: Start with basic functionality
    // 1. [First step]
    // 2. [Second step]
    //
    // Phase 2: Add improvements
    // 3. [Third step]
    // 4. [Fourth step]

    todo!("Implement your project here")
}

// TODO: Add helper functions as needed
// fn helper_function() { ... }
```

## tests/integration.rs Template

```rust
//! Integration tests for [Project Name]

use std::process::Command;

#[test]
fn test_basic_usage() {
    let output = Command::new("cargo")
        .args(["run", "--", "test_input"])
        .output()
        .expect("Failed to run program");

    assert!(output.status.success());
    // Add assertions about output
}

#[test]
fn test_error_handling() {
    let output = Command::new("cargo")
        .args(["run", "--", "invalid_input"])
        .output()
        .expect("Failed to run program");

    // Should handle error gracefully
    assert!(!output.status.success());
    // Check error message is helpful
}
```

## docs/hints.md Template

```markdown
# Hints for: [Project Name]

> **Try without hints first!**
> Building problem-solving skills is important.

---

## Phase 1 Hints

### Hint 1: Getting Started
<details>
<summary>Click to reveal</summary>

[General guidance for starting]

</details>

### Hint 2: Data Structures
<details>
<summary>Click to reveal</summary>

[Suggestions for structs/enums]

</details>

---

## Phase 2 Hints

### Hint 3: [Topic]
<details>
<summary>Click to reveal</summary>

[More specific guidance]

</details>

---

## Still Stuck?

Ask Claude: "I need help with [specific part] of the project"
```

## Suggested Projects by Level

### Beginner (after fundamentals)
1. **CLI Calculator** - Variables, functions, input/output
2. **Password Generator** - Strings, random, CLI arguments
3. **Unit Converter** - Structs, enums, pattern matching

### Intermediate (after ownership)
1. **Todo List** - Vectors, file I/O, structs with methods
2. **Simplified Grep** - File handling, iterators, CLI
3. **Word Counter** - HashMap, file I/O, command line

### Advanced (after traits)
1. **Markdown to HTML** - Parser, traits, generics
2. **Key-Value Store** - HashMap, serialization, persistence
3. **HTTP Request Tool** - Networking, error handling, CLI

### Expert (after async)
1. **Chat Server** - async/await, channels, networking
2. **Build Tool** - File system, processes, dependency graph
3. **Mini Database** - B-trees, file I/O, indexing

## Chat Interaction After Creating Project

After creating all files, tell the student:

```
🚀 Project created!

📁 Location: projects/[project-name]/
📖 Start by reading README.md
📋 Check REQUIREMENTS.md for detailed specs
✏️ Begin coding in src/main.rs
🧪 Run `cargo test` to check your progress

This project is designed to take 2-4 hours. Take your time!

Phases:
1. MVP - Get basic functionality working
2. Improvements - Make it better
3. Extras - Optional challenges

Let me know when you're done or if you need help!
```

## Notes for the Tutor

1. **ALWAYS create files** - Never present projects only in chat
2. **Appropriate scale** - Project should be completable in 2-4 hours
3. **Clear phases** - Dividing into phases shows visible progress
4. **Don't over-specify** - Leave room for student decisions
5. **Example code** - Provide guide snippets, not complete solutions
6. **Reference tests** - Tests define expected behavior
7. **Use student's language** - All content in `learning_language`
8. **Real-world context** - Projects should feel useful, not academic
