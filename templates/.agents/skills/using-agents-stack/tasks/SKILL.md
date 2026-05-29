---
name: tasks
description: Break plan into minimal verifiable tasks with 5-dimension verification metadata.
trigger: When plan.md exists and tasks.md does not.
inputs: [spec.md, plan.md]
outputs: [.agents-stack/<id>/tasks.md, .agents-stack/<id>/status.json]
boundaries: Task breakdown only. No implementation. No design changes.
---

# Tasks Worker

Decompose the plan into a strictly ordered sequence of verifiable tasks. Each task is a self-contained unit with embedded 5-dimension verification. This document is the execution script for the implement phase.

## Output Template: tasks.md

```markdown
# Tasks: [Brief Title]

**Workstream ID:** `<id>`
**Plan Referenced:** [date or version]
**Total Tasks:** `<N>`
**Execution Order:** DAG-based — tasks with no mutual dependencies may execute in parallel. Groups execute sequentially.

---

## TASK-1: Scaffold Test Infrastructure

**Depends On:** None
**Parallel Group:** Group A
**Shared Resources:** None (scaffold only)

### 1. Align Spec
- SPEC.md — overall quality bar: all ACs must be testable

### 2. Coverage Checklist
- [ ] Test framework configured and running
- [ ] Test database/seeding utilities in place
- [ ] CI-compatible test runner command exists (e.g., `npm test`)
- [ ] Fixture/mock helpers scaffolded for core entities

### 3. Deliverables
- Test configuration files — ensure test runner passes (even with no tests)
- Test utility helpers — factories, seeders, cleanup routines

### 4. Verification Checkpoints
- [ ] `npm test` runs and exits 0 (no tests is fine, no errors)
- [ ] Test DB can be created, migrated, seeded, and torn down
- [ ] Coverage tool configured and reporting

### 5. Definition of Done
- Coverage ≥ 80%, all checkpoints green
- Test infrastructure ready for RED-GREEN-REFACTOR workflow

---

## TASK-N: [Task Name]

**Depends On:** TASK-01, TASK-03 (or None if independent)
**Parallel Group:** Group B (or same group if parallel with other tasks)
**Shared Resources:** `src/schema.ts`, `prisma/schema.prisma` (or None if no overlap)

### 1. Align Spec
- SPEC.md §X — [specific requirement reference]
- AC-00X — [acceptance criterion this task satisfies]

### 2. Coverage Checklist
- [ ] [Test scenario that must be covered]
- [ ] [Test scenario that must be covered]

### 3. Deliverables
- `path/to/file.ts` — [what this file adds/changes]
- `path/to/test.ts` — [corresponding test file]

### 4. Verification Checkpoints
- [ ] [Runnable command — `npm test`, `curl localhost:PORT/path`, `python -c "..."`. Must produce observable pass/fail output. "Looks correct" is not a checkpoint.]
- [ ] [Runnable command — same rule]

### 5. Definition of Done
- Coverage ≥ 80% for files in this task
- All checkpoints green
- Task-N tests pass alongside all prior task tests (no regressions)
```

## Workflow

1. Read `spec.md` — understand user stories, edge cases, and acceptance criteria
2. Read `plan.md` — understand architecture, files to touch, and test strategy
3. Break the plan into tasks and organize them into a DAG: identify dependencies, group independent tasks into parallel groups
4. Verify DAG dependencies — each task lists its real predecessors. Tasks with no mutual dependencies are grouped for parallel execution. Groups execute sequentially.
5. For every task, complete all five dimensions of verification:
   - **1. Align Spec** — trace to specific ACs and spec sections
   - **2. Coverage Checklist** — what test scenarios are required
   - **3. Deliverables** — exact file paths from plan.md impact analysis
   - **4. Verification Checkpoints** — observable pass/fail commands
   - **5. Definition of Done** — coverage threshold ≥ 80%, all checkpoints green
6. **Run cross-artifact self-consistency check** (see Quality Bar below) — verify that your own output is internally consistent and traceable to spec+plan
7. If consistency check fails: fix gaps before writing tasks.md
8. Write `tasks.md` to `.agents-stack/<id>/tasks.md`
9. Update `status.json`: set `phase: "tasks"`

## Quality Bar

- Tasks follow a DAG — independent tasks share a Parallel Group; groups execute sequentially
- Each task is small enough to complete in one AI session (time-box: ~1 AI session)
- TASK-1 is always scaffold test infrastructure
- Every task has all five verification dimensions filled in
- Verification Checkpoints (dimension 4) are all **runnable commands** — no descriptive statements, no "looks correct", no unverifiable conditions
- Coverage checklist maps to test strategy from plan.md
- If a task cannot be made verifiable, the plan is insufficient — flag it

### Edge Case Coverage Rule
For every task that implements a function producing an error state, the Coverage Checklist MUST include at least one test scenario where:
- The function receives invalid or empty input
- The function's dependency fails
- The function's output is consumed by a downstream task in error state

A Coverage Checklist without edge case scenarios is incomplete.

### Cross-Artifact Self-Consistency Check

Before declaring done, verify your own output against spec.md and plan.md:

| Check | How to verify |
|-------|---------------|
| AC coverage | Every AC in spec.md has at least one task with a matching "Align Spec" reference |
| Task-to-AC traceability | Every "Align Spec" reference in every task points to a real AC or spec section |
| Deliverables-traceable | Every file in Deliverables appears in plan.md's Impact Analysis — no phantom files |
| No dead dependencies | Every "Depends On" task actually exists in the task list |
| DAG is acyclic | Trace each dependency chain to its root — no loops |
| First task invariant | TASK-1 is test infrastructure scaffold (not implementation) |
| No orphaned ACs | Every AC is covered by at least one task |
| Error output coverage | Every EC error output format in spec.md has at least one downstream task referencing it in "Align Spec" |
| Failure-path AC coverage | Every failure-path AC in spec.md maps to at least one task |

Run this check **before** writing tasks.md. If you find gaps, fix them by adding/updating tasks. Do not pass inconsistent tasks to implement.

## Done

`tasks.md` exists with strictly sequential tasks, each having complete 5-dimension verification metadata. Cross-artifact consistency check passed. First task is scaffold test infrastructure. `status.json` reflects tasks phase.

**PASS → Next: analyze**　|　**FAIL → Rollback to tasks**
