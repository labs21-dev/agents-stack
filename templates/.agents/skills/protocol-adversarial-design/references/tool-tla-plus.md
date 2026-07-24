# Optional formal backend — minimal TLA+/TLC

One **Mode C** option after hard acceptance + thin machine exist. This skill
does not require TLA+; prefer Mode A/B unless you need this artifact. Not a
language course.

## When to escalate

- User explicitly wants a `.tla` artifact or CI-able formal check
- Mode B is a poor fit (e.g. fairness / large structured concurrency) and a
  checker helps
- Multiple epochs / quorums / retries make manual or ad-hoc enumeration dishonest

## Minimal shape (sketch)

```tla
---- MODULE ProtocolSlice ----
EXTENDS Integers, Sequences, TLC

VARIABLES workspace, path, decision

TypeOK == decision \in {"undecided", "allow", "deny"}

Init == /\ decision = "undecided"
        /\ workspace = <<"repo", "root">>
        /\ path = << >>

\* Replace with real path algebra as needed — keep tiny.
ResolveAllow == /\ decision = "undecided"
                /\ decision' = "allow"
                /\ UNCHANGED <<workspace, path>>

ResolveDeny == /\ decision = "undecided"
               /\ decision' = "deny"
               /\ UNCHANGED <<workspace, path>>

Next == ResolveAllow \/ ResolveDeny

Inv == decision = "allow" => TRUE  \* replace with real membership check

Spec == Init /\ [][Next]_<<workspace, path, decision>>
====
```

Replace `Inv` with the hard sentence compiled into TLA+. Keep variables aligned
with `state-machine-stub.md`.

## TLC checklist

1. Write `ProtocolSlice.tla` + a model (Toolbox or CLI) with `Inv` as invariant
2. Bound domains tightly (small sets)
3. On error: export/read the trace; return to design precedence
4. On success: still list model assumptions in Boundaries

## Install / run (pointer only)

- TLA+ Toolbox or VS Code TLA+ extension + TLC
- Prefer checking **one invariant** first; add more only when stable

As of 2026-07: core TLA+/TLC practice is **settled**; editor/tooling UX moves —
verify current install docs when teaching commands.

## Do not

- Start here before Gate + hard sentence
- Encode the entire product
- Treat green TLC as production certification
