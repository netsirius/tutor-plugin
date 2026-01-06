---
description: Review code with educational feedback. Use /tutor:review to review the current file, or /tutor:review [path] for a specific file. Provides constructive feedback and improvement suggestions.
allowed-tools: Read, Bash, Grep
---

# Command: Review

The user wants you to review their code and provide educational feedback.

## Important: Language Adaptation

Before presenting any content, read `.tutor/config.json` and check the `learning_language` field. ALL feedback MUST be presented in the student's chosen language.

## Your Task

1. Identify the file to review:
   - If a path is provided: use that
   - If not: find the current exercise in progress
   - Prioritize files in `lessons/*/exercises/`

2. Read `.tutor/config.json` to get the learning language

3. Read the code and analyze:
   - Correctness (does it compile? do tests pass?)
   - Style (is it idiomatic?)
   - Efficiency (are there obvious improvements?)
   - Error handling (is it robust?)

4. For Rust, run:
   ```bash
   cargo check 2>&1
   cargo test 2>&1
   cargo clippy 2>&1  # If available
   ```

5. Provide structured and educational feedback (in the student's language)

## Response Format (English)

```markdown
## 📝 Code Review

### File: `src/main.rs`

---

### ✅ What's Good
1. **Clear structure**: The code is well organized
2. **Descriptive names**: `calculate_total` is clear
3. **Option handling**: Good use of `if let`

---

### 🔧 Compilation Result
✅ Compiles without errors

### 🧪 Tests
- Passed: 4/5
- ❌ `test_empty_input`: The test fails because...
  ```
  expected: Some(0)
  got: None
  ```

---

### 💡 Improvement Suggestions

#### 1. Consider using `match` instead of multiple `if`
**Line 15-20**

Your current code:
```rust
if x == 1 { ... }
else if x == 2 { ... }
else { ... }
```

More idiomatic version:
```rust
match x {
    1 => { ... }
    2 => { ... }
    _ => { ... }
}
```

**Why**: `match` in Rust guarantees exhaustiveness and is clearer.

---

#### 2. The `clone()` can be avoided
**Line 8**

```rust
// Current
let name = user.name.clone();

// Better (if you only need to read)
let name = &user.name;
```

**Why**: `clone()` copies memory. If you're only reading, a reference is more efficient.

---

### 📊 Overall Evaluation

| Aspect | Score |
|--------|-------|
| Correctness | ⭐⭐⭐⭐☆ |
| Style | ⭐⭐⭐☆☆ |
| Efficiency | ⭐⭐⭐⭐☆ |

---

### 🎯 Next Step
Fix the `test_empty_input` test by handling the empty input case,
then review the style suggestions when you have time.
```

## Review Levels

Adapt the depth according to the student's level:

### Beginner
- Focus on: does it work?
- Avoid overwhelming with optimizations
- Celebrate that it compiles and passes tests

### Intermediate
- Add: idiomatic style
- Suggest better patterns
- Introduce concepts like efficient borrowing

### Advanced
- Complexity analysis
- Edge cases
- Concurrency and thread-safety
- Advanced clippy suggestions

## Remember

- **Be constructive**: Always start with the positive
- **Explain the why**: Not just what to change, but why
- **Don't overwhelm**: 3-5 suggestions maximum per review
- **Prioritize**: Most important first
- **Motivate**: The goal is for them to learn, not to feel bad
- **Use the student's learning language for ALL feedback**
