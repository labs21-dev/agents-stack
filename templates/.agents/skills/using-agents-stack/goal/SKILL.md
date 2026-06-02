---
name: goal
description: Define the goal: what problem we solve, for whom, and what success looks like. The directional anchor that architecture and specs must serve.
trigger: When no goal.md exists for the active workstream.
inputs:
  - CONSTITUTION.md
  - .agents-stack/tracked-work.json
outputs:
  - .agents-stack/workstream/<ws-id>_{YYYYMMDD}/goal.md
  - .agents-stack/workstream/<ws-id>_{YYYYMMDD}/status.json
boundaries: Direction only. No requirements. No architecture. No implementation details. Just the problem, who it matters to, and what winning looks like.
---

# Goal Worker

Define the goal. This is the directional anchor — everything downstream exists to serve this. Architecture decisions are validated against this. Specs derive from this.

You define *why* we're building — not what, not how.

## Output Template: goal.md

```markdown
# Goal: [Brief Title]

**Workstream ID:** `<id>`

## Problem

[What problem does this solve? One paragraph. Be specific — name the pain, the gap, the friction. Not "users need X" but "users currently do Y which takes Z minutes and fails W% of the time."]

## Who Is This For?

[Who experiences this problem? Be specific — persona, role, context. Not "users" but "new developers onboarding to the platform."]

## Success Criteria

What does winning look like? Observable, measurable outcomes — not features.

| # | Success Criterion | How We Know |
|---|------------------|-------------|
| SC-01 | [measurable outcome] | [observable signal] |
| SC-02 | [measurable outcome] | [observable signal] |

## Non-Goals

What are we explicitly NOT trying to achieve? Precision prevents scope creep and over-engineering.

- [Non-goal 1]
- [Non-goal 2]
- Reason for exclusion: [why this matters now]

## Constraints

What limits our design space? Budget, time, technical, organizational.

| Constraint | Impact |
|-----------|--------|
| [e.g., Must work with existing auth system] | Architecture must use current session middleware |
| [e.g., 2-week timeline] | Scope must fit within sprint boundary |
```

## Workflow

1. Read `CONSTITUTION.md` for governing rules
2. Read `.agents-stack/tracked-work.json` for active workstream ID
3. From human intent, extract: the problem, who it's for, what success looks like
4. Define non-goals explicitly — what are we NOT building, and why
5. Identify constraints that limit design space
6. Write `goal.md` to `.agents-stack/workstream/<ws-id>_{YYYYMMDD}/goal.md`
7. Update `status.json`: set `phase: "goal"`

## Quality Bar

- Problem is concrete and specific — names pain with evidence
- Success criteria are observable, not "system is fast" but "page loads in <2s"
- Non-goals are explicit with reasons — not "we might do this later"
- Constraints are real limits, not preferences
- If the goal cannot be written without mentioning a technology, file, or architecture — it's not a goal, it's a plan. Push back.

## Done

`goal.md` exists with problem, audience, success criteria, non-goals, and constraints. `status.json` reflects goal phase.

**PASS → Next: spec**
