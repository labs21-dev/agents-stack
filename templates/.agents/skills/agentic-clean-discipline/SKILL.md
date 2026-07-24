---
name: agentic-clean-discipline
description: >-
  Execution-time discipline for trusting AI-generated code without line-by-line
  review. Pipeline: risk-grade → reverse-gate → spec gate → AI generate →
  verify gate (unit/coverage/mutation) → metric gate (complexity/module/
  dependency) → L3 human line-read. Use when an agent will generate or modify code
  and the task is gradeable. NOT for docs, translation, one-off scripts, or
  explicit line-by-line co-write. Ships three valves the naive version omits:
  reverse-gate STOP, feedback upgrade (reopen grade from downstream evidence),
  category disclosure (defects gating cannot catch).
---

# Agentic Clean Discipline

On-demand SOP for trusting AI-generated code via gates instead of line review.

Method: grade → reverse-gate → spec → generate → verify → metric → (L3)
human read. Trust transfers between gates; it does not appear from nowhere. A
weak spec gate is the ceiling of the whole chain.

Tooling is language-agnostic and optional. Never claim "verified correct";
claim "no gate failure observed."

## When to trigger

An agent will generate or modify code AND the task is gradeable (failure cost
and reversibility nameable).

Do NOT trigger: docs, translation, lookups, one-off scratch scripts, pure
refactor with no behavior change, explicit line-by-line co-write.

## Sibling split

| Need | Skill |
|------|-------|
| Fuzzy multi-lens decision | `meta-thinking-framework` |
| Dangerous protocol contract + explore | `protocol-adversarial-design` |
| Trusting AI-generated code without line review | **this skill** |

Downstream of the other two. Protocol character in the task → spec gate
delegates to `protocol-adversarial-design` (`references/delegation.md`). Still
fuzzy decision → `meta-thinking-framework` first.

## Hard rules

1. **Reverse-gate first.** Fail a screen → STOP. Do not open gates.
2. **Spec is the ceiling.** Weak spec → weak chain. Self-check before generate.
3. **No single metric passes.** Combine and read; mutation cross-checks.
4. **Grade reopens on evidence.** Downstream results may falsify the step-0
   grade. Re-grade up by default when cost is high.
5. **State the category boundary every run.** Gates cannot catch abstract
   smell, cross-module emergence, or naming-intent drift.

## Flow (every invocation)

### 0. Risk grade

Grade L1/L2/L3 by `references/risk-grading-matrix.md` (failure cost ×
reversibility). State grade confidence. Flag cross-bucket corners — any L3
corner runs the whole task at L3.

- **L1** — exploration/prototype: spec(light) + smoke + human skim critical
  path. No mutation, no full metrics.
- **L2** — routine: hard spec + unit + coverage + mutation(sampled) + metrics.
- **L3** — safety/money/irreversible: L2 all + mutation(full) + trust-boundary
  review + line-level human read of core paths.

### 1. Reverse gate

Run `references/reverse-gate.md`. Any screen fails → STOP
(`templates/stop-output.md`), fall back to human reading. Do not gate a task
whose defect class gates cannot catch.

### 2. Spec gate

Turn the requirement into a hard spec. L2+ use Gherkin or stated invariants.
Run `references/spec-self-check.md`. Score < 3 and not cheaply raisable → STOP.

Protocol character (concurrency / idempotency / trust boundary / lifecycle /
cancel race) → delegate to `protocol-adversarial-design` per
`references/delegation.md`. Adopt its invariants + alignment tests as this
spec and the verify-gate core.

### 3. Generate

Generate. Bound retries/steps (`references/failure-patterns.md`).

### 4. Verify gate (open per grade)

Unit → coverage → mutation (L2 sampled / L3 full). Mutation testing catches
AI's signature failure: runs fine, edge missing, happy-path tests all green.
**The verifier must not be the generator** (`references/role-pipeline.md`).
No self-declared completion.

### 5. Metric gate

Complexity, module size, dependency structure, function length. Combine and
read per `references/metric-combo-rules.md`. Never pass on a single metric.
Mutation score cross-checks whether low complexity is real or cosmetic.

### 6. L3 only — human line-read core paths

Mandatory human reading for the highest-failure-cost grade. This skill does
not promise "never read."

### 7. Feedback upgrade

After any gate, run `references/feedback-upgrade.md`:
- verify-gate / mutation failure density far above the grade's prediction →
  re-grade (usually up), re-run denser gates.
- delegated `protocol-adversarial-design` reports danger above initial grade →
  re-grade up.

Grade is not fixed at step 0.

## Required output (non-STOP)

1. **Grade** — L1/L2/L3 + confidence + cross-bucket flag
2. **Reverse-gate** — one line per screen, pass/STOP
3. **Spec self-check score** + cage-strength-equals-spec-strength warning
   (red if < 3)
4. **Gates opened** — each gate's result
5. **Metric combo** — combined reading, not per-metric pass lines
6. **Category disclosure** — defects gating cannot catch (filled in)
7. **Assumptions to verify** — what could be wrong + lowest-cost test each

STOP runs need only: failed screen(s), reason, recommended alternative.

## Category disclosure (mandatory, filled in each run)

> This task's quality judgment is gate-based. Structurally uncatchable by
> gating: [abstract smell / cross-module emergence / naming-intent drift].
> Task sensitive to those → fall back to human reading.

## References

- `references/risk-grading-matrix.md` — L1/L2/L3 + cross-bucket rule
- `references/reverse-gate.md` — STOP screens
- `references/spec-self-check.md` — spec quality checklist + scoring
- `references/delegation.md` — delegate to `protocol-adversarial-design`
- `references/metric-combo-rules.md` — combine-and-read + anti-gaming
- `references/role-pipeline.md` — role separation (verifier ≠ generator)
- `references/feedback-upgrade.md` — reopen grade from downstream evidence
- `references/failure-patterns.md` — agent failure modes
- `references/anti-patterns.md` — how this skill fails

## Templates

- `templates/quality-report.md`
- `templates/stop-output.md`

## Self-loop

If a later delivery is defective, locate the leaking gate (spec / verify /
metric / grade) and fix only that gate's output.