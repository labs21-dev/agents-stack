# Bounded explore stub (language-agnostic)

Use when Explore escalates to **Mode B**. Fill this; implement in whatever
runner fits the repo. Do not invent a preferred language.

## Machine (same as state-machine stub)

- Variables + domains:
- Init:
- Actions (name → guard → effect):
- Invariant(s):

## Bounds

- Max depth / max states:
- Domains kept finite how:

## Runner checklist

- [ ] Enumerate reachable states from Init via Actions
- [ ] Evaluate Inv at every state
- [ ] On fail: print ordered action trace + state before/after (or equivalent)
- [ ] On pass: record explored size + explicit non-claims (Boundaries)

## Result

- Pass / Fail:
- Trace (if Fail):
- Assumptions / not modeled:
