# Scoping — what's already scannable?

The first step is never "what docs should we write?" It's "what does the agent
already know for free?" Only the remainder needs docs.

## What counts as scannable (do NOT document)

| Source | Gives the agent, for free |
|---|---|
| `package.json` / `Cargo.toml` / `pyproject.toml` | language, framework, scripts, deps |
| Type signatures | function shape, inputs/outputs, optionality |
| Tests | intended behavior, edge cases the author cared about |
| `git log` | what changed, when, by whom |
| CI config | how the project is built/tested/deployed |
| Directory structure | module layout, entry points |
| Code comments | local "why this line" |

If a fact lives in any of the above, **a doc repeating it is a second source of
truth that will rot.** Delete or convert to a pointer.

## What is NOT scannable (these DO need docs)

- **Hidden conventions** — rules the team follows that no lint/type enforces
  (e.g. "never add a new top-level export without updating the barrel index
  test" — *if* no test enforces it).
- **Why a decision was made / what was rejected** — code shows the chosen path,
  not the alternatives. → ADR.
- **Where we are mid-task** — code is a snapshot; "tried X, failed, next is Y"
  isn't in it. → plan/handoff.
- **Trust boundaries** — code shows *that* a check exists, not *why the boundary
  is drawn here* or *what's trusted*. → SECURITY.md.
- **Non-negotiable principles** — code shows current shape, not "this is
  deliberately unchanging." → CONSTITUTION.md.

## Procedure

1. List the repo's scannable sources (read manifest, types, CI, dir tree).
2. For each candidate doc fact, ask: *scannable?* → if yes, drop it.
3. Survivors are gaps → map to a class in `doc-classes.md`.
4. If a gap has no class → it doesn't need a doc. Close it with a comment, a
   test, a lint rule, or a type. A test is worth a thousand docs.

## Negative-space record

Write down what you considered and **rejected** (with reason) as part of the
output. This is not ceremony — it prevents the set from silently re-bloating
next time, and lets a reviewer see the doc budget was a deliberate minimum, not
an oversight.