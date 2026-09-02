# Spec self-check

Run before generation. A weak spec makes downstream green tests meaningless.

## Checklist

- [ ] Behavior stated as input→output, not implied ("handles the user case" fails)
- [ ] Edges enumerated: null, empty, boundary, duplicate, concurrent, retry, oversized
- [ ] At least one invariant named in hard language ("should be safe" fails)
- [ ] Failure modes named for each edge ("undefined" fails)
- [ ] No hidden assumptions the AI must "just know"

## Scoring

Checked boxes / 5.

| Score | Action |
|---|---|
| 4-5 | Proceed. |
| 2-3 | Raise the spec, or accept lower ceiling — do not claim high quality. |
| 0-1 | STOP. Fall back to human reading, or rewrite the spec. |

## Output line (mandatory)

> Spec self-check: N/5. Cage strength = spec strength. [RED if N < 3]

## Protocol character

Concurrency / idempotency / trust boundary / lifecycle / cancel race →
delegate to `protocol-adversarial-design` (`delegation.md`). Its invariants
become this spec; its alignment tests become the verify-gate core.