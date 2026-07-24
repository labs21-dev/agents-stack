# Reverse gate — STOP screens

Run before opening any gate. Any failure → STOP, fall back to human reading.

## Screen 1 — Gate-catchable defect class?

Does quality reduce to things gates verify (input→output, invariants,
coverage, complexity)?

- Pass: CRUD endpoint, data transform, parser, feature with clear I/O
  contract, bugfix against a repro.
- STOP: quality hinges on abstract-level choice, cross-module emergence, or
  naming/intent alignment. Gates cannot catch these.

## Screen 2 — Spec hardenable?

Can the requirement become a hard spec at reasonable cost, or does it stay
irreducibly fuzzy ("make it feel natural", "the abstraction should be
cleaner")?

- Pass: stated behavior, edges enumerable.
- STOP: fuzzy spec + non-trivial cost. Reading code is cheaper than a cage
  that won't hold.

## Screen 3 — Generate, not comprehend?

- Pass: new feature, modify behavior, add test, fix bug.
- STOP: task is comprehending/assessing existing code. Read it. Gates do not
  produce comprehension.

## Screen 4 — Reversible enough to cage?

- Pass: L3 gates match irreversibility, or task is reversible.
- STOP: irreversible harm possible but only L1/L2 gates justified. Upgrade
  to L3 or fall back to human reading.

## STOP output

Use `templates/stop-output.md`:

```
STOP — reverse gate failed.
Failed screen(s): <which>
Reason: <why>
Recommended: <human read | meta-thinking-framework | protocol-adversarial-design>
```

## Negation list

- Abstract/architectural smell is the whole point
- Spec irreducibly fuzzy + non-trivial cost
- Task is comprehension, not generation
- Irreversible harm + only sampled gates justified