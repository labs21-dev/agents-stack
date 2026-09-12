---
name: refactor-review
description: >-
  Structured review of AI-proposed software refactors and architecture
  optimizations. Core job is verification (did it solve the real problem, did
  it add risk, is migration controllable) — not "understanding the writeup."
  Use when the user asks to review a refactor/architecture proposal, optimize
  "the whole architecture," accept/reject AI redesigns, or wants a review
  checklist before migrating. Also use when an upstream skill or caller needs
  a refactor review with on-demand domain specialization. Method: load fixed
  kernel → caller (or this agent) fills a specialization card → lint the card
  → risk-tier L1/L2/L3 → structured review. Do NOT use for line-by-line code
  review of a small patch (use normal review / agentic-clean-discipline), pure
  product strategy (meta-thinking-framework), or protocol race contracts
  (protocol-adversarial-design).
---

# Refactor Review

On-demand SOP for reviewing **software refactors / architecture changes**
proposed by AI (or humans). Audience: engineers who must decide accept /
modify / reject without being persuaded by a polished writeup.

**Spirit:** Verify, don't merely comprehend. Nail goals first. Domain checks
are generated **on demand** by the caller — not a mega checklist that pretends
to cover every refactor type.

**Composition:**

```
fixed kernel  +  specialization card (on demand)  →  tiered review
```

## When to trigger

See frontmatter. Sibling split:

| Need | Skill |
|------|--------|
| Fuzzy multi-lens decision | `meta-thinking-framework` |
| Dangerous protocol contract + explore | `protocol-adversarial-design` |
| Trust AI-generated *code* via gates | `agentic-clean-discipline` |
| Review AI *refactor / architecture* proposal | **this skill** |

## Hard rules

1. **Kernel is immutable.** Specialization may only *tighten* checks, never
   waive failure paths, migration/rollback, goal-nailing, or invariants lint.
2. **No valid specialization card → L1 only.** Do not claim a full domain
   review without a lint-passing card.
3. **Verify ≠ understand.** Output must be checkable against goals, evidence,
   failure paths, and migration — not a summary of the proposal's narrative.
4. **Tier by irreversibility.** Pay full process cost only at L3.
5. **State grade and specialization quality every run.** If invariants lack
   falsifiers, downgrade them to hypotheses (not hard gates).

## Flow (every invocation)

### 0. Confirm goals (or STOP)

If the task has no explicit **optimization goals / hard constraints /
success metrics / acceptable trade-offs**, force them out first using
`references/kernel.md` § Goal nail. Without this, stop at a
**GOALS-REQUIRED** output — do not review aesthetics.

### 1. Load kernel

Read `references/kernel.md`. These clauses cannot be overridden.

### 2. Obtain specialization card

Prefer the **caller** supplies the card (they hold task context). If missing,
this agent generates one from the task using
`templates/specialization-card.md`, then treats it as **provisional**
(caller should confirm on L2/L3).

### 3. Lint the card

Apply `references/specialization-lint.md`.

- **Fail** → repair once, or fall back to **L1-only** review and label
  `specialization: invalid`.
- **Pass** → continue; note any INVARIANT rows that are hypotheses only.

### 4. Grade risk tier

Assign L1 / L2 / L3 per `references/risk-tiers.md` (impact × reversibility ×
invariant touch). Specialization `L_TRIGGERS` may *raise* the tier, not lower
below kernel floors.

### 5. Run structured review

Produce output per `templates/review-output.md`, depth by tier
(`references/risk-tiers.md` § Required depth). Use layered question types in
`references/layered-checklist.md`, filled with specialization
INVARIANTS / FAILURE_MODES / EVIDENCE_REQUIRED / DO_NOT.

### 6. Decide per major change

For each core change: **Accept / Modify / Reject** + one-line reason.
L2+ : short ADR stubs for Accepts. L3 : adversarial pass + path walk +
pilot recommendation (see kernel § Techniques).

## Output contract

Always include:

1. Goals/constraints echo (or GOALS-REQUIRED)
2. Specialization lint result + tier
3. Structured review body (tier-appropriate sections)
4. Per-change verdicts
5. Open hypotheses + cheapest falsifiers

## References

- `references/kernel.md` — immutable review kernel
- `references/specialization-lint.md` — card lint + degrade rules
- `references/risk-tiers.md` — L1/L2/L3 triggers and depth
- `references/layered-checklist.md` — four review layers (question types)

## Templates

- `templates/specialization-card.md` — on-demand domain card schema
- `templates/review-output.md` — review output skeleton
- `templates/caller-invoke.md` — paste-ready invoke block for callers
