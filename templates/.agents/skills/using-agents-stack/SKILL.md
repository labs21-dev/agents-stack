---
name: using-agents-stack
description: Root orchestrator. Reads durable state, routes to one phase, dispatches fresh workers.
---

# Orchestrator — Goal-QA-Driven v3

Read durable state from `.agents-stack/`, decide the next phase based on linear progression, dispatch a fresh worker.

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

## State Machine Mode

Check `status.json.state_machine` on every message:

| Value | Behavior |
|-------|----------|
| `"on"` | Linear pipeline enforced. Route by phase order only. |
| `"off"` | No pipeline interference. Do NOT route, do NOT enforce. Execute ad-hoc. |
| missing / undefined | Treat as `"on"` (default when workstream is active) |

User can toggle at any time: `/state-machine on|off` or natural language "turn off state machine" / "stop using pipeline" / "disable pipeline enforcement".

When toggling OFF → set `status.json.state_machine = "off"`. When toggling ON → set `status.json.state_machine = "on"`.

## Pipeline

```
goal → spec → plan → [CHECK #1: verify-architecture] → tasks → [CHECK #2: analyze] → implement → [CHECK #3: qa] → release
```

This orchestrator activates when `state_machine: "on"` AND a workstream is active in `tracked-work.json`.

## Routing (State Machine ON)

**Single logic — no intent detection, no contextual triggers, no artifact-driven routing:**

1. Read `status.json.current_phase`
2. Read the phase's completion signal (see `references/state-machine.md` Phase Table)
3. **Completion signal met?**
   - YES → Advance `current_phase` to next phase in the table. Update `status.json`. Dispatch the next phase.
   - NO → Re-dispatch `current_phase`. The phase is not done.
4. If `current_phase` is the last phase (release) AND completion signal met → archive. Set `current_phase: null`.
5. If `status.json.blocking_gate` is set → STOP. Do not advance. Report to user.

**Phase completion signals (from state-machine.md):**

| Phase | Check |
|-------|-------|
| goal | `goal.md` exists with Problem + SCs + Non-Goals |
| spec | `spec.md` exists with BDD ACs + edge cases |
| plan | `plan.md` exists with Architecture Trace table (non-empty) |
| verify-architecture | `arch-report.md` exists AND verdict = PASS |
| tasks | `tasks.md` exists with 5-dimension verification metadata |
| analyze | `report.md` exists AND verdict = PASS |
| implement | `handoff.md` exists, all tasks `[✅] done`, review approved |
| qa | `qa-report.md` exists AND verdict = PASS |
| release | `changelog.md` exists, workstream archived |

## Blocking Gates

| When | Gate |
|------|------|
| Phase produces FAIL verdict | `status.json.blocking_gate` set — do not advance |
| Any checkpoint FAIL | Route back to the failed layer (L1→implement, L2→plan, L3→spec) |

## Dispatch Essentials

- Provide worker with: child SKILL.md path, workstream ID, artifact paths
- **Generator ≠ Auditor**: All three checkpoint phases (verify-architecture, analyze, qa) must use different worker instances from the phases they verify. The agent that designs must not verify. Verify before dispatching.
- Context reuse: generator phases (spec→plan→tasks→implement) may reuse; verify-architecture, analyze, and qa always separate workers; release may reuse (post-verification)

## Routing Output Examples

- `Route to goal. Current phase: goal.`
- `Route to analyze. Current phase: analyze.`
- `Phase analyze complete. Advancing to implement.`
- `Blocked. Phase analyze returned FAIL. See report.md. Route back to plan.`
- `State machine is OFF. Executing ad-hoc.`
- `Awaiting human input.` · `Escalated to human.`
