# agents-stack v3 state machine

Goal-QA-Driven phase model. Orchestrator reads these rules, decides next phase, dispatches worker.

## Core Invariants

1. Files are state. Chat memory is not durable.
2. Exactly one workstream active at a time. Others must be parked.
3. Implementer ≠ Verifier (Generator ≠ Auditor). Implement and QA must be separate workers.
4. Cold start must work. A new agent recovers from files alone.
5. Iteration ≠ Retry. Retry fixes execution within same contract. Iteration changes spec/plan.

## Artifact Precedence

When files disagree, higher-precedence artifact wins:

1. qa-report.md
2. handoff.md
3. tasks.md
4. plan.md
5. spec.md
6. status.json
7. .agents-stack/tracked-work.json

## Phase Table

| Phase | Evidence | Next Step |
|-------|----------|-----------|
| uninitialized | Missing or empty tracked-work.json | Create first workstream |
| goal | goal.md exists | Route to spec |
| spec | spec.md exists | Route to plan |
| plan | plan.md exists + architecture trace complete | Route to tasks |
| verify-architecture | arch-report.md exists with PASS verdict | Route to tasks |
| tasks | tasks.md exists | Route to analyze (Checkpoint #2: consistency gate) |
| analyze | Checkpoint #2 passed | Route to implement |
| implement | handoff.md exists | Route to qa (Checkpoint #3: adversarial verification) |
| qa | qa-report.md exists | Evaluate verdict |
| release | changelog.md exists + archived | Complete |
| awaiting_human | status.json blocked_reason set | Human decision |
| escalated_to_human | max depth/attempt exceeded | Human decision |
| archived | Evidence in .agents-stack/archive/ | Next workstream |

## Transition Rules

### Contextual Trigger (overrides artifact check at any point)

Before artifact-driven routing, detect user natural language intent:
- "goal/define direction" → route goal (create workstream if needed)
- "spec/think through" → route spec (create workstream if needed)
- "architecture/plan" → route plan
- "tasks/breakdown" → route tasks
- "implement/code" → route implement
- "QA/verify/test" → route qa
- "release/ship" → route release
- "review code" → load clean-philosophy skill (non-pipeline)
- "browser test/UI check" → load frontend-qa skill (non-pipeline)
- "design review" → load frontend-design skill (non-pipeline)
- "complexity audit/prune" → dispatch prune-review (non-pipeline)
- No clear intent → fall through to artifact-driven routing

### Forward Pipeline

- No goal.md → route goal
  - goal worker reads CONSTITUTION.md, tracked-work.json, defines goal.md (problem, success criteria, non-goals, constraints)
- goal.md exists, no spec.md → route spec
  - spec worker reads goal.md + CONSTITUTION.md, derives user stories and ACs from goal, writes spec.md
- spec.md exists, no plan.md → route plan
  - plan worker reads goal.md + spec.md, designs architecture with Architecture Trace, writes plan.md
- plan.md exists, no tasks.md → route verify-architecture (Checkpoint #1)
  - verify-architecture worker reads spec.md + plan.md, produces arch-report.md
  - validates Architecture Trace completeness + goal mapping + over-engineering signals
  - PASS → set `phase_gates.tasks.entry_ok = true`, route tasks
  - FAIL → route back to plan (fix architecture before task breakdown)
- `phase_gates.tasks.entry_ok = true`, no tasks.md → route tasks
  - tasks worker reads spec+plan, breaks into tasks with 5D verification, writes tasks.md
- tasks.md exists, no handoff.md → route analyze (Checkpoint #2: spec×plan×tasks consistency gate)
  - orchestrator checks spec+plan+tasks consistency before dispatching implement
  - gate passes → set `phase_gates.implement.entry_ok = true`, route implement
  - minor gaps → route tasks with fix suggestions
  - major gaps → route analyze (human or automated cleanup)
  - severe gaps → route back to spec or plan
- analyze gate passed, no handoff.md → route implement
  - implement worker reads tasks, implements each with RED-GREEN-REFACTOR cycle, writes handoff.md
  - each task must clear Inter-Task Gate before next task (see implement/SKILL.md)
  - all tasks done → set `phase_gates.implement.handoff_written = true`
  - review agent passes → set `phase_gates.implement.review_approved = true`
  - if build/startup fails: implement_failed, orchestrator may retry
- handoff.md exists AND `phase_gates.implement.handoff_written = true` AND `phase_gates.implement.review_approved = true` → route qa
  - qa worker independently reproduces and verifies against SPEC
  - verdict: PASS, FAIL, or BLOCKED
  - on FAIL: trace to layer (L1 code, L2 architecture, L3 spec)

### Post-QA

- PASS → route release
- FAIL + Layer 1 (code) + attempt < max_attempts → route implement (retry)
- FAIL + Layer 2 (architecture) → route plan (re-plan)
- FAIL + Layer 3 (spec) → route spec (re-spec)
- FAIL + attempt >= max_attempts → escalated_to_human
- BLOCKED → awaiting_human

### Post-Release

- changelog.md exists → archive workstream
- Update tracked-work.json
- Ready for next workstream

## Three-Layer Rework

| Layer | Scope | Affected Phase | Cost |
|-------|-------|---------------|------|
| L1: Code | Implementation error, missed edge case | implement | Low |
| L2: Architecture | API/DB design insufficient | plan | Medium |
| L3: Spec | Requirement/AC missing or wrong | spec | High |

## Budget Exhaustion

- depth >= max_depth (5) → escalated_to_human
- attempt >= max_attempts (3) → escalated_to_human
