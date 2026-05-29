---
name: spec
description: Define what we build: goal, user stories, edge cases, BDD acceptance criteria.
trigger: When no spec.md exists for the active workstream.
inputs: [CONSTITUTION.md, .agents-stack/tracked-work.json, relevant reference docs]
outputs: [.agents-stack/<id>/spec.md, .agents-stack/<id>/status.json]
boundaries: Requirements definition only. No code. No architecture design.
---

# Spec Worker

Translate vague intent into a precise, verifiable specification. You define *what* we build — not how, not with what technology, not with what file structure.

## Output Template: spec.md

```markdown
# Spec: [Brief Title]

**Workstream ID:** `<id>`

## Core Goal

### Problem
[What problem does this solve? Why does it matter?]

### Solution Intent
[High-level approach — 2-3 sentences max]

## User Stories

### US-001: [Title]
**As a** [who]
**I want** [what action/scenario]
**So that** [why — value delivered]

### US-002: ...
...

## Edge Cases

Edge cases are pre-identified here — not deferred to QA or implementation. Name them now.

### EC-001: [Name]
- **Scenario:** [What happens at the boundary]
- **Expected behavior:** [How the system must respond]

### EC-002: [Name]
- **Scenario:** [Failure mode / extreme input / concurrency condition]
- **Expected behavior:** [How the system must respond]

### Error Output Contract Rule
For every component that produces output consumed by a downstream phase or task,
you MUST define error output explicitly. Each error state must name its consumer.

### EC-00X: [Component] returns error state [State]
- **Error output format:** [exact type/fields — e.g. `TaskResult(status="blocked", reason="empty_output")`]
- **Consumed by:** [downstream phase/task — e.g. P10 Session Lifecycle → `end_session(reason)`]

...

## BDD Acceptance Criteria

Every AC must be verifiable without reading source code. Use Given-When-Then format.

### AC-001: [Title — maps to US-001 if possible]
**Given** [precondition / starting state]
**When** [action / trigger]
**Then** [observable outcome]

### AC-002: ...
...

### Failure-Path Coverage Rule
For every happy-path AC describing a successful outcome, you MUST define at least one
failure-path AC describing what happens when the precondition fails, the action fails,
or the system is in an unexpected state. A happy-path AC without a corresponding
failure-path AC is incomplete.

## Out of Scope

- [Explicitly excluded: feature X]
- [Explicitly excluded: non-goal Y]
- [Reason for exclusion]
- Any known workaround or stub implementation must be called out here:
  - [Stub/workaround: what was simplified, under what condition it breaks]
```

## Workflow

1. Read `CONSTITUTION.md` for governing rules and constraints
2. Read `.agents-stack/tracked-work.json` for the active workstream ID
3. Form spec from human intent — what is the core problem and solution?
4. Identify edge cases explicitly: stress every boundary, empty state, error path, concurrency scenario
5. Write `spec.md` to `.agents-stack/<id>/spec.md`
6. Update `status.json`: set `phase: "spec"`

## Quality Bar

- Every AC is externally verifiable — a tester confirms it without reading code
- Edge cases are named and resolved, not deferred to "handle errors gracefully"
- Error output format is defined for every component that can fail
- At least one failure-path AC exists for every critical user flow
- Out of Scope is explicit — precision prevents scope creep
- User stories are who-what-why, not implementation notes

## Done

`spec.md` exists with verifiable BDD acceptance criteria, pre-identified edge cases, and clear out-of-scope declarations. `status.json` reflects spec phase.

**PASS → Next: plan**
