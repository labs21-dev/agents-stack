# AGENTS.md

This repository uses agents-stack v3 — a Goal-QA-Driven development harness with three verification checkpoints.

## Key Paths

- `.agents-stack/workstream/<ws-id>_{YYYYMMDD}/` — workstream artifacts (goal.md, spec.md, plan.md, arch-report.md, tasks.md, report.md, handoff.md, qa-report.md, changelog.md, status.json)
- `.agents-stack/tracked-work.json` — active/parked workstream registry
- `.agents-stack/reference/architecture.md` — pipeline, checkpoint system, project architecture
- `.agents/skills/using-agents-stack/` — orchestrator + phase SKILL.md files

## Core Invariants

1. **Files beat chat memory.** Durable state lives in `.agents-stack/`. Chat is not state.
2. **One active workstream.** Park or complete before starting another.
3. **Generator ≠ Auditor.** All three checkpoint workers (verify-architecture, analyze, qa) must be separate agent instances from the phases they verify. The agent that designs must not verify.
4. **Cold start must work.** A new agent recovers from files alone — no chat history needed.
5. **Iteration ≠ Retry.** Retry fixes execution within the same contract. Iteration questions the premise; go back to spec/plan.
6. **Three-checkpoint rhythm.** Every ~2 phases, a verification gate isolates risk before it compounds. Checkpoint #1: Architecture vs Goal. Checkpoint #2: SPEC×PLAN×TASKS consistency. Checkpoint #3: CODE vs REALITY. Skip a checkpoint = errors locked into the foundation. Backtrack cost: 1x vs 5-8x.

## Safety / Do Not Do

- Do NOT skip blocking gates. If `status.json.blocking_gate` is set and unmet → STOP, do not advance.
- Do NOT self-review. The agent that produces an artifact (spec, plan, code) must not verify that same artifact. Dispatched checkpoint workers enforce this — do not override.
- Do NOT modify `.agents-stack/reference/` outside of the release phase or an explicit `/update-reference` command.
- Do NOT change requirements by editing code. Update spec.md first, re-derive downstream artifacts.
- Do NOT bypass plan when architecture issues surface. Update plan.md, then re-derive tasks.
- Do NOT write implementation code as the orchestrator. Route, dispatch workers, verify results — never implement.

## Quick Resume

1. Read `CONSTITUTION.md`, `AGENTS.md`, `.agents-stack/tracked-work.json`
2. Read `.agents-stack/workstream/<ws-id>_{YYYYMMDD}/status.json` and strongest artifact
3. Load the phase SKILL.md from `.agents/skills/using-agents-stack/<phase>/SKILL.md`
   - If the loaded skill is `using-agents-stack` (orchestrator): route only, do NOT implement
4. Verify checkpoint matches disk state; continue from strongest valid checkpoint

Success: a cold-start agent reads these files and resumes safely without chat history.

## Pipeline

```
goal → spec → plan → [CHECK #1: Arch vs Goal] → tasks → [CHECK #2: ANALYZE] → implement → [CHECK #3: QA] → release
```

Each phase has a SKILL.md defining its contract, output format, verification gates, and handoff protocol. **Load it before executing the phase.** Skipping the skill = working without the spec.

Full pipeline documentation including checkpoint mechanics, risk isolation principle, and cost table: `.agents-stack/reference/architecture.md`.

## Commit & PR

### Commit Style

Conventional commits: `type(scope): description`. Types: `feat`, `fix`, `refactor`, `docs`, `chore`. Scope is the phase or component (e.g., `qa`, `plan`, `AGENTS.md`). Use the commit body for rationale — what changed and why, not just what.

### Before Committing

- Inspect `git status` + `git diff` — stage only intended files, never commit secrets
- Verify all checkpoint gates for the current workstream have passed

### Before PR

- Cold-start test: a fresh agent reading only `CONSTITUTION.md`, `AGENTS.md`, and `.agents-stack/` can resume the workstream
- Generator ≠ Auditor: the reviewer must not be the agent that implemented the code

## Intent Routing

| User Intent | Route To | Action |
|-------------|----------|--------|
| **Pipeline work** — spec, plan, tasks, implement, qa, release, or active workstream with development intent | `using-agents-stack` | Load orchestrator; it routes to the correct phase based on artifact state |
| **Ad-hoc development** — one-off bugfix, feature, refactor, question, exploration (no workstream context) | **Direct execution** | Implement directly or load the appropriate domain skill |

For skill-specific intents (code review, frontend QA, design review, adversarial QA, complexity audit, reflect/learn), see the Contextual Skill Resolver in your platform's AGENTS.md.
