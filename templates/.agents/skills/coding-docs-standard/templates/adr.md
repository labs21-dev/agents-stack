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
  date is immutable (decision date). last-updated is intentionally absent —
  editing is forbidden; supersede instead.
-->

## Context
<!-- REQUIRED. The situation forcing the decision. Not scannable from code — code
     only shows the outcome. -->

## Decision
<!-- REQUIRED. What we chose. One paragraph. -->

## Rejected alternatives
<!-- REQUIRED — do not leave empty. The anti-relitigation payload. An agent
     "improving" back to a rejected option must hit this table first. -->

| Alternative | Why rejected |
|---|---|
| {option} | {specific reason} |

## Consequences
<!-- REQUIRED. -->
- Positive:
- Negative / accepted cost:
- Reversibility:

## Supersedes / superseded by
<!-- fill if relevant -->

<!-- SELF-CHECK:
- [ ] Rejected alternatives is filled — reject the ADR if empty.
- [ ] Append-only — if the decision changed, this status → superseded and a new ADR
      is written, not this one edited (date stays immutable).
- [ ] Context explains the WHY, not just the outcome (the outcome is in code).
- [ ] No content duplicated in CONSTITUTION.md "trade-offs" — it points here, not the reverse.
-->