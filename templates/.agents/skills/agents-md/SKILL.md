---
name: agents-md
description: Create, update, and maintain AGENTS.md files following OpenAI best practices for agent instruction files. Standalone skill — not part of any pipeline.
trigger: When the user asks to create, update, or maintain AGENTS.md. Also triggered when pipeline phases are added/removed/renamed and AGENTS.md needs to reflect the change.
inputs:
  - AGENTS.md (current)
  - CONSTITUTION.md
  - .agents-stack/reference/architecture.md
  - .agents/skills/using-agents-stack/ (SKILL.md directory listing)
outputs:
  - AGENTS.md (updated)
boundaries: Read-only except AGENTS.md. Does not modify SKILL.md files, reference docs, or pipeline artifacts. Reports to the orchestrator but operates independently.
---

# Agents.md

Create, update, and maintain AGENTS.md — the project-level agent instruction file that serves as the cold-start resume anchor and intent router. This is a standalone skill; it is NOT a pipeline phase and does not belong to `using-agents-stack`.

Follow OpenAI best practices for structure, ordering, and content selection.

## OpenAI Best Practices

These principles govern ALL AGENTS.md edits:

1. **Static content first, dynamic content last** — maximize prompt cache hits. Invariants and paths at the top; intent routing at the bottom.
2. **Every-task rules only** — anything that applies to all tasks belongs here. Single-task context does NOT.
3. **No duplication of SKILL.md** — reference phase locations, do not copy phase contracts.
4. **Pipeline details → architecture.md** — AGENTS.md shows the diagram and points to the full docs.
5. **Concise and operational** — rules, not background essays.

## AGENTS.md Structure

The file must follow this order (per OpenAI's 8-point template, adapted for agents-stack):

| Section | Required | Content |
|---------|----------|---------|
| **Project purpose** | ✅ | One sentence: what this repo is and does |
| **Key Paths** | ✅ | Where to find workstream artifacts, registry, reference docs, skills |
| **Core Invariants** | ✅ | 6 non-negotiable rules (files beat memory, one workstream, Generator ≠ Auditor, cold start, iteration ≠ retry, three-checkpoint rhythm) |
| **Safety / Do Not Do** | ✅ | Operational guardrails (blocking gates, self-review, reference/, spec-first, plan-first, orchestrator role) |
| **Quick Resume** | ✅ | Cold-start protocol: which files to read in what order |
| **Pipeline** | ✅ | Pipeline diagram with checkpoints, "load SKILL.md before executing" rule, pointer to architecture.md for full docs |
| **Commit & PR** | ✅ | Conventional commit style, pre-commit checks, pre-PR checks |
| **Intent Routing** | ✅ | Pipeline work → using-agents-stack, ad-hoc → direct execution, skill-specific → platform resolver |

Sections 3-5 (coding conventions, test commands, tooling rules) from the OpenAI template are N/A for agents-stack (methodology project, not application code).

## What Goes In vs What Stays Out

### ✅ Goes IN AGENTS.md (stable, every-task rules)

| Category | Examples |
|----------|----------|
| File paths | Where artifacts live, where skills live |
| Non-negotiable rules | Invariants, safety rules |
| Cold-start protocol | Resume steps |
| Pipeline overview | Diagram + "load SKILL.md" rule |
| Commit conventions | Type format, pre-commit checks |
| Intent routing | Pipeline vs ad-hoc |

### ❌ Stays OUT (dynamic, single-task, or lives elsewhere)

| Category | Where it lives instead |
|----------|----------------------|
| Phase contracts (inputs, outputs, workflow) | Each phase's SKILL.md |
| Full state machine rules | `references/state-machine.md` |
| Detailed checkpoint mechanics | `reference/architecture.md` |
| Current workstream ID | `.agents-stack/tracked-work.json` |
| Current phase/attempt/layer | `.agents-stack/<id>/status.json` |
| Specific skill intent triggers | Platform's AGENTS.md (contextual skill resolver) |

## Workflow

### When Creating a New AGENTS.md

1. Read `CONSTITUTION.md` — extract all invariants, safety rules, and workflow rules
2. Read `.agents-stack/reference/architecture.md` — extract pipeline diagram, checkpoint system summary
3. List `.agents/skills/using-agents-stack/` — confirm which phases and utility skills exist
4. Write AGENTS.md following the structure table above
5. Verify: every section in the structure table is present, no SKILL.md content is duplicated, static sections precede dynamic sections

### When Updating an Existing AGENTS.md

1. Read current `AGENTS.md`
2. Identify what changed (new phase? renamed phase? new invariant? new safety rule?)
3. Read `CONSTITUTION.md` and `architecture.md` to confirm the change is reflected there first
4. Apply the minimal edit — change only what's needed, preserve static ordering
5. If a phase was added/removed: update the pipeline diagram, update artifact list in Key Paths, do NOT add a phase row to a table (that's what architecture.md is for)
6. If an invariant changed: update the Core Invariants section, keep numbering stable
7. Verify: no duplication introduced, static sections still precede dynamic sections, OpenAI principles still hold

### Common Update Scenarios

| Trigger | What to Update in AGENTS.md |
|---------|---------------------------|
| New pipeline phase added | Pipeline diagram, Key Paths artifact list |
| Phase renamed | Pipeline diagram, Key Paths artifact list |
| New invariant added | Core Invariants (append, keep numbering) |
| New safety rule | Safety / Do Not Do (append) |
| New utility skill | No change — utility skills are not pipeline phases and don't appear in the diagram |
| Commit convention change | Commit & PR section |
| Pipeline restructuring | Pipeline diagram + Key Paths; defer full docs to architecture.md |

## Verification

Before declaring done, verify:

1. **Structure check:** All 8 required sections present (purpose, paths, invariants, safety, resume, pipeline, commit, routing)
2. **Static-first check:** Invariants and safety rules appear before Pipeline; Intent Routing is the last section
3. **No duplication check:** No phase-specific input/output/workflow details that duplicate SKILL.md frontmatter
4. **Pipeline accuracy check:** Diagram matches the phases listed in `.agents/skills/using-agents-stack/` (excluding utility skills: prune-review, reflect, agents-md)
5. **Consistency check:** Invariants match CONSTITUTION.md; pipeline matches architecture.md
6. **Cold-start check:** A reader of AGENTS.md alone can find every key file path needed to resume a workstream

## Done

AGENTS.md exists and passes all 6 verification checks. Cold-start agent can resume from files alone.
