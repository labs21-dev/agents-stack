# Skill Anatomy

A skill is a directory with a recognized structure. The structure is runtime-agnostic — it describes *what* a skill is, not how any particular runtime discovers or injects it.

## Directory layout

```
<skill-name>/
  SKILL.md            ← entry point; frontmatter + body
  references/         ← heavy detail, loaded on demand (progressive disclosure)
    *.md
  templates/          ← copyable artifacts the skill produces for users
    *
  evals/              ← optional, for L1 evaluation
    evals.json
    files/            ← input files referenced by evals
```

## SKILL.md

### Frontmatter (YAML)

```yaml
---
name: <kebab-case-slug>
description: <what it does + specific contexts when to use it>
---
```

- `name` — slug, matches the directory name.
- `description` — the **primary triggering mechanism**. Must contain both *what the skill does* and *concrete contexts when to use it*. All "when to use" guidance goes here, not in the body. LLMs generally undertrigger skills, so be a little pushy — name concrete trigger phrases and situations, including ones the user might not explicitly voice.

### Body

The body is what the agent reads when it consults the skill. Keep it lean — put heavy detail in `references/` and point to it, rather than inlining everything. A reader should understand the skill's purpose and flow from the body alone, and follow references only when they need the detail.

## Progressive disclosure

The agent reads `SKILL.md` first. `references/` files are read only when the body points to them and the agent needs that detail. This keeps the entry point cheap and lets complex skills scale without bloating every session.

Guidelines:
- One topic per reference file.
- Reference files are linked from the body at the point they're needed.
- `templates/` holds copyable artifacts (scaffolds, schemas, sample files) the skill hands to the user.

## What a skill is not

- Not an agent — it has no territory, no tools of its own, no running loop.
- Not always-on — it's consulted when the description matches a need. (Always-on disciplines belong in a constitution/module layer, not in `skills/`.)
- Not a library — it's instructions + references the agent reads, not code it imports.

## Skill quality signals (L1)

A good skill:
- Has a description that reliably triggers on real needs and not on lookalikes.
- Has a body lean enough to read cheaply, with detail progressively disclosed.
- Produces outputs that satisfy its stated expectations when triggered.
- Earns its attention budget — the need it serves recurs often enough to justify mounting it every session.