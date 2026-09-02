---
last-updated: {YYYY-MM-DD}
---

# Constitution

<!--
  L2 — load before any architecture-level decision, or when a change might violate a principle.
  Records what scanning CANNOT find: things that are DELIBERATELY unchanging.
  Code shows current shape; it doesn't show "this is non-negotiable."
  last-updated with no status: a stale date here often means "deliberately unchanged,"
  not "rotted" — verify against code before distrusting it (the inverse of living docs).
-->

## Non-negotiable principles
<!-- REQUIRED. The few things the team refuses to trade away. Keep it short — a long
     constitution is one nobody reads. -->

1. **{principle}** — {what it means} — {why non-negotiable}. Violation → {consequence}.

## Deliberate non-goals
<!-- REQUIRED. Things we explicitly do NOT do, to stop agents from "helpfully" adding them. -->

-

## Trade-offs we've consciously accepted
<!-- fill if relevant. Costs we've paid on purpose. POINT to the ADR, don't restate it. -->

- {cost accepted} — for {benefit} — see `docs/ADR/NNN`

<!-- SELF-CHECK:
- [ ] Each principle says WHY it's non-negotiable (code shows shape, not intent).
- [ ] Non-goals present — these stop the agent from re-adding rejected scope.
- [ ] No principle duplicates a lint/test rule (those live in automation, not here).
- [ ] "Trade-offs" points to ADRs, does not re-copy the decision rationale.
- [ ] Not duplicated in AGENTS.md — AGENTS.md only points here.
-->