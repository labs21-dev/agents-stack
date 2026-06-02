---
name: agents-md
description: Extract implicit knowledge and audit AGENTS.md against four principles. Derives sections from domain, not from a fixed template.
trigger: When the user asks to create, review, or optimize an AGENTS.md file.
inputs:
  - AGENTS.md (current, if exists)
  - CONSTITUTION.md (if exists)
  - Project codebase / file tree
outputs:
  - AGENTS.md (created or updated)
  - Audit notes (optional — what was flagged and why)
boundaries: Read-only on all files except AGENTS.md. Advises, does not dictate structure. Domain decides format.
---

# Agents.md

Extract what an agent cannot discover from code and write it into AGENTS.md. Audit existing AGENTS.md against four principles. Sections emerge from the project's domain — there is no universal template.

## Four Principles

These govern ALL AGENTS.md decisions. Derived from OpenAI best practices + clean philosophy.

### 1. Implicit Knowledge Only

**Rule:** If an agent can discover it by reading code, running `ls`, or inspecting config files — don't write it.

| Write (implicit) | Don't write (discoverable) |
|-----------------|---------------------------|
| Which directory is the canonical state root (vs archive) | File tree structure (`ls` already shows this) |
| WHY a non-standard tool was chosen (`uv` not `pip`) | That React is used (`package.json` already says this) |
| Pipeline phase ORDER and checkpoint positions | Individual phase contracts (each SKILL.md already defines these) |
| Intent routing logic | Domain skill names (discoverable from skills directory) |
| Commit message convention (`type(scope): description`) | Lint rules (linter already enforces these) |

**Test:** Delete the content. Run the agent on the project. If the agent still does the right thing → the content was discoverable.

### 2. Domain Derives Format

**Rule:** Sections emerge from what the project DOES, not from a template. A design project doesn't need a pipeline section. A research project doesn't need commit conventions.

Common domain archetypes and their natural sections:

| Domain | Natural Sections |
|--------|-----------------|
| **Code project** (app, library, service) | Tech stack, dev commands, invariants, boundaries, commit conventions |
| **Methodology / harness** (agents-stack) | Pipeline, checkpoints, invariants, safety rules, cold-start protocol |
| **Design system** | Component library, tokens, principles, review protocol |
| **Research / knowledge base** | Scope, methodology, sources, output format |
| **AI agent / infra** | Agent architecture, model routing, tool conventions, safety boundaries |

**Start by asking:** "What does an agent working on this project MOST need to know that it can't discover?" The answer IS the section list.

### 3. Length as Smell

**Rule:** ~60 lines is ideal. >150 is a warning. >300 is almost certainly redundant with discoverable content.

Not a hard limit — a diagnostic. When AGENTS.md grows:
- Check: is this content discoverable from code?
- Check: is this content duplicated in another referenced file (SKILL.md, architecture.md, README)?
- Check: would the agent still succeed if this section were removed?

### 4. Compliance Ceiling

**Rule:** AGENTS.md compliance rate is ~70%. Rules that MUST be enforced (security, data integrity) need hooks or tool-level guards, not just AGENTS.md entries.

| AGENTS.md is right for | Hooks/tools are right for |
|------------------------|--------------------------|
| "Prefer `uv` over `pip`" | "NEVER push to main" |
| "Tests must pass before commit" | "NEVER commit secrets" |
| "Load SKILL.md before executing phase" | "NEVER modify reference/ outside release" |

If a rule appears in both the AGENTS.md Safety section AND a tool hook → the AGENTS.md entry is still valuable (it explains WHY), but don't rely on it for enforcement.

## Workflow

### Creating AGENTS.md from Scratch

1. **Read the project** — codebase, config files, directory structure, any CONSTITUTION.md
2. **Ask the domain question:** "What does this project DO?" → classify into an archetype
3. **Extract implicit knowledge:** What would a fresh agent get WRONG if it only read the code?
4. **Derive sections:** From the domain archetype + implicit knowledge gaps, derive 4-6 sections
5. **Write concisely:** Target ~60 lines. Every line must pass the "would the agent discover this?" test
6. **Tag the compliance ceiling:** If any rule needs absolute enforcement, note it for hooks

### Auditing an Existing AGENTS.md

1. **Read AGENTS.md + codebase**
2. **Run the 4-principle audit.** For each section and each line, answer:

| Question | If YES | If NO |
|----------|--------|-------|
| Is this implicit (agent can't discover from code)? | Keep | **Flag for removal** |
| Is this duplicated in another referenced file? | **Flag for removal** | Keep |
| Is this domain-relevant (does this project actually DO this)? | Keep | **Flag for removal** |
| Is this a hard enforcement rule? | **Note: needs hook** | AGENTS.md is sufficient |

3. **Check length:** If >150 lines, flag sections that fail the implicit knowledge test
4. **Check ordering:** Static content (invariants, safety, commands) before dynamic content (routing, phase-specific details)?
5. **Report findings** — not as commands, as observations with rationale

### Optimizing for Prompt Cache

Static content at the top maximizes cache hits. Dynamic content (routing, workstream references) goes at the bottom or in external files.

The ideal order (emerges naturally from the principles, not a template):
1. What this is (1-2 sentences)
2. Commands the agent will run repeatedly (`pnpm dev`, `pytest -v`)
3. Invariants and safety rules (won't change between sessions)
4. Workflow / method (how work flows — moderately stable)
5. Exit / shipping rules (commit style, PR checks)
6. Routing (intent mapping — most likely to change as skills evolve)

## Audit Report Format

When auditing, produce findings in this format:

```markdown
## AGENTS.md Audit

**Project:** [name] | **Domain:** [archetype] | **Lines:** [N]

### Implicit Knowledge Gaps
[What should be in AGENTS.md but isn't — agent would get this wrong]

### Discoverable Content
[What's in AGENTS.md but agent can find from code — candidate for removal]
| Section | Content | Discoverable From | Recommendation |
|---------|---------|------------------|----------------|

### Length Check
[Current lines vs ~60 target. Which sections are the biggest contributors?]

### Compliance Notes
[Which rules need hooks, not just AGENTS.md entries?]
```

## Done

AGENTS.md exists (or audit report delivered). Every line passes the implicit knowledge test. Sections emerge from domain, not template. Static content precedes dynamic. Compliance ceiling noted where relevant.
