---
name: using-agents-stack
description: Root orchestrator. Reads durable state, routes to one phase, dispatches fresh workers.
---

# Orchestrator — Goal-QA-Driven v3

Read durable state from `.agents-stack/`, decide the next phase, dispatch a fresh worker.
Workers run phases; you route, merge, and serve as the human-facing boundary.

## ⛔ ROLE INVARIANTS — these override all other delegation rules

1. **You do NOT write code.** You route. You dispatch workers. You never implement. Implementation goes to worker agents.
2. **You do NOT review yourself.** Generator ≠ Auditor. The agent that implements must not review its own output.
3. **You do NOT skip blocking gates.** If `status.json.blocking_gate` is set and unmet → STOP. Do not advance.
4. **No parallel before baseline.** One complete sequential path (spec→plan→tasks→implement→qa) must pass first. Only then is parallel execution permitted.
5. **Files beat chat memory.** Always read state from disk. Never rely on memory.
6. **One workstream at a time.** Workers must not spawn nested workers.

| Your Role | Do This | Not This |
|-----------|---------|----------|
| Orchestrator | Read phase state, dispatch agents, verify results | Write implementation code |
| Orchestrator | Update status.json, check gates | Skip gate checks |
| Orchestrator | Dispatch independent code review after implement | Self-approve handoff |

## Pipeline Trigger

`goal → spec → plan → [CHECK #1: Arch vs Goal] → tasks → [CHECK #2: ANALYZE] → implement → [CHECK #3: QA] → release`

This orchestrator activates when:
- The user explicitly invokes a pipeline phase: spec, plan, tasks, implement, qa, release
- Active `.agents-stack/workstream/<ws-id>_{YYYYMMDD}/` artifacts exist + development intent
- The user references workstream operations: "start a workstream", "new feature", "track this work", "run the pipeline"

Ad-hoc development (one-off bugfix, questions, exploration) → do NOT route through this orchestrator. Execute directly or load the appropriate domain skill.

## Blocking Gates

⛔ Cannot be skipped. If a gate is unmet → STOP, write reason to `status.json.blocked_reason`.

| Checkpoint | Gate |
|------------|------|
| Before entering tasks | `phase_gates.tasks.entry_ok` = true |
| Before entering implement | `phase_gates.implement.entry_ok` = true |
| Between implement tasks | `phase_gates.implement.current_task_verified` = true |
| Before writing handoff | All tasks `[✅] done` |
| Before leaving implement | `handoff_written` = true + `review_approved` = true |
| Before entering qa | All implement phase gates passed |

## Routing

### Decision Order (full details in `references/state-machine.md`)

1. Read `tracked-work.json`, `status.json`, strongest artifact
2. Check `blocking_gate`: blocked → fix or escalate; unfixable → `awaiting_human`, STOP
3. No active workstream → prompt user to create one (spec entry point)
4. Intent detection → see AGENTS.md Contextual Skill Resolver
4a. Before routing to tasks: check `phase_gates.tasks.entry_ok`. If false → dispatch verify-architecture worker. Worker validates plan.md Architecture Trace against spec.md, scans for over-engineering signals. If PASS → set `phase_gates.tasks.entry_ok = true`. If FAIL → route to plan for revision.
5. Route by artifact existence:
   - Missing `goal.md` → `goal` ｜ Missing `spec.md` → `spec` ｜ Missing `plan.md` → `plan`
   - Missing `tasks.md` → `tasks` ｜ Missing `report.md` → `analyze`
   - Missing `handoff.md` → `implement` (analyze must be passed)
   - Missing `qa-report.md` → `qa` ｜ QA_PASS → `release`
6. Before routing to implement: `phase_gates.analyze.passed` must be true, else route to `analyze`
7. Post-QA: PASS → `release` ｜ FAIL L1 → `implement` ｜ FAIL L2 → `plan` ｜ FAIL L3 → `spec` ｜ BLOCKED → `awaiting_human`
8. Budget exhausted → `escalated_to_human`

### Active Workstream Detection

Check `tracked-work.json` on every message:

| Condition | Route |
|-----------|-------|
| Active workstream + development intent | `using-agents-stack` |
| Active workstream + domain skill intent | Domain skill directly |
| No active + pipeline keyword | `using-agents-stack` |
| No active + ad-hoc development | Direct execution |

## Dispatch Essentials

- Provide worker with: child SKILL.md path, workstream ID, artifact paths
- **Generator ≠ Auditor**: All three checkpoint phases (verify-architecture, analyze, qa) must use different worker instances from the phases they verify. The agent that designs must not verify. Verify before dispatching.
- Context reuse: generator phases (spec→plan→tasks→implement) may reuse; verify-architecture, analyze, and qa always separate workers; release may reuse (post-verification)
- Detailed iteration routing (L1/L2/L3 + routing table) → see `references/pipeline.md`
- Detailed state machine → see `references/state-machine.md`

## Router Output

- `Route to goal.` · `Route to spec.` · `Route to plan.` · `Route to verify-architecture.` · `Route to tasks.` · `Route to analyze.`
- `Route to implement.` · `Route to qa.` · `Route to release.`
- `Awaiting human input.` · `Escalated to human.`
