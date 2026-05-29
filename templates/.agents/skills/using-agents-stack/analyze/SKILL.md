---
name: analyze
description: Pre-implementation alignment gate. Checks spec / plan / tasks consistency and plan vs codebase reality before code is written.
trigger: When tasks.md exists and analyze has not passed for this workstream. Also triggered on L2/L3 reroute from implement or qa.
inputs: [spec.md, plan.md, tasks.md, codebase files referenced by plan.md]
outputs: [.agents-stack/workstream/<ws-id>_{YYYYMMDD}/report.md, .agents-stack/workstream/<ws-id>_{YYYYMMDD}/status.json]
boundaries: Read-only. No code changes. No design changes. No task modifications.
---

# Analyze Worker

You are the pre-implementation alignment gate. Before any code is written, verify that the spec, plan, and tasks are consistent with each other — and that the plan still matches the real codebase.

## Entry Gate

```
tasks.md exists
    ↓
Check .agents-stack/<id>/status.json for analyze phase_gate
    ↓
If analyze already passed for this workstream → skip
If reroute from implement (L2/L3) → re-run analyze
If fresh → run
```

## Workflow

Run all 8 checks in order. Each check produces pass/fail + layer assessment.

### Check 1: AC Extraction

Read `spec.md` and extract all BDD acceptance criteria. Build a checklist:

| AC ID | Description | Verifiable? |
|-------|-------------|-------------|
| AC-001 | ... | ✅/❌ |

If any AC is not verifiable (cannot be Given-When-Then'd without reading code), flag as L3 → spec.

### Check 2: AC → Architecture Coverage

Read `plan.md` Architecture Decisions. For each AC, confirm there is at least one architecture decision that satisfies it.

| Gap | Layer | Route to |
|-----|-------|----------|
| AC has no corresponding architecture | L3 | spec |
| Architecture exists but underspecified | L2 | plan |

### Check 3: AC → Task Traceability

Read `tasks.md`. For each AC, confirm at least one task references it via "Align Spec".

| Gap | Layer | Route to |
|-----|-------|----------|
| AC referenced but task underspecified | L2 | plan (add task scope) |
| AC not referenced by any task | L2 | plan (add task) |
| AC not in spec (task references phantom AC) | L1 | tasks (fix reference) |

### Check 4: Deliverables → Real Files

Read each task's "Deliverables" file paths. Check they exist in the codebase (for MODIFY files) or are plausible paths (for ADD files).

| Gap | Layer | Route to |
|-----|-------|----------|
| MODIFY path doesn't exist on disk | L2 | plan (outdated impact analysis) |
| ADD path conflicts with existing file | L2 | plan (path collision) |

### Check 5: DAG Integrity

Check tasks.md dependency graph:
- Every "Depends On" references a task that exists
- No circular dependencies
- TASK-1 is test infrastructure scaffold

| Gap | Layer | Route to |
|-----|-------|----------|
| Missing dependency target | L1 | tasks |
| Circular dependency | L1 | tasks |
| TASK-1 not scaffold | L1 | tasks |

### Check 6: Plan vs Codebase Reality

Compare `plan.md` Impact Analysis against the current codebase. Since plan was written, the codebase may have changed:
- Files listed as MODIFY still exist?
- Listed downstream modules unchanged?
- No new structural changes that invalidate the plan?

| Gap | Layer | Route to |
|-----|-------|----------|
| File removed since plan | L2 | plan (revise) |
| New dependency introduced since plan | L2 | plan (re-assess impact) |

### Check 7: Report

Write `report.md` to `.agents-stack/workstream/<ws-id>_{YYYYMMDD}/report.md`:

```markdown
# Analyze Report

**Workstream ID:** `<id>`

## Verdict: [PASS | FAIL]

## Summary
[One-paragraph summary: all clear, or N gaps found across L1/L2/L3]

## Check Results

| # | Check | Status | Layer | Details |
|---|-------|--------|-------|---------|
| 1 | AC Extraction | ✅ | — | N ACs found, all verifiable |
| 2 | AC→Architecture | ❌ | L3 | AC-003 has no architecture decision |
| 3 | AC→Task Traceability | ✅ | — | All ACs traced |
| 4 | Deliverables→Real Files | ❌ | L2 | `src/db/migration.ts` doesn't exist |
| 5 | DAG Integrity | ✅ | — | Valid |
| 6 | Plan vs Codebase | ✅ | — | No drift |

## Gaps Requiring Action

### [L3] AC-003: No architecture in plan
- **Problem:** Spec defines AC-003 (user can reset password) but plan has no auth/ reset architecture
- **Route to:** spec or plan

### [L2] Phantom file: `src/db/migration.ts`
- **Problem:** Plan lists this file for MODIFY but it doesn't exist on disk
- **Route to:** plan

## Final Routing
Route to: [implement | tasks | plan | spec]
```

### Check 8: Status Update

Update `status.json`:
- Set `phase: "analyze"`
- Set `phase_gates.analyze.passed` to `true` / `false`
- If FAIL, set `blocking_gate` with gap details and `blocked_reason`

## Gate

**HARD STOP.** If analyze returns FAIL, you CANNOT route to implement. Route to the correct layer and only proceed to implement when analyze passes.

| Minor (1 L1 gap) | Major (2+ L1 or any L2/L3) |
|------------------|---------------------------|
| Can route to L1 (tasks) then directly to implement without re-running full analyze | Must route to L2/L3, fix, regenerate downstream artifacts, then re-run full analyze |

## Done

`report.md` exists with PASS/FAIL verdict. If PASS: `status.json.phase_gates.analyze.passed` = true. If FAIL: blocking_gate set, correct route identified.

**PASS → Next: implement**　|　**FAIL → Rollback to L1: tasks / L2: plan / L3: spec**
