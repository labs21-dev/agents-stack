---
name: skill-evolution
description: Evolve skills from real usage. Use when a skill has been used enough to accumulate evidence and the user wants to decide whether a piece of it should graduate into the standard set, be deprecated, or be revised — collects passive usage cases, flags candidates that cross a frequency-plus-verification threshold, drafts concrete upgrade patches, and routes them through a human gate. Also use when the user asks "should this lens/rule/trigger become permanent?", "this skill keeps getting it wrong, should we remove that rule?", or wants to set up case-driven evolution for a skill. Does not legislate skill standards itself — only accumulates cases and drafts patches; the human approves every change.
---

# Skill Evolution (L2 + L3)

The companion to **skill-creator**. Where skill-creator owns short-cycle, human-driven iteration within a session (L0 generation, L1 evaluation), this skill owns the **long-cycle, case-driven evolution across sessions**:

- **L2 Evolution** — collect real usage cases → flag candidates → draft upgrade/deprecate patches → human gate → merge (with rollback).
- **L3 Accumulation** — accumulate what "a good skill" means across skills, as cases. **Accumulate only, never legislate** — folding a pattern into a standard is a human action (the reflexivity defense).

## Reflexivity defense (structural, not preference)

This skill is a meta-skill operating on skills. A meta-skill that grades its own output with its own standard drifts into **self-validating mediocrity** — everything passes its own bar, quality monotonically decays, no external signal interrupts it. Therefore:

- **L3 legislation is human-only.** This skill accumulates cases and flags candidate patterns; it never folds a pattern into a standard itself.
- **Cases are passive + post-hoc verified, not self-rated.** The agent doesn't declare its own use "effective"; effectiveness is judged by an external outcome.
- **Patches are AI-drafted, human-gated.** The AI proposes a concrete diff; the human approves, rejects, or amends before it's applied.
- **L3 seed standards are borrowed, not self-generated.** External frameworks (e.g. CCA, extract-methodology's common-law loop) are the cold-start anchor.

## The evolution state machine

```
IDLE (passively collect cases)
  → effective cases ≥ N AND ≥1 post-hoc verified   → FLAG (upgrade candidate)
  → adverse cases  ≥ M                              → FLAG (deprecate candidate)
FLAG
  → AI drafts a concrete patch (scope + diff + evidence + risk tag + before-snapshot instruction)
  → DRAFTED
DRAFTED
  → human reviews: approve / reject / amend          → APPROVED | REJECTED
APPROVED
  → apply patch + keep before-snapshot + write changelog
  → MERGED
MERGED
  → next real usage verifies the change sharpened output; if it regressed, roll back the snapshot
REJECTED
  → back to IDLE; if adverse cases persist, proceeds toward DEPRECATE
```

Upgrade and deprecate are **symmetric** — a skill that only ever upgrades accumulates dead rules. Adverse-case deprecation runs the same machine with a different FLAG trigger.

## Thresholds

- **Upgrade candidate**: a single rule/lens/trigger has **≥3 effective cases**, **and** ≥1 of those is **post-hoc verified** (not self-rated).
- **Deprecate candidate**: **≥3 adverse cases** for an existing rule.
- N=3 / M=3 are initial values. They are themselves accumulated — if validation shows they're too loose (false upgrades) or too tight (deserved upgrades stalling), that becomes an L3 agenda item, not a silent tweak.

## Risk grading (gate tightness)

| Change type | Risk | Gate | before-snapshot |
|---|---|---|---|
| Add example, add trigger condition, add a clarifying section | Low | batch fast review | recommended |
| Graduate a candidate lens/rule into the standard set | Medium | per-item review | required |
| Change a core rule, deprecate an existing rule | High | per-item strict + two-person | required |

## AI patch authority boundary

- **AI may**: passively collect cases, flag threshold-crossing candidates, draft concrete upgrade/deprecate patches (diff + scope + evidence summary + risk tag + reversibility + before-snapshot instruction).
- **AI may not**: apply a patch itself, edit the L3 constitution/INDEX recurring-patterns or legislation-log, auto-fill recurring-patterns, or self-rate a case as effective (must be post-hoc verified).

## Files

- `references/evolution-protocol.md` — full upgrade/deprecate flow, thresholds, risk grading
- `references/patch-draft-format.md` — the format an AI-drafted patch must follow
- `references/l3-accumulate.md` — the lightweight L3 accumulate-only mechanism (compound/)
- `templates/evolution-log.md` — per-skill case log (copy into a skill that mounts evolution)
- `templates/evolution-attach.md` — the SKILL.md fragment a mounted skill adds, pointing here

## Mounting evolution on a skill

To give a skill evolution capability:
1. Copy `templates/evolution-log.md` into the skill's `references/` (renamed e.g. `evolution-log.md`).
2. Append the `templates/evolution-attach.md` fragment to that skill's `SKILL.md`.
3. The skill now passively records cases and can flag candidates; upgrades route through this skill's protocol + the human gate.

A skill need not mount evolution. Simple one-off skills shouldn't — the case-collection overhead isn't worth it. Mount it on skills that recur and accumulate real usage. (Mechanism, not policy: provide the capability, let the skill decide.)

## Reflexivity self-check

This skill is itself N=1 — its protocol is derived from one worked example (the meta-thinking-framework emerging-lenses-log). It is calibrated by its own output: every evolution event it processes is evidence about whether the protocol is right. After N≥3 events, the human reviews whether the six-step machine and the thresholds are correct; some may merge, split, or drop. The skill is designed to be re-calibrated by its own output, not frozen.