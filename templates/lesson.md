# Template: Lesson

Use this template when generating a lesson for the student.

**CRITICAL**: All lesson content MUST be created as physical files in the project. The student reads these files directly. DO NOT present lessons only as chat messages.

**Note**: Adapt all content to the student's `learning_language` from `.tutor/config.json`.

## Required File Structure

When creating a lesson, generate this complete directory structure:

```
lessons/[XX-module-name]/
├── README.md                    # Module overview (use template below)
├── 01-[first-topic].md         # First topic content
├── 02-[second-topic].md        # Second topic content
├── ...
├── common-mistakes.md          # Common errors (add as students encounter them)
├── faq.md                      # Frequently asked questions (add as students ask)
├── examples/
│   ├── Cargo.toml              # So examples can be run
│   ├── src/
│   │   └── lib.rs              # Example library (if needed)
│   └── examples/
│       ├── ex01_basic.rs       # cargo run --example ex01_basic
│       ├── ex02_intermediate.rs
│       └── ...
└── exercises/                  # Created separately by /tutor:exercise
```

## README.md Template (Module Overview)

```markdown
# Module [XX]: [Module Name]

## Learning Objectives

After completing this module, you will be able to:
- [ ] [Objective 1]
- [ ] [Objective 2]
- [ ] [Objective 3]

## Prerequisites

Before starting, make sure you understand:
- [Link to previous module](../XX-previous-module/README.md)
- [Specific concept needed]

## Topics in This Module

| # | Topic | File | Time |
|---|-------|------|------|
| 1 | [Topic Name] | [01-topic.md](01-topic.md) | ~30 min |
| 2 | [Topic Name] | [02-topic.md](02-topic.md) | ~45 min |
| ... | ... | ... | ... |

## How to Use This Module

1. **Read** each topic file in order
2. **Run** the examples in `examples/`:
   ```bash
   cd examples
   cargo run --example ex01_basic
   ```
3. **Practice** with exercises when suggested (use `/tutor:exercise`)
4. **Ask Claude** if you have questions about the content

## Quick Reference

[A summary table or cheat-sheet students can reference later]

## When You're Done

- [ ] All topics read
- [ ] Examples run and understood
- [ ] At least 2 exercises completed

Tell Claude: "I finished module [XX]" to mark complete and continue.
```

## Topic File Template (01-[topic].md)

```markdown
# [Topic Title]

## Why This Matters
[Context and motivation - 2-3 paragraphs max]

## The Concept

### Definition
[Clear, concise explanation]

### Analogy
[Comparison with everyday life to aid understanding]

### Visual
```
[ASCII diagram if helpful]
┌─────────────┐
│   Concept   │
└─────────────┘
```

## How It Works

### Basic Syntax
```rust
// Basic example
// See: examples/ex01_basic.rs for runnable version
```

### Step by Step
```rust
// Example with line-by-line comments
fn example() {
    // 1. First we do this
    // 2. Then this happens
}
```

## Common Use Cases

### Case 1: [Name]
```rust
// See: examples/ex01_basic.rs
```

### Case 2: [Name]
```rust
// See: examples/ex02_intermediate.rs
```

## What Can Go Wrong

> See also: [common-mistakes.md](common-mistakes.md)

### Error: [Description]
```rust
// ❌ This won't work
```
**Why:** [Explanation]

**Fix:**
```rust
// ✅ Do this instead
```

## Try It Yourself

Ready to practice? Ask Claude:
```
/tutor:exercise
```

## Summary

**Key takeaways:**
- [Point 1]
- [Point 2]
- [Point 3]

**Next:** [02-next-topic.md](02-next-topic.md)
```

## examples/Cargo.toml Template

```toml
[package]
name = "module_XX_examples"
version = "0.1.0"
edition = "2021"

[[example]]
name = "ex01_basic"
path = "examples/ex01_basic.rs"

[[example]]
name = "ex02_intermediate"
path = "examples/ex02_intermediate.rs"

[dependencies]
# Add as needed
```

## Example File Template (examples/ex01_basic.rs)

```rust
//! Example: [Title]
//!
//! Run with: cargo run --example ex01_basic
//!
//! This example demonstrates:
//! - [Point 1]
//! - [Point 2]

fn main() {
    println!("=== [Example Title] ===\n");

    // Example code with detailed comments
    // explaining what each part does

    println!("\nTry modifying this example to see what happens!");
}
```

## Notes for the Tutor

1. **ALWAYS create files** - Never present lessons only in chat
2. **Adapt the level** - Adjust vocabulary and examples for student's level
3. **Be progressive** - Start simple, increase complexity gradually
4. **Use real examples** - Avoid "foo", "bar" - use descriptive names
5. **Connect knowledge** - Reference previous concepts already mastered
6. **Don't overwhelm** - Split long topics into multiple files
7. **Runnable examples** - Every code example should be runnable
8. **Use the student's language** - All content in `learning_language`
9. **Update as you go** - Add to common-mistakes.md and faq.md when students ask questions
