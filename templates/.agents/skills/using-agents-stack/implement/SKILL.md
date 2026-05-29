---
name: implement
description: RED-GREEN-REFACTOR implementation per task. Each task passes before next. Produces handoff.md with reproducible evidence.
trigger: When tasks.md exists and handoff.md does not, or retry after Layer 1 rework.
inputs: [CONSTITUTION.md, spec.md, plan.md, tasks.md]
outputs: [code within task boundaries, .agents-stack/<id>/handoff.md, .agents-stack/<id>/status.json]
boundaries: Only files in tasks.md deliverables. Must not self-approve. Must record reproducible evidence.
---

# Implement Worker

Implement tasks from TASKS.md one by one using the RED-GREEN-REFACTOR cycle. Each task must pass all its Verification Checkpoints before the next task begins.

## Entry Checks

Before touching ANY code, verify these gates:

1. `tasks.md` exists with defined tasks
2. This workstream is the active one in `tracked-work.json`
3. **Generator ≠ Auditor**: if you previously performed QA for this workstream, STOP
4. **Blocking gate check**: `status.json.phase_gates.implement.entry_ok` must be `true`. If blocked, record reason and hand back to orchestrator.
5. **Test harness readiness**: `npm test -- --collect-only` or equivalent must work
6. **RED before GREEN per task**: before writing implementation code for ANY task, the test file must already exist with a failing test

If any check fails: stop, record in `status.json` with `blocking_gate` and `blocked_reason`, hand back to orchestrator.

## Task Status States

Track task status in TASKS.md with these markers:

- `[ ] pending` — not started
- `[→] in_progress` — actively working
- `[✅] done` — passed all verification checkpoints
- `[↩] reworking` — Layer 1: code fix in progress
- `[⚠️] needs_plan` — Layer 2: architecture/plan must change, STOP
- `[🚨] needs_spec` — Layer 3: requirement/spec must change, STOP

## Dispatch Note
This skill is for the implementation agent. If you are the orchestrator reading this, dispatch a fresh implementation agent instead of self-implementing. Do not write code directly.

## Workflow

Tasks execute ONE AT A TIME, in dependency order. No exceptions.

### Inter-Task Gate (Hard Stop)

**⛔ Before moving from task N to task N+1, ALL of these must be true:**

| Gate | Condition | How to verify |
|------|-----------|---------------|
| RED phase completed | Failing test written first, RED evidence recorded | `cat handoff.md` — task N section shows RED command + failing output |
| Task N tests pass | All tests for task N pass (RED→GREEN→REFACTOR complete) | `npm test` or equivalent |
| No regression | All prior task tests still pass | `npm test` (full suite) |
| 5-dimension verified | Import / unit / type / spec / edge — all checked | per task's Verification Checkpoints |
| handoff evidence | Task N's evidence recorded in handoff.md | handoff.md exists with task N section |
| status.json updated | `phase_gates.implement.current_task_verified` = true | read status.json |

If ANY gate is unmet, you CANNOT start task N+1. Fix the current task first.

### Per-Group Execution

For each Parallel Group in dependency order:

1. Identify all tasks in the current group
2. Execute tasks sequentially within the group (one at a time):
   - Read 5-dimension verification metadata → write failing tests → implement → run checkpoints → gate check
3. Once ALL tasks in the group pass: proceed to the next group

### Per-Task Within Group — RED-GREEN-REFACTOR Cycle

Each task follows exactly this 7-phase cycle. No phase can be skipped or merged.

#### Phase 1 — RED: Write a Failing Test
1. Read the task's 5-dimension verification metadata
2. Write test(s) that match the Verification Checkpoints. **At least one test must cover a negative path** (invalid input → expected error). If the task's Coverage Checklist includes edge cases, at least one RED test must cover an edge case.
3. **Run the test(s) — they MUST fail.** If they pass, the test is invalid.
4. If the test framework reports a runtime error (not a test failure), fix the infrastructure first and repeat from step 2.

#### Phase 2 — GREEN: Write Minimal Implementation
5. Write the minimum production code to make the failing test pass. Do NOT add abstractions, edge cases not covered by tests, or refactoring.
6. **Run the test(s) — they MUST pass.** If they fail, iterate on production code only and repeat.

#### Phase 3 — REFACTOR: Improve Without Changing Behavior
7. Refactor: improve naming, extract duplication, simplify logic.
8. **Run ALL prior task tests + current task tests — they MUST all pass.**
9. If any test breaks, revert the refactoring and retry with smaller steps.

#### Phase 4 — VERIFY: Run All Checkpoints (falsifiable)
10. Run every Verification Checkpoint from the task's metadata.
11. Each checkpoint must produce observable evidence — actual command output, API response, or test result.
12. If a checkpoint cannot produce falsifiable evidence, mark it as invalid and skip.

#### Phase 5 — COMMIT: Lock the State
13. Mark task `[✅] done`.
14. Commit or save state with a message referencing the task ID.

#### Phase 6 — REGRESS: Verify No Regression
15. Run ALL completed task tests from this workstream (not just the current one). All must pass.

#### Phase 7 — GATE: Lock the Inter-Task Gate
16. Update `status.json.phase_gates.implement` — set `current_task` and `current_task_verified` = `true`, clear `blocking_gate`.
17. **Only now may you start the next task.**

#### Failure Handling at Each Phase

| Phase | Failure Mode | Action |
|-------|-------------|--------|
| RED step 3 | Test passes unexpectedly | The test is invalid — rewrite it |
| GREEN step 6 | Production code fails to pass | Iterate on production code only, do NOT modify the test |
| REFACTOR step 8-9 | Refactoring breaks existing tests | Revert refactoring — it was too aggressive |
| VERIFY step 11 | Checkpoint cannot produce evidence | Mark checkpoint as invalid, report to handoff's Known Issues |
| REGRESS step 15-16 | Prior task test fails | A prior task's behavior was broken — fix before continuing |
| Build/startup fails | Project doesn't compile or boot | Set `build_failed`, do NOT write handoff as passed |

Beyond code errors: **Architecture blocker** → `[⚠️] needs_plan`, **Spec gap** → `[🚨] needs_spec`, **Parallel group failure** → `[↩] reworking`. In all cases: stop, update status.json with blocked_reason, hand back to orchestrator.

## Status Derivation Rule (Hard Gate)

No status, success, or result field may be assigned a constant value. Every such field MUST be computed from actual state — derived from errors collected, output parsed, or guard evaluated. The RED test must exercise at least two distinct input paths that produce different status values.

**Violations (auto-reject):** Any field assigned a bare literal regardless of input — `status ← "completed"`, `success ← true`, `return Result(status: "completed")`, or any `*_status`/`*_success` field that never varies across test inputs.

## Output: handoff.md

```markdown
# Handoff

## Summary
[What was built — brief]

## Acceptance Trace

### TASK-01: [name]
- Status: [PASS | FAIL]
- RED: [test command + output showing initial failure]
- GREEN: [test command + output showing pass after implementation]
- REFACTOR: [all prior + current tests pass output]
- REGRESS: [full suite test output]

### TASK-02: [name]
...

## Verification-Before-Completion Evidence

Each claim below is backed by a command executed in this session:

- Build: [exit code 0] — `npm run build` (or equivalent)
- All tests: [N passed, 0 failed] — `npm test`
- System start: [process alive, port listening] — `npm start` + `curl localhost:PORT`
- Core path: [end-to-end flow verified] — specific command + output
- Pre-handoff checklist: all items passed

## Risks & Limitations
- [Warnings, limitations, and unresolved edge cases the QA worker should know — the Known Workarounds table above captures implementation shortcuts separately]

## Deviations from Plan
- [What was done differently than plan.md specified, and why]

## Combinatorial Risks

Tasks were checked for emergent interactions — conditions where two tasks independently correct can trigger a failure when combined.

| Risk ID | Tasks Involved | Hypothesis | Trigger Condition |
|---------|---------------|------------|-------------------|
| CR-001 | T3, T7 | T3 changes schema → T7's query may miss new fields | If T3 lands before T7 adapts |
| CR-002 | T5, T6 | Both write to shared-cache with different key formats → silent overwrite | If cache prefix convention isn't agreed |
- [Add rows per identified risk. If none found, state: "No combinatorial risks identified — tasks operate on disjoint files/resources."]

## Known Workarounds

Any implementation decision made to pass tests without full correctness MUST be recorded here. QA will scan for undeclared workarounds and flag them.

| Workaround ID | What was simplified/stubbed | Breaking condition | Resolution plan |
|---------------|---------------------------|--------------------|-----------------|
| W-001 | [description] | [under what input/scenario it fails] | [TODO reference or follow-up task] |
- [If none, state: "No workarounds — all implementations are complete and correct."]

## Rework Notes (if applicable)
- Prior failure: [what failed]
- What changed: [fix applied]
```

## Verification-Before-Completion

You are about to claim the work is done. Every claim in handoff.md must be backed by a command you actually ran in this session — not "I could run it" but "I ran it and here is the output." Re-run tests if code changed since. Static claims without command output are not evidence. Core path exercise is not optional — verify at least one end-to-end flow. If a checkpoint cannot be executed, record it in Known Issues; do not assume it passes.

### Pre-Handoff Checklist

Before writing handoff.md, complete this checklist. Each item requires an actual command execution:

- [ ] `npm run build` (or equivalent) — exits 0
- [ ] `npm test` (or equivalent) — all tests pass
- [ ] System starts without crash — process stays alive
- [ ] Core feature path exercised — one end-to-end flow verified
- [ ] All task checkpoints re-verified with CURRENT state (not cached results)
- [ ] `decisions.md` updated with any deviations from plan

If any item fails: fix it first, re-run the chain, only then write handoff.

## Pre-Handoff Verification

Before finalizing handoff.md, run these three checks sequentially.

### 1. Wiring Integrity (Call-Graph Scan)

For every function or method in the task's public API, verify at least one production caller outside tests:

```
rg "function_name\(" --glob '!tests/**'
```

| Condition | Action |
|-----------|--------|
| 0 production callers | **BLOCKED** — add wiring task or remove the function |
| 1+ callers | PASS |

### 2. Cross-Task Interaction Check (Combinatorial Risk)

Review all tasks and identify pairs sharing resources (files, functions, config, schema). For each:
- Does one task's output flow into another's input? → **Ordering dependency**
- Do both write to the same location? → **Race condition**
- Does one change a contract the other depends on? → **Contract violation**

Record findings in handoff.md's `## Combinatorial Risks` section. If none found, state explicitly.

### 3. Independent Review

Before finalizing handoff, dispatch a review agent:

- [ ] All tasks marked `[✅] done`
- [ ] All inter-task gates passed
- [ ] Review agent dispatched with full context
- [ ] `review-verdict.md` exists with **PASS** — no P0/P1 gaps
- [ ] `status.json.phase_gates.implement.review_approved` = `true`

**You CANNOT finalize handoff.md without a PASS from review agent.**

## Retry Discipline

Increment `attempt` in `status.json` on each fresh attempt. Restore clean state before re-implementing. If `attempt >= max_attempts`: set `phase: "escalated_to_human"` and stop.

## Done

All tasks marked `[✅] done`. `handoff.md` exists with reproducible evidence. System builds, runs, and core path works.

Before declaring implement phase complete, verify ALL gates:

| Gate | Condition |
|------|-----------|
| All tasks verified | Every task passed RED→GREEN→REFACTOR→VERIFY→REGRESS |
| No blocking gate | `status.json.blocking_gate` is null |
| Handoff written | `handoff.md` exists with reproducible evidence per task |
| Review approved | `status.json.phase_gates.implement.review_approved` = true |
| Phase gate updated | `status.json.phase_gates.implement.handoff_written` = true |

If any gate is unmet, the implement phase is NOT done. Fix the gate before declaring completion.

**PASS → Next: qa**　|　**FAIL → Rollback to L1: re-implement / L2: plan / L3: spec**
