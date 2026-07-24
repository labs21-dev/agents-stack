# Thin state machine

You are not writing the product. You are writing the **smallest machine** that
can violate the invariant.

## Pieces

| Piece | Meaning |
|-------|---------|
| **Variables** | Protocol-relevant state only |
| **Init** | Legal starting valuations |
| **Next / Actions** | Atomic steps movers can take |
| **Invariant** | What must hold in every reachable state (and/or between steps) |

Optional later: fairness / liveness. Skip on first shot.

## Sizing

- Target **≤ ~15 variables**; prefer **3–8**.
- Actions should be obvious events: `RequestAccess`, `ResolvePath`, `UserReject`,
  `ToolFinish`, `Retry`, `EpochBump`.
- If you need a variable for "the LLM's mood" — you left the protocol.

## Mental compile (no TLA+ required)

```
Variables:  workspace, requestedPath, resolvedPath, decision
Init:       decision = undecided ∧ workspace = W0
Actions:    Request(path) | Resolve | DecideAllow | DecideDeny
Invariant:  decision = allow ⇒ resolvedPath ∈ workspace
```

Same content can later become a `.tla` file; the thinking is identical.

## Cutting guide

| Keep | Cut |
|------|-----|
| ids, statuses, epochs, locks, paths, votes | UI strings, prompts, metrics dashboards |
| allow/deny, pending/running/done | Full tool implementations |
| "who may write" | How the write is serialized on disk |

## Dual-rule smell in the model

If two actions can set `decision` from unrelated predicates that disagree,
stop and collapse to one Decide step driven by the source truth.

## Next

Explore with a table or TLC — `exploration.md`.
