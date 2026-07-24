# Security

<!--
  L2 — load only when touching auth, trust boundaries, external data, or any attack surface.
  Records what scanning CANNOT find: WHY the boundaries are drawn here, what's trusted.
  Code shows a check exists; it doesn't show the trust model behind it.
-->

## Trust boundaries

| Boundary | Trusted side | Untrusted side | Why drawn here |
|---|---|---|---|

## What is trusted (and the assumption behind each)

- {source/actor} — trusted because {assumption}. If assumption breaks → {consequence}.

## What is NOT trusted / must be validated

-

## Attack-surface assumptions

<!-- Things we assume about the threat model. If wrong, the defense is misplaced. -->

-

## Don'ts (that no lint/test enforces)

-

<!-- SELF-CHECK:
- [ ] Each boundary explains WHY, not just that a check exists (code shows the check).
- [ ] Trust assumptions are explicit (the unscannable part).
- [ ] No rule here is duplicated in AGENTS.md — AGENTS.md only points here.
- [ ] Automatable don'ts are lint/test rules, not prose.
-->