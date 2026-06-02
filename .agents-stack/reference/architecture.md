# Architecture — agents-stack v3

## Overview

agents-stack is an AI-native development harness/methodology (not an npm package).
Design goal: enable AI agents to reliably produce high-quality software in a file-first workflow.

## Core Design

### Phase Pipeline

```
goal → spec → plan → [CHECK #1: Arch vs Goal] → tasks → [CHECK #2: ANALYZE] → implement → [CHECK #3: QA] → release
```

Each phase produces a durable artifact in `.agents-stack/<workstream-id>/`.

### State Root

`.agents-stack/` is the single canonical state root.
No split-brain between `.harness/` and `docs/`.

### Orchestrator-Worker Model

- Orchestrator: reads state, decides phase, dispatches worker
- Worker: executes one phase, produces artifact, returns
- Dispatch by artifact existence — which artifact is missing determines next phase

## Three-Checkpoint Verification System

Every 2 steps, a verification checkpoint isolates risk before it compounds.

### Checkpoint #1: Architecture vs Goal (plan → tasks)

**Question:** Does the architecture serve the goal, or has architecture become its own goal?

**Method:** Plan's Architecture Trace table — every architecture decision must map to a goal success criterion or a spec requirement. Decisions without goal trace are over-engineering.

**Catches:** Over-engineered abstractions, future-proofing without trigger, patterns without problems, layers without distinct responsibility.

**Cost of skipping:** Building tasks for an architecture that doesn't serve the goal. WS-A lesson: architecture grew to 936-line monolith because "reduce file count" became the goal instead of serving the real requirements.

### Checkpoint #2: SPEC × PLAN × TASKS Consistency (tasks → implement)

**Question:** Do spec, plan, and tasks agree with each other — and with the real codebase?

**Method:** 8-check alignment gate (AC extraction, bidirectional architecture coverage, task traceability, DAG integrity, plan vs codebase reality).

**Catches:** Missing ACs, phantom files, circular dependencies, outdated impact analysis, spec ambiguities.

**Cost of skipping:** Implementing the wrong thing. WS-A lesson: "backward compatible" was ambiguous — spec meant strict backward compat, implement built new+old coexistence. One missed question wasted an entire workstream.

### Checkpoint #3: CODE vs REALITY (implement → release)

**Question:** Does the code actually work under real conditions, including adversarial ones?

**Method:** Independent adversarial verification by a different agent (Generator ≠ Auditor). Live system exercise against every acceptance criterion.

**Catches:** Dead imports, permission bypasses, concurrent write corruption, hardcoded status values.

**Cost of skipping:** Bugs discovered in production. WS-A lesson: adversarial QA found 12 P0 issues in 3 hours that would have become emergency hotfixes post-release.

## Risk Isolation Principle

```
Without checkpoints:
  Goal → Arch → SPEC → IMPLEMENT → Release
  Problem found at Release → backtrack 5 steps

With checkpoints:
  Goal → Arch → [CHECK] → SPEC → [CHECK] → IMPLEMENT → [CHECK] → Release
  Problem found at nearest checkpoint → backtrack 1 step
```

| Discovery Stage | Backtrack Distance | Relative Cost |
|----------------|-------------------|---------------|
| Checkpoint #1 finds issue | Revise plan | 1x |
| Checkpoint #2 finds issue | Revise spec/plan/tasks | 2x |
| Checkpoint #3 finds issue | Re-implement | 3x |
| Release finds issue | Re-do everything | 5-8x |

### Adversarial Separation

Implement and QA must be different worker instances.
This enforces the Generator ≠ Auditor invariant.

## Key Files

| Path | Purpose |
|------|---------|
| `CONSTITUTION.md` | Technical charter: invariants, rules |
| `AGENTS.md` | Orchestrator resume anchor |
| `.agents-stack/tracked-work.json` | Workstream registry |
| `.agents-stack/<id>/` | Active workstream artifacts |
| `.agents/skills/using-agents-stack/` | Router + phase skills |
