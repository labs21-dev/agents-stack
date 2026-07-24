# Decay defense

Code is alive; docs are inert. The instant they separate, docs begin to rot.
This skill treats decay as a time-function and defends with three mechanisms.

## 1. Single source

Any rule lives in exactly one file. Before saving a doc:

- `grep` the repo for the rule's key sentence. It must not appear in two docs.
- If it does → pick one home, replace the other with a pointer
  (`→ see docs/CONSTITUTION.md §X`).

Two copies = two truths decaying at different rates. The agent may draw the
older one and be confidently wrong.

## 2. Detectable failure (prefer automation over prose)

If a constraint **can** be enforced by CI / lint / type / test, it **must** be.
A prose rule is a hope; a failing build is a fact.

- "Don't import `X` from `Y`" → eslint/depcheck rule, not a doc sentence.
- "All public API has tests" → coverage gate, not a doc sentence.
- "This invariant holds" → a test that fails when it doesn't.

The doc's job for an automatable constraint is to **point at the gate** and
explain the *why* the gate can't express (gates don't hold rationale). This is
the only case where a doc and a gate co-exist on the same constraint — and the
doc holds the rationale, not the rule.

## 3. Living docs carry timestamps; dead docs archive; ADRs supersede

Three "outdated" treatments, not one:

- `docs/plan/*` and `docs/handoff/*` carry `last-updated`. A living doc past its
  freshness is **not** ground truth — the agent should treat it as a hint and
  re-verify against code.
- **Completed plans / retired handoffs move to `docs/archive/<class>/`**
  immediately. A live list mixing "done" and "in progress" makes the agent
  misjudge state. Retired SECURITY/CONSTITUTION files also archive (with a stub
  pointer left at the original path).
- **ADRs are append-only and never archived.** Supersede in place with a new
  numbered ADR linking back; the old one keeps `status: superseded-by-NNN`.
  History *is* the point — archiving an ADR hides exactly the record an agent
  needs when it stumbles onto an old decision and would otherwise relitigate it.

In one line: **living → `docs/`; dead → `docs/archive/`; ADRs stay and supersede.**

## Why this matters (failure → doc class)

| Failure | Doc class that leaks | Defense |
|---|---|---|
| Stale "ground truth" | Entry/Living | timestamp + archive + prefer automation |
| Conflicting copies | any | single-source grep |
| Silent success | Entry | mandatory verify command |
| Reopened dead debate | ADR | rejected-alternatives field + supersede-in-place (never archive) |
| Live set polluted by dead files | Living/Constraint | archive on completion/retirement |