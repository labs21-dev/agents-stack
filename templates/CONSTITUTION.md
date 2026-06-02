# Constitution

This document is the project's technical charter. It defines invariants and rules that all workstreams must follow.

## Core Invariants

1. **Files are state** — all durable state lives in `.agents-stack/`
2. **One active workstream** — at most one non-parked workstream at a time
3. **Implementer ≠ Verifier** — implement and qa must be dispatched to different workers
4. **Cold start must work** — a new agent recovers full state from files alone
5. **Iteration ≠ Retry** — retry fixes execution, iteration questions premises

## Workflow Rules

- spec phase must produce BDD-format Acceptance Criteria
- tasks phase: each task must include 5-dimension verification metadata
- implement must follow RED-GREEN-REFACTOR cycle per tasks.md, each task passing before the next
- qa must independently reproduce and verify every AC from SPEC
- Change requirements → update spec first. Change architecture → update plan first.
- Project milestones and workstream backlog are defined in `ROADMAP.md`

## State Machine Mode

Pipeline enforcement is binary. No fuzzy intent detection, no contextual override.

`status.json.state_machine`:
- `"on"` — Pipeline strictly enforced. Phases execute in linear order. Agent cannot skip or bypass. Say "turn off state machine" to exit.
- `"off"` — No pipeline interference. Free-form execution.

Default: `"on"` when a workstream is active. Toggle anytime.

<!-- Add project-specific tech stack, coding standards, and architectural constraints below -->
