---
adr: {NNN}
title: {short title}
status: proposed | accepted | superseded-by-{NNN} | deprecated
date: {YYYY-MM-DD}
---

# ADR {NNN}: {title}

<!--
  The ONLY class allowed to record the "why." Append-only — never edit; supersede
  with a new ADR linking back. The REJECTED ALTERNATIVES field is the highest-value
  part: code can never show what was turned down, and it's what stops an agent from
  re-opening a dead debate.
-->

## Context
<!-- The situation forcing the decision. Not scannable from code — code only shows the outcome. -->

## Decision
<!-- What we chose. One paragraph. -->

## Rejected alternatives (REQUIRED — do not leave empty)

| Alternative | Why rejected |
|---|---|
| {option} | {specific reason} |

<!-- This field is the anti-relitigation payload. An agent "improving" back to a
     rejected option must hit this table first. -->

## Consequences
- Positive:
- Negative / accepted cost:
- Reversibility:

## Supersedes / superseded by
<!-- If this replaces or is replaced by another ADR, link it here. -->

<!-- SELF-CHECK:
- [ ] Rejected alternatives field is filled — reject the ADR if empty.
- [ ] Append-only — if the decision changed, this status → superseded and a new ADR is written, not this one edited.
- [ ] Context explains the WHY, not just the outcome (the outcome is in code).
-->