# Layered loading (L0 / L1 / L2)

An agent's context budget is a fixed tax on every doc it loads. Loading too
much dilutes attention — the agent starts skipping, which is equivalent to no
docs. Load by trigger, not by habit.

## L0 — always in context

Only `AGENTS.md`. It must stay small: rules + pointers + verify commands.
**Never inline L2 content here.** A SECURITY rule copied into `AGENTS.md` is a
second source of truth that rots independently. Pointer only: `→ see docs/SECURITY.md`.

## L1 — task-relevant

The current `docs/plan/*` + the ADRs relevant to the task. Load when continuing
or starting scoped work. `docs/archive/` is **not** L1 — an agent should not
pull archived plans by default; load a specific one only if it needs to
understand a past decision that was never promoted to an ADR.

## L2 — boundary-triggered

- `docs/SECURITY.md` — load when touching auth, trust boundaries, external data,
  or any attack surface.
- `docs/CONSTITUTION.md` — load before any architecture-level decision or when a
  change might violate a principle.

Triggering is the agent's judgment. `AGENTS.md` tells it **when** to pull L2
(e.g. "before changing anything in `auth/`, read `docs/SECURITY.md`") — that
pointer is L0; the content stays L2.

## Anti-patterns

- ❌ One giant `AGENTS.md` with everything → context overload, single-point
  decay, no layered loading.
- ❌ Copying SECURITY/CONSTITUTION rules into `AGENTS.md` for "convenience" →
  violates single source; the copy goes stale.
- ❌ Loading L2 unconditionally → wastes budget on tasks that don't need it.