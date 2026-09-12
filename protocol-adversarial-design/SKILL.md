---
name: protocol-adversarial-design
description: >-
  Design-time checkable contracts for high-risk software protocols — concurrency,
  retries/idempotency, distributed handoff, authz/trust boundaries, lifecycle state
  machines, approval/cancel races, and "which rule wins" ambiguity. Use when the user
  designs or reviews such a protocol, wants hard acceptance criteria that survive
  interleaving, asks to find edge cases in state transitions, mentions TLA+/model
  checking/PlusCal for a thin protocol, or says "single source of truth" for
  derived guards. Even if they only say "write acceptance for this race" or
  "adversarial QA for this state machine," use this skill. Do NOT use for CRUD,
  pure UI/copy, single request-response with no shared mutable state, prompt/skill
  wording, or weekly-churning product semantics. Not a general architecture or
  product-decision framework (use meta-thinking for those). Tooling is optional
  and language-agnostic (table first; any bounded explorer; TLA+/TLC optional).
  Method: gate → hard invariant → thin state machine → adversarial explore →
  align tests.
---

# Protocol Adversarial Design

On-demand **SOP** for turning a dangerous protocol into a **checkable hard
acceptance contract**, then adversarially exploring its state space. Audience:
software engineers. Problem class: narrow — interleaving, composition, trust
adjudication, lifecycle — not every design task.

**Spirit:** Init / Next / Inv + search for a bad trace (TLA+/TLC lineage),
evolved for day-to-day protocol design — not a formal-methods course.

**Tooling is optional and language-agnostic.** Default = state table +
invariant. Escalate to any bounded executable explorer, or an optional formal
checker (e.g. TLC). Never claim "proven correct"; claim "no violation inside
the model."

## When to trigger

See frontmatter. Sibling split:

| Need | Skill |
|------|--------|
| Fuzzy multi-lens decision | `meta-thinking-framework` |
| Dangerous protocol contract + explore | **this skill** |
| Implementation tests / red-team outside the model | normal QA / security practice |

## Hard rules

1. **Gate first.** Fail the screen → stop. Do not model.
2. **Thin > whole system.** First shot ≤ ~15 variables; one protocol slice.
3. **Single source of truth.** Derived mechanisms must not appear as peer truths in the source invariant.
4. **Explore ≠ prove.** Model-green ≠ reality-safe. State uncovered assumptions every turn.
5. **Fix design before code.** Counterexamples rewrite precedence / truth; then align implementation.

## Flow (every invocation)

### 1. Gate — screen or stop

Apply the four screens in `references/screening.md`. If any fails, output a
**STOP** using the template section below and suggest the cheaper alternative
(tests, ADR, code review). **End.**

### 2. Hard acceptance

Write 1–3 invariants in hard language (no "should" / "尽量"). Ban derived
mechanism names from the source sentence. Follow `references/hard-acceptance.md`.
Fill `templates/protocol-brief.md`.

### 3. Thin model

Define Variables / Init / Next (actions) only for the protocol slice. Use
`references/thin-state-machine.md` and `templates/state-machine-stub.md`.
If the model wants UI, prompts, or full product surface — cut.

### 4. Adversarial explore

Prefer a combination/state table first (Mode A). If the user wants a runnable
check or the table cannot cover the interleavings, escalate to **executable
bounded explore** in any runner (Mode B). Use a formal checker such as
TLA+/TLC only when asked or when that artifact is the right fit (Mode C) —
see `references/exploration.md`, `templates/bounded-explore-stub.md`, optional
`references/tool-tla-plus.md`. Interpret counterexamples as design bugs
(precedence / dual truth), not "add an if." Do **not** default to writing a
script every run.

### 5. Align

List 3–5 implementation tests that nail the contract. State model boundaries
and what remains for human/adversarial QA outside the model. Use
`templates/alignment-tests.md`.

## Required output shape

Every completed run (non-STOP) must include:

1. **Gate** — why it passed (one line per screen)
2. **Invariants** — the hard sentences
3. **Thin model** — variables, init, actions (table or stub)
4. **Explore** — table and/or executable bounded explore and/or formal-checker
   result; counterexample trace if any (name the backend used)
5. **Design fix** — what truth/precedence changed (if broken)
6. **Align tests** — 3–5 cases
7. **Boundaries** — assumptions + explicitly uncovered attacks/surfaces

STOP runs only need: failed screen(s), reason, recommended alternative.

## References

- `references/screening.md` — four screens + negation list
- `references/hard-acceptance.md` — writing invariants
- `references/thin-state-machine.md` — Init/Next mindset
- `references/exploration.md` — table / executable explore / formal checker
- `references/tool-tla-plus.md` — optional TLA+/TLC path (one formal backend)
- `references/anti-patterns.md` — how this skill fails
- `references/domain-examples.md` — short cross-domain examples

## Templates

- `templates/protocol-brief.md` — gate + invariants
- `templates/state-machine-stub.md` — variables / actions / invariants
- `templates/bounded-explore-stub.md` — language-agnostic Mode B checklist
- `templates/alignment-tests.md` — implementation alignment checklist
