# Python Q&A — Quick Reference

## Q1: How does Python execute code?
3 steps:
1. You write `.py` file
2. Python compiles it to **bytecode** (`.pyc`) — just a syntax check, not execution
3. **PVM** (Python Virtual Machine) runs bytecode **line by line, top to bottom**

Python = interpreted language. Runs one line, then next. If line 5 has error, lines 1-4 still ran.

---

## Q2: Interpreted vs Compiled — what's the difference?
- **Compiled (C, Java):** checks entire code first → refuses to run if any error found
- **Interpreted (Python):** runs line by line → crashes only when it reaches the bad line

---

## Q3: If Python is interpreted, why does it compile to bytecode?
Two stages — don't confuse them:
- **Stage 1 (Compile):** whole file → bytecode. Only checks **syntax** (brackets, indentation). Does NOT run anything.
- **Stage 2 (Execute):** bytecode runs **line by line**. This is where runtime errors (`10/0`) happen.

Python's compile = just grammar check. C's compile = grammar + logic + type check.

---

## Q4: What is `__` (dunder) in Python?
**dunder = Double UNDERscore**

3 types:

| Pattern | Name | Meaning |
|---|---|---|
| `__name__` | Dunder variable | Python's built-in special variable |
| `__init__()` | Dunder method | Python calls this automatically (you don't call it) |
| `_name` | Single underscore | "Internal — please don't touch from outside" (just a hint) |
| `__name` | Double underscore | "Private — Python hides it from outside the class" |

---

## Q5: What is `__init__.py` file (empty)?
- Completely different from `__init__()` method
- It tells Python: **"this folder is a package"**
- Without it: `from folder.module import something` won't work
- Empty is fine — just needs to exist
- Like a nameplate on a door — doesn't need content

---

## Q6: Why does Python use `class` keyword for everything?
Python has **only one keyword** to define any data shape: `class`

Node.js has many: `{}`, `Joi.object()`, `mongoose.Schema()`, `z.object()`, `interface`, `type`
Python has: `class` — that's it.

**Don't look at `class` keyword. Look at what's inside `()`:**

| You see | It's actually | Node.js equivalent |
|---|---|---|
| `class X(BaseModel)` | Validation schema | Joi / Zod schema |
| `class X(BaseSettings)` | Config from .env | dotenv + validation |
| `class X(Base)` | DB model | Mongoose / Sequelize model |
| `class X:` (with methods) | Real OOP class | No direct Express equivalent |

---

## Q7: How to tell "data shape" vs "real OOP class"?
- **Data shape:** only has fields, no methods, inherits from `BaseModel`/`Base`/`BaseSettings`
- **Real OOP class:** has methods that do work (`def query()`, `def process()`), stores state (`self.connection`)

In our RAG project → every `class` is a data shape. Zero real OOP.

---

## Q8: What is `BaseSettings`, `BaseModel`, `Base`?
These are **features from installed packages** — nothing magical:

| What | Package | Install | Node.js equivalent |
|---|---|---|---|
| `BaseSettings` | pydantic-settings | `pip install pydantic-settings` | dotenv + joi combined |
| `BaseModel` | pydantic | `pip install pydantic` | joi or zod |
| `Base` | sqlalchemy | `pip install sqlalchemy` | mongoose or sequelize |

You install package → import its feature → use it. Same as npm.

---

## Q9: Is our RAG project class-based or function-based?
**Function-based (Express-style).** All business logic is plain functions:
- `ingest_document()`, `chunk_text()`, `stream_chat()`, `embed_texts()`, `similarity_search()`
- Routes use `@router.get()` / `@router.post()` — same as Express

The `class` keyword only appears for data shapes (schemas, models, config) — not for OOP.

---

## Q10: Can we write Python without classes, like Express?
**Yes.** Python supports both patterns:
- Functions only = works fine (Express-style)
- Classes = useful when you have **state** (data that lives and changes over time)

Use functions for: simple logic, stateless work, utilities
Use classes for: when you keep passing the same data to every function — that's the signal
