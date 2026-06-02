# agents-stack v3 state machine

Goal-QA-Driven phase model. Orchestrator reads these rules, decides next phase, dispatches worker.

## Core Invariants

1. Files are state. Chat memory is not durable.
2. Exactly one workstream active at a time. Others must be parked.
3. Implementer ≠ Verifier (Generator ≠ Auditor). Implement and QA must be separate workers.
4. Cold start must work. A new agent recovers from files alone.
5. Iteration ≠ Retry. Retry fixes execution within same contract. Iteration changes spec/plan.

## State Machine Mode

Pipeline enforcement is binary. There is no fuzzy intent detection, no contextual override, no ad-hoc bypass.

| Mode | Behavior |
|------|----------|
| `state_machine: "on"` | Pipeline strictly enforced. The orchestrator advances phases linearly — one step at a time. The agent cannot skip, reorder, or bypass phases. User must explicitly say "turn off state machine" to exit. |
| `state_machine: "off"` | No pipeline enforcement. Agent executes freely. No orchestrator routing. |

**Default:** `"on"` when a workstream is active. User can toggle via `/state-machine on|off` or plain language "turn off state machine" / "stop using pipeline".

When `state_machine: "on"`, every user request is intercepted: the orchestrator checks the current phase, and if it's not yet complete, routes there. The user's intent does not override the pipeline — the pipeline is the intent.

```
User: "implement the login feature"
Orchestrator: "State machine is ON. Current phase: analyze.
              Complete analyze first. Do you want to proceed with analyze?"
```

## Artifact Precedence

When files disagree, higher-precedence artifact wins:

1. qa-report.md
2. handoff.md
3. tasks.md
4. plan.md
5. spec.md
6. goal.md
7. status.json
8. .agents-stack/tracked-work.json

## Phase Table

Phases execute in strict linear order. Each has a completion signal — an artifact existence check + optional verdict. No phase can be entered before all prior phases are complete.

| # | Phase | Completion Signal |
|---|-------|-------------------|
| 1 | goal | `goal.md` exists with Problem + Success Criteria + Non-Goals |
| 2 | spec | `spec.md` exists with BDD ACs + edge cases |
| 3 | plan | `plan.md` exists with Architecture Trace (every decision traces to goal/spec) |
| 4 | verify-architecture | `arch-report.md` exists with verdict PASS |
| 5 | tasks | `tasks.md` exists with 5-dimension verification metadata |
| 6 | analyze | `report.md` exists with verdict PASS |
| 7 | implement | `handoff.md` exists, all tasks `[✅] done`, review approved |
| 8 | qa | `qa-report.md` exists with verdict PASS |
| 9 | release | `changelog.md` exists, workstream archived |

**Checkpoint positions:** verify-architecture = Checkpoint #1 (before tasks). analyze = Checkpoint #2 (before implement). qa = Checkpoint #3 (before release). Every ~2 phases a verification gate isolates risk.

## Transition Rules

When `state_machine: "on"`:

0. **No active workstream?** → Create workstream. Set `current_phase: "goal"`. Dispatch goal.
1. Read `status.json.current_phase`
2. Check: is the current phase's completion signal met?
   - **YES** → Advance `current_phase` to the next phase. Dispatch that phase.
   - **NO** → Re-dispatch the current phase (it's not done).
3. If all phases complete (after release) → `current_phase: null`, archive workstream.

If a phase produces a FAIL verdict (arch-report.md, report.md, qa-report.md):
- `status.json.blocking_gate` is set
- Phase does NOT advance
- Orchestrator stays on current phase until user resolves (re-run or route back to earlier phase)

This is the ONLY routing logic. There is no artifact-driven routing, no intent detection, no contextual triggers. The phase table IS the routing table.

## Three-Layer Rework

| Layer | Scope | Affected Phase | Cost |
|-------|-------|---------------|------|
| L1: Code | Implementation error, missed edge case | implement | Low |
| L2: Architecture | API/DB design insufficient | plan | Medium |
| L3: Spec | Requirement/AC missing or wrong | spec | High |

When rework is needed: set `current_phase` to the layer's phase, re-generate downstream artifacts.

## Budget Exhaustion

- depth >= max_depth (5) → escalated_to_human
- attempt >= max_attempts (3) → escalated_to_human
