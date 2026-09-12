# Screening — four gates

All four must pass. Any failure → **STOP** (do not model).

## Screen 1 — Independent movers?

Are there **two or more** actors/events that can advance shared state without a
single global lock in the real system?

Examples that pass: in-flight tool + user cancel; retry + original response;
leader failover + client write; two guards that both claim to decide allow/deny.

Fail if: only one synchronous request-response with no concurrent mutator.

**Note:** Two *mechanism names* (e.g. path jail + root jail) are not movers.
Movers are events: request arrives, path resolves, config reloads, cancel fires.

## Screen 2 — Failure is expensive?

Would a violation be a correctness / safety / money / trust incident — not a
mild UX miss?

Pass: double charge, data loss, authz escape, session written after reject,
handoff then append to dead session.

Fail: copy tone, layout, cache-miss latency, "skill markdown hard to read."

## Screen 3 — Thin enough?

Can the slice be told with **roughly ≤ 15 state variables** and a handful of
actions?

Pass: workspace + path + decision; pendingApproval + toolRunning + sessionOpen.

Fail: "whole ReAct loop + all tools + prompts + skills." Shrink first or STOP.

## Screen 4 — Hard sentence possible?

Can you state the property as a crisp invariant?

Good: `allow ⇒ resolvedPath ∈ workspace`

Bad: `agent should behave safely` / `UX should feel fast`

If you cannot write the sentence without weasel words → STOP; write ordinary
acceptance criteria / tests instead.

---

## Negation list (do not use this skill)

- CRUD with clear single-writer semantics
- Pure UI, copy, branding, layout
- Prompt / skill / docs wording
- Product semantics that still churn weekly
- "Design the whole system / agent" with no protocol slice named
- Asking for a full TLA+ language course (point to `tool-tla-plus.md` only after a thin protocol exists; Mode A/B usually enough)

---

## STOP output pattern

```
STOP — Protocol Adversarial Design
Failed screen(s): <N, …>
Why: <one sentence each>
Do instead: <tests | ADR | code review | shrink slice to X | meta-thinking>
```

---

## Pass → next

Hand off to hard acceptance (`hard-acceptance.md`) with a one-line protocol name
and the draft invariant candidate (even if rough).
