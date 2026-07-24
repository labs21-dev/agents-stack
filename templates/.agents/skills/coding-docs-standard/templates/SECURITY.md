---
last-updated: {YYYY-MM-DD}
---

# Security

<!--
  L2 — load only when touching auth, trust boundaries, external data, or any attack surface.
  Records what scanning CANNOT find: WHY the boundaries are drawn here, what's trusted.
  Code shows a check exists; it doesn't show the trust model behind it.
  last-updated with no status: a stale date may mean "trust model unchanged" or "rote."
  If touching auth, verify the boundaries below against current code before trusting them.
-->

## Trust boundaries
<!-- REQUIRED. -->

| Boundary | Trusted side | Untrusted side | Why drawn here |
|---|---|---|---|

## What is trusted (and the assumption behind each)
<!-- REQUIRED. The unscannable part: code shows the check, not the assumption behind it. -->

- {source/actor} — trusted because {assumption}. If assumption breaks → {consequence}.

## What is NOT trusted / must be validated
<!-- REQUIRED. -->

-

## Attack-surface assumptions
<!-- REQUIRED. Things we assume about the threat model. If wrong, the defense is misplaced. -->

-

## Don'ts
<!-- fill if relevant. ONLY don'ts that no lint/test enforces. If a lint/test CAN
     enforce it, make it a lint/test rule and drop it from here — don't keep a prose
     copy that rots. -->

-

<!-- SELF-CHECK:
- [ ] Each boundary explains WHY, not just that a check exists (code shows the check).
- [ ] Trust assumptions are explicit (the unscannable part).
- [ ] Every "Don't" cannot be turned into a lint/test rule (automatable ones were moved out).
- [ ] No rule here is duplicated in AGENTS.md — AGENTS.md only points here.
-->